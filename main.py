import torch
import torchaudio
from gtts import gTTS
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.output_parsers import StrOutputParser
from transformers import WhisperProcessor, WhisperForConditionalGeneration, AutoProcessor, AutoModel

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


def get_LLMChain():

    llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

    prompt_template = PromptTemplate(
        input_variables=["text", "target_language"],
        template="Translate the following text to {target_language}:\n\n{text}"
    )

    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        output_parser=StrOutputParser()
    )

    return chain

def get_speech(text, output_path="output_audio.wav"):
    tts = gTTS(text)
    tts.save(output_path)
    return output_path


if __name__ == "__main__":

    load_dotenv()

    audio_path = input("Enter the path of the audio: ")
    transcription = get_transcripts(audio_path=audio_path)

    lang = input("Enter the language you want to convert into: ")
    chain = get_LLMChain()

    source_text = transcription
    target_language = lang

    translated_text = chain.invoke({"text": source_text, "target_language": target_language})

    print("")
    print(f"Transcription: {transcription}\n")
    print("Translated Text:", translated_text['text'])

    audio_output_path = get_speech(translated_text['text'])
    print(f"Generated speech saved at: {audio_output_path}")