# app.py
from main import speech_to_speech
from flask import Flask, request, jsonify, render_template, url_for, send_from_directory
import os
import time

app = Flask(__name__)

# Configure static folder for uploads and output
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'

# Ensure the upload and output directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('speechtospeech.html')

@app.route('/speech-to-speech', methods=['POST'])
def speech_to_speech_api():
    try:
        if 'video' not in request.files or 'language' not in request.form:
            return jsonify({"error": "Missing video or language parameter"}), 400

        video_file = request.files['video']
        trans_language = request.form['language']

        # Save uploaded video with unique filename
        input_filename = f"input_video_{int(time.time())}.mp4"
        temp_video_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        video_file.save(temp_video_path)

        # Generate output filenames
        output_video_filename = f"translated_video_{int(time.time())}.mp4"
        output_audio_filename = f"translated_audio_{int(time.time())}.mp3"
        
        video_output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_video_filename)
        audio_output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_audio_filename)

        # Process the video
        final_video_path, final_audio_path = speech_to_speech(temp_video_path, trans_language)

        # Move processed files to output directory
        os.rename(final_video_path, video_output_path)
        os.rename(final_audio_path, audio_output_path)

        # Generate URLs for the processed files
        video_url = url_for('static', filename=f"output/{output_video_filename}")
        audio_url = url_for('static', filename=f"output/{output_audio_filename}")

        return jsonify({
            "success": True,
            "video_url": video_url,
            "audio_url": audio_url
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)