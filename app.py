from flask import Flask, request
import base64
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
key = os.getenv("OPENAI_API_KEY")
openai.api_key = key

@app.route('/audio_transcribe_traslate', methods=['POST'])
def audio_transcribe_traslate():
    data = request.get_json()

    if 'audio' not in data:
        return {'error': 'No audio data found'}, 400

    audio_base64 = data['audio']
    file_name = data['filename']

    # Decode the base64 audio data and save it as a file
    audio_data = base64.b64decode(audio_base64.split(',')[1])
    with open(file_name, 'wb') as f:
        f.write(audio_data)

    audio_file= open(file_name, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    print(transcript["text"])

    res = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "Eres un traductor del Castellano al Ingles"},
            {"role": "user", "content": "Traduceme el siguiente texto: "+transcript["text"]}
        ]
    )
    print(res["choices"][0]["message"]["content"])

    return {'transcribe':transcript["text"],'traslate': res["choices"][0]["message"]["content"]}, 200
    # return {'message': res["choices"][0]["message"]["content"]}, 200

@app.route('/audio_transcribe', methods=['POST'])
def audio_transcribe():
    data = request.get_json()

    if 'audio' not in data:
        return {'error': 'No audio data found'}, 400

    audio_base64 = data['audio']
    file_name = data['filename']

    # Decode the base64 audio data and save it as a file
    audio_data = base64.b64decode(audio_base64.split(',')[1])
    with open(file_name, 'wb') as f:
        f.write(audio_data)

    audio_file= open(file_name, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    return transcript, 200


@app.route('/upload_audio_base64', methods=['POST'])
def upload_audio_base64():
    data = request.get_json()

    if 'audio' not in data:
        return {'error': 'No audio data found'}, 400

    audio_base64 = data['audio']
    file_name = data['filename']
    file_type = data['filetype']
    # file_name = f'recording.{file_type}'

    # Decode the base64 audio data and save it as a file
    audio_data = base64.b64decode(audio_base64.split(',')[1])

    # audio_data.save(file_name)
    with open(file_name, 'wb') as f:
        f.write(audio_data)

    return {'message': 'Audio file uploaded and saved successfully'}, 200


@app.route('/upload_audio', methods=['POST'])
def upload_audio():

    print(request.files)  # Print request.files to see its content
    if 'audio' not in request.files:
        return {'error': 'No audio file found'}, 400

    audio = request.files['audio']
    print('Nombre del archivo:', audio.filename)
    print('Tamaño del archivo:', audio.content_length)
    print('Tipo de contenido:', audio.content_type)

    if audio.filename == '':
        return {'error': 'No audio file name found'}, 400
    

    audio.save(audio.filename)
    return {'message': 'Audio file uploaded and saved successfully'}, 200

if __name__ == '__main__':
    app.run()
