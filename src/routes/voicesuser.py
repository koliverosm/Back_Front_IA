from email import message_from_file
from flask import current_app, jsonify, Blueprint, request
from werkzeug.utils import secure_filename
from ..chat.chatnami import Asistente
import os
# __ Desactivar Mensajes De La Consola
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from decouple import config as datos
#from openai import OpenAI

# main = Asistente()

#client = OpenAI(api_key=datos('OPENAI_API_KEY'),)

recognition = Blueprint('recognition', __name__)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'waw'}
    result = '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return result


@recognition.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome Estas En Ruta Voice, Apartir De Aqui Todo LLeva /voice/+La Ruta Que Deseas Acceder'})


@recognition.route('/voice', methods=['POST'])
async def voice():

    try:
        audio = request.files['audio']
        print('Esto Es lo Segundo', audio)

        # Verificar que el archivo sea una imagen
        if audio and allowed_file(audio.filename):
            # La ruta donde se encuentra el archivo actual
            basepath = os.path.dirname(__file__)
            # Nombre original del archivo
            filename = secure_filename(audio.filename)  # type: ignore

            # Guardar el archivo en el sistema de archivos
            extension = os.path.splitext(filename)[1]
            nuevoNombreFile = filename + extension  # name_face_generator() + extension
            upload_path = os.path.join(
                basepath, '../uploads/audios', filename)
            print('Ruta: ', upload_path)
            audio.save(upload_path)
            audio_file = open(upload_path, 'rb')
            print(audio_file)
           # transcription = client.audio.transcriptions.create(model="whisper-1",file=audio_file)
            # transcribed = openai.Audio.transcribe("whisper-1",audio_file)
            # model = current_app.config['MODEL']
            # result =  model.transcribe(upload_path)
            # print(result["text"])
            return jsonify({'response': 'transcription[text]'}), 201
        else:
            return jsonify({'Error': 'No se pudo obtener la foto'}), 404
    except Exception as error_general:
        return jsonify({"error": "Error general", "informacion": str(error_general)}), 500


@recognition.route('/text', methods=['POST'])
async def text():
    try:
        text = request.json['text']
        print('User: ',text)
        if text:
            respuesta = await Asistente.readtext(text)
            return jsonify({'response': respuesta}), 201
        else:
            return jsonify({'Error': ''}), 404
    except Exception as error_general:
        return jsonify({"error": "Error general", "informacion": str(error_general)}),500
