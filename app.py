from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
import speech_recognition as sr
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)  # Add Swagger UI to your app

# Ensure the uploads folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def getsomething():
    """
    Health check route
    ---
    responses:
      200:
        description: Returns working status
    """
    response = "working......"
    return jsonify({'translated_text': response}), 200 


@app.route('/translate', methods=['POST'])
def translate():
    """
    Translate text from one language to another
    ---
    parameters:
      - name: body
        in: body
        schema:
          type: object
          required:
            - text
            - language_from
            - language_to
          properties:
            text:
              type: string
            language_from:
              type: string
            language_to:
              type: string
    responses:
      200:
        description: Translation successful
      400:
        description: Missing text or language code
    """
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
    """
    Transcribe an audio file to text
    ---
    parameters:
      - name: audio
        in: formData
        type: file
        required: true
    responses:
      200:
        description: Transcription successful
      400:
        description: No audio file provided or Google Speech Recognition error
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)
    audio_file.save(file_path)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(file_path) as source:
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

if __name__ == '__main__':
    app.run(debug=True)
