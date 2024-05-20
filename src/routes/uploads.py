import uuid as has_id_face
from flask import json, jsonify, request, Blueprint
from flask_cors import cross_origin
from flask_uploads import UploadNotAllowed, UploadSet, IMAGES
from werkzeug.utils import secure_filename

from random import sample
import os
from src.dto.dtoImage import ImagenDTO
from src.models.m_client import UserFile
from ..controllers import uploadscontroller
from cryptography.fernet import Fernet
import base64
from decouple import config as datos

carga = uploadscontroller.UploadController()
uploadsFile = Blueprint('uploadsFile', __name__)
photos = UploadSet('photos', IMAGES)


################# FUNCIONES PRINCIPALES#############################
def name_face_generator():
    # Generando string aleatorio
    string_aleatorio = "KEVINISAACROBERTO"
    longitud = 10
    secuencia = string_aleatorio.upper()
    resultado_aleatorio = sample(secuencia, longitud)
    string_aleatorio = "".join(resultado_aleatorio)
    return string_aleatorio


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    result = '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    return result


def __encrypt(photo_encryted: bytes):
    clave: str = datos('SECRET_KEY_PHOTO')  # type: ignore
    print("Esta Es La Clave SECRET: ", clave)
    fernet = Fernet(clave)  # type: ignore
    foto_encriptada = fernet.encrypt(photo_encryted)
    return foto_encriptada

###############################################


@uploadsFile.route('/')
@cross_origin()
def index():
    return jsonify({'message': 'Welcome Estas En Ruta Uploads, Apartir De Aqui Todo LLeva /uploads/ + La Ruta Que Deseas Acceder'})

####Buscar foto por id de la foto
@uploadsFile.route('/getfoto', methods=['POST', 'GET'])  # type: ignore
async def getfoto():
    data = request.get_json()
    foto_info, status_code = carga.c_getfoto(data)  # type: ignore

    if foto_info and status_code == 200:
        basepath = os.path.dirname(__file__)
        # Crear el path completo incluyendo el nombre del archivo para guardar la imagen
        upload_path = os.path.join(
            basepath, '../uploads/photo_query', f'{foto_info.namefile}')
        # Escribir los bytes de la imagen en el archivo
        with open(upload_path, 'wb') as archivo:
            archivo.write(foto_info.datafile)  # type: ignore
        foto_base64 = base64.b64encode(foto_info.datafile).decode('utf-8')
        # with open(upload_path, 'rb') as f:
        #          foto = f.read()
        return jsonify({'namefile': f'{foto_info.namefile}', 'file': foto_base64, 'id_face': f'{foto_info.id_face}'}), status_code
    else:
        return jsonify({'Error': 'No se pudo obtener la foto'}), 404

#################END 

#########################
@uploadsFile.route('/getfotoidenty', methods=['POST', 'GET'])  # type: ignore
async def search_photo():
    
    
    if request.method == 'POST':
        identy = request.get_json()
        foto_info, status_code = await carga.c_getphoto_identy(identy)  # type: ignore

        if foto_info and status_code == 200:
            basepath = os.path.dirname(__file__)
            # Crear el path completo incluyendo el nombre del archivo para guardar la imagen
            upload_path = os.path.join(
                basepath, '../uploads/photo_query', f'{foto_info.namefile}')
            # Escribir los bytes de la imagen en el archivo
            with open(upload_path, 'wb') as archivo:
                archivo.write(foto_info.datafile)  # type: ignore
            foto_base64 = base64.b64encode(foto_info.datafile).decode('utf-8')
            # with open(upload_path, 'rb') as f:
            #          foto = f.read()
            return jsonify({'namefile': f'{foto_info.namefile}', 'file': foto_base64, 'id_face': f'{foto_info.id_face}'}), status_code
        elif status_code == 404:
                      return jsonify(foto_info), status_code
    else:
        return jsonify({'Metodo': f'{request.method}'}), 200

###################3
@uploadsFile.route('/file', methods=['POST'])
async def upload_file():

    if request.method == 'POST':
        try:
            file = request.files['image']
            print('Esto Es lo Segundo', request.files)
            # Verificar que el archivo sea una imagen
            if file and allowed_file(file.filename):
                # La ruta donde se encuentra el archivo actual
                basepath = os.path.dirname(__file__)
                # Nombre original del archivo
                filename = secure_filename(file.filename)  # type: ignore
                id_face = has_id_face.uuid5(
                    has_id_face.NAMESPACE_DNS, f'{filename}')

                # Guardar el archivo en el sistema de archivos
                extension = os.path.splitext(filename)[1]
                nuevoNombreFile = filename + extension  # name_face_generator() + extension
                upload_path = os.path.join(
                    basepath, '../uploads/Face_reco', nuevoNombreFile)

                file.save(upload_path)
                ##### Encriptar La Foto En Formarlo BLOB Para la base de datos #####
                with open(upload_path, 'rb') as f:
                    foto = f.read()
               # respuesta = ""
               # code = 201

                respuesta, code = await carga.c_upload(ImagenDTO(filename, foto, f'{id_face}'))
                # print('Esta Es la Repuesta Despues De Subir ROUTES',respuesta, "Codigo", code)
                if code == 201:
                    # si se sube correctamente en la base de datos se guarda en el directorio
                    # file.save(upload_path)
                    return respuesta, 201
                elif code == 400:

                    return respuesta, 400
            else:
                # print("Tipo de archivo no permitido. Por favor, suba solo archivos de imagen.")
                return 'Tipo de archivo no permitido. Por favor, suba solo archivos de imagen.'
        except UploadNotAllowed:
            return 'Tipo de archivo no permitido'
    return 'No se ha  subido ningún archivo'


@uploadsFile.route('/adminFile', methods=['POST'])
async def upload_file_admin():
    if request.method == 'POST':
        try:
          #  print('Datos del formulario:', request.form)
           # print('Encabezados:', request.headers)
            # print('Archivos:', request.files)
            file = request.files['image']
            dataUser = json.loads(request.form['dataUser'])
            # print("Esto Llega De JS ", file)
            username = dataUser.get('username')
            password = dataUser.get('password')
            email = dataUser.get('email')
            id_face_form = dataUser.get('id_face')
            # print(dataUser)
            # print('User', username, password, email)
            if file and allowed_file(file.filename):
                # La ruta donde se encuentra el archivo actual
                basepath = os.path.dirname(__file__)
                # Nombre original del archivo
                filename = secure_filename(file.filename)  # type: ignore
                # Guardar el archivo en el sistema de archivos
                extension = os.path.splitext(filename)[1]
                nuevoNombreFile = filename + extension  # name_face_generator() + extension
                upload_path = os.path.join(
                    basepath, '../uploads/Face_reco', nuevoNombreFile)
                file.save(upload_path)
                ##### Encriptar La Foto En Formarlo BLOB Para la base de datos #####
                with open(upload_path, 'rb') as f:
                    foto = f.read()
                respuesta, code = await carga.c_upload_userFile(UserFile(username, password, email), ImagenDTO(filename, foto, f'{id_face_form}'))
                # print('Esta Es la Repuesta Despues De Subir ROUTES',respuesta, "Codigo", code)
                if code == 201:
                    # si se sube correctamente en la base de datos se guarda en el directorio
                    # file.save(upload_path)
                    return respuesta, 201
                elif code == 400:
                    return respuesta, 400
            else:
                mensaje = 'Tipo de archivo no permitido. Por favor, suba solo archivos de imagen.'
                return jsonify({'message': mensaje})

            return jsonify({'message': ''})
        except UploadNotAllowed:
            return jsonify({'message': 'Tipo de archivo no permitido'})

    else:
        return jsonify('metodo', request.method, 'Estas En La Ruta /upload')


@uploadsFile.route('/generated', methods=['GET'])
def generated():
    id_face = has_id_face.uuid5(has_id_face.NAMESPACE_DNS, name_face_generator())
    print("Generado Desde El Backend: ", id_face)
    return jsonify({'generated': f'{id_face}'}), 201
