from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
# Errors
from ..utils.service_error import CustomException
# Security
from src.utils.service_cifrado import Security
verify_token = Blueprint('verify_token', __name__)


@cross_origin()
@verify_token.route('/', methods=['GET', 'POST'])
def index_verify_token():

    return jsonify({'METODO': f'{request.method}', "Ruta Actual": "verify_token"}), 200


@cross_origin()
@verify_token.route('/now', methods=['GET', 'POST'])
async def verifytoken():
    if request.method == 'POST':
        headers = request.headers
        # print("Formato De Headers", headers)
        try:
            autorizacion, has_access, statuscode = await Security.verify_token(
                headers)
            # print('La Validacion Es: ', has_access, 'Code:', statuscode)
            if autorizacion and statuscode == 200:
                response = jsonify(
                    {'message': autorizacion, 'data': has_access})
                return response, statuscode

            if statuscode == 401:
                return jsonify({'message': autorizacion, 'user': 'UNAUTHORIZED'}), statuscode
            else:
                return jsonify({'message': autorizacion, 'data': has_access}), statuscode
        except CustomException as ce:
            return jsonify({'message': str(ce), 'success': False}), statuscode
    else:
        return jsonify({'METODO': f'{request.method}', "Ruta Actual": "verify_token/now"}), 200
