import torch
import torchaudio
from gtts import gTTS
from pydub import AudioSegment
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from moviepy import VideoFileClip, AudioFileClip
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser
from transformers import WhisperProcessor, WhisperForConditionalGeneration

def video_into_audio(video_path):
    clip = VideoFileClip(video_path)
    audio_path = 'original_audio.mp3'
    clip.audio.write_audiofile(audio_path)
    return audio_path


def get_transcripts(audio_path):

    model_name = "openai/whisper-large-v2"
    processor = WhisperProcessor.from_pretrained(model_name)
    model = WhisperForConditionalGeneration.from_pretrained(model_name)

    speech_array, sample_rate = torchaudio.load(audio_path)

    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(sample_rate, 16000)
        speech_array = resampler(speech_array)
        sample_rate = 16000

    inputs = processor(speech_array.squeeze(0).numpy(), sampling_rate=sample_rate, return_tensors="pt")

    with torch.no_grad():
        generated_ids = model.generate(inputs["input_features"])

    transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return transcription


def get_LLMChain(text, target_language):

    load_dotenv()

    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

    prompt_template = PromptTemplate(
        input_variables=["text", "target_language"],
        template="Translate the following text to {target_language} as if you are translating it in the real time to give it a look of a great translation:\n\n{text}"
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        output_parser=StrOutputParser()
    )

    res = chain.invoke({'text':text, 'target_language':target_language})
    print(res)

    return res['text']


def get_speech(text, output_path="output_audio.mp3"):
    tts = gTTS(text)
    tts.save(output_path)
    return output_path


def adjust_audio_speed(audio_file, original_video_path, output_file="adjusted_audio.mp3"):
    audio = AudioSegment.from_file(audio_file)
    video = VideoFileClip(original_video_path)
    target_duration = video.duration
    current_duration = audio.duration_seconds
    speed_factor = current_duration / target_duration
    adjusted_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * speed_factor)
    }).set_frame_rate(audio.frame_rate)
    adjusted_audio.export(output_file, format="mp3")
    return output_file


def replace_audio_in_video(original_video_path, translated_audio_path, output_video_path="output_video.mp4"):
    video = VideoFileClip(original_video_path)
    translated_audio = AudioFileClip(translated_audio_path)
    video_with_new_audio = video.with_audio(translated_audio)
    video_with_new_audio.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    return output_video_path


def speech_to_speech(original_video, trans_language):

    # Getting the Audio from the Video 
    audio_input = video_into_audio(original_video)

    # Getting the transcripts
    transcripts = get_transcripts(audio_input)

    # LLM Chain for translation
    trans_text = get_LLMChain(transcripts, trans_language)

    # Converting Text to Speech
    audio = get_speech(trans_text)

    # Adjusting the speed of the audio file
    final_audio = adjust_audio_speed(audio, original_video)

    # Merging it into the original video
    final_video = replace_audio_in_video(original_video, final_audio)

    return final_video, final_audio


if __name__ == "__main__":

    video = input("Enter the path of the video: ")
    language = input("Enter the desired language: ")

    res_video, res_audio = speech_to_speech(video, language)