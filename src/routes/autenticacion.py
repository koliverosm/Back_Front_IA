from flask_cors import cross_origin
from flask import Blueprint, request, jsonify
# Models
from src.models.m_client import User_login, Id_Face
# Security
from src.utils.service_cifrado import Security
# Services
from src.controllers.logincontroller import Logincontroller

autenticacion = Blueprint('autenticacion', __name__)
clsLogin = Logincontroller()


@autenticacion.route('/', methods=['GET', 'POST'])
def index():
    return jsonify({'success': 'Estas En La Ruta Autenticacion'})


@cross_origin()
@autenticacion.route('/generated_token', methods=['POST'])
async def auten_token():
    username = request.json['username']
    password = request.json['password']
    _user = User_login(0, username, password, None)
    authenticated_user = await clsLogin.c_login_credentials(_user)

    if (authenticated_user != None):
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token}), 201
    else:
        return jsonify({'message': 'Unauthorized'}), 401


@autenticacion.route('/generated_token_face', methods=['POST'])
async def auten_token_face():
    id_face_identy: str = request.json['id_face_identy']
    # print("Route", id_face_identy)
    model_id_face = Id_Face(id_face_identy)
    authenticated_user = await clsLogin.c_login_credentials_faces(model_id_face)

    if (authenticated_user != None):
        # print("Ya Fui y Tengo los Datos: ", authenticated_user.get_username())
        encoded_token = Security.generate_token(authenticated_user)
        return jsonify({'success': True, 'token': encoded_token}), 201
    else:
        return jsonify({'message': 'Unauthorized'}), 401
