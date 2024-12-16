# Speech-to-Speech Translation 🎙️➡️🔊

A web application that transforms video content by translating speech from one language to another while preserving the original video. Built with Flask, Whisper, Google's Gemini, and various audio processing libraries.

## 🌟 Features

- Upload videos through an intuitive drag-and-drop interface
- Support for multiple languages including:
  - English 🇬🇧
  - Spanish 🇪🇸
  - French 🇫🇷
  - German 🇩🇪
  - Japanese 🇯🇵
  - Korean 🇰🇷
  - Hindi 🇮🇳
  - Bengali 🇮🇳
  - Telugu 🇮🇳
  - Tamil 🇮🇳
  - Marathi 🇮🇳
  - Kannada 🇮🇳
- Real-time speech-to-speech translation
- Automatic audio synchronization with video
- Modern, responsive UI with progress indicators
- Preview of both original and translated videos

## 🛠️ Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Speech Recognition**: OpenAI Whisper
- **Translation**: Google Gemini 1.5 Flash
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Audio Processing**: PyDub, MoviePy
- **ML Framework**: PyTorch, Transformers

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/speech-to-speech-translation.git
cd speech-to-speech-translation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```

## 🚀 Usage

1. Start the Flask server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Upload a video using the drag-and-drop interface or file selector

4. Select your target translation language

5. Click "Transform Now" and wait for the processing to complete

6. Preview both the original and translated videos

## 📁 Project Structure

```
speech-to-speech-translation/
├── app.py              # Flask application setup and routes
├── main.py            # Core translation and processing logic
├── static/            # Static files (CSS, JS, output videos)
├── templates/         # HTML templates
│   └── speechtospeech.html
├── uploads/          # Temporary storage for uploaded videos
└── requirements.txt  # Project dependencies
```

## ⚠️ Important Notes

- Ensure you have sufficient disk space for video processing
- Processing time depends on video length and system specifications
- Supported video formats: MP4 (recommended)
- Maximum video size limit depends on your server configuration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created by [Adarsh Yadav](https://github.com/yadavadarsh55)