from flask import jsonify, request, Blueprint
from flask_cors import cross_origin
from ..controllers import usuariocontroller
usr = usuariocontroller

con_usuario = usr.Usuariocontroller()

Usuarios_blueprint = Blueprint('usuarios', __name__)


@Usuarios_blueprint.route('/')
@cross_origin()
def index():

    return jsonify({'message': 'Welcome Estas En Ruta Usuario, Apartir De Aqui Todo LLeva /usuarios/+La Ruta Que Deseas Acceder'})


@Usuarios_blueprint.route('/validate', methods=['POST'])
@cross_origin()
def login():
    data = request.get_json()

    return con_usuario.c_validate(data)


@Usuarios_blueprint.route('/listausuarios', methods=['GET'])
@cross_origin()
def listausuarios():
    print('Usuarios Listados')
    return con_usuario.c_consultar_usuarios()


@Usuarios_blueprint.route('/crear_usuario', methods=['POST'])
@cross_origin()
def crear_usuario():
    data = request.get_json()
    return con_usuario.c_crear_usuario(data)


@Usuarios_blueprint.route('/crear_usuario_admin', methods=['POST'])
@cross_origin()
def crear_usuario_admin():
    data = request.get_json()
    return con_usuario.c_crear_usuario_admin(data)


@Usuarios_blueprint.route('/consultar_usuario_id', methods=['GET', 'POST'])
@cross_origin()
def consultar_usuario_id():
    return con_usuario.c_consultar_usuario_id()


'''
@Usuarios_blueprint.route('/actualizar_usuario', methods=['POST'])
@cross_origin()
def actualizar_usuario():

    return con_usuario.c_actualizar_usuario_id()


@Usuarios_blueprint.route('/bajar_usuario', methods=['POST'])
@cross_origin()
def bajar_usuario():
    return con_usuario.c_bajar_usuario()
'''
