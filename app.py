from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
import speech_recognition as sr
import os
from flasgger import Swagger
from pydub import AudioSegment  # Import pydub for audio conversion

app = Flask(__name__)
swagger = Swagger(app)

# Ensure the uploads folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def getsomething():
    response = "working......"
    return jsonify({'translated_text': response}), 200

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    if 'text' not in data or 'language_to' not in data or 'language_from' not in data:
        return jsonify({'error': 'Missing text or language code'}), 400

    text_to_translate = data['text']
    current_language = data['language_from']
    target_language = data['language_to']

    try:
        translator = GoogleTranslator(source=current_language, target=target_language)
        translated_text = translator.translate(text_to_translate)
        return jsonify({'translated_text': translated_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)

    try:
        # Convert .m4a to .wav using pydub
        if file_path.endswith('.m4a'):
            wav_file_path = file_path.replace('.m4a', '.wav')
            audio = AudioSegment.from_file(file_path)
            audio.export(wav_file_path, format="wav")
        else:
            wav_file_path = file_path

        # Transcribe the audio using speech_recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            return jsonify({'transcribed_text': text}), 200

    except sr.UnknownValueError:
        return jsonify({'error': 'Google Speech Recognition could not understand the audio'}), 400
    except sr.RequestError as e:
        return jsonify({'error': f'Google Speech Recognition request failed: {e}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(wav_file_path):
            os.remove(wav_file_path)

if __name__ == '__main__':
    app.run(debug=True)
