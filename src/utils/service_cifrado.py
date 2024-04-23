from decouple import config
import datetime
import jwt
import pytz


class Security():

    secret = config('JWT_KEY')
    tz = pytz.timezone("America/Bogota")

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            'iat': datetime.datetime.now(tz=cls.tz),
            'exp': datetime.datetime.now(tz=cls.tz) + datetime.timedelta(minutes=5),
            'username': authenticated_user.get_username(),
            'roles': authenticated_user.get_roles()

        }

        return jwt.encode(payload, cls.secret, algorithm="HS256")

    @classmethod
    async def verify_token(cls, headers):
        authenticated = False
        data_jwt = ""
        if 'Authorization' in headers:
            authorization = headers['Authorization']
            encoded_token = authorization.split(" ")[1]

            if len(encoded_token) > 0:
                try:
                    payload = jwt.decode(
                        encoded_token, cls.secret, algorithms=["HS256"])
                    roles = payload['roles']
                   
                    if 'admin' in roles:
                        authenticated = True
                        data_jwt = payload
                    elif 'user' in roles:
                        authenticated = True
                        data_jwt = payload
                    return authenticated, data_jwt, 200

                except jwt.ExpiredSignatureError:
                    # Excepción cuando la firma del token ha expirado
                    print("token expired")
                    data_jwt = "token expired"
                    return authenticated, data_jwt, 203

                except jwt.InvalidSignatureError:
                    # Excepción cuando la firma del token es inválida
                    print("token is invalid")
                    data_jwt = 'Invalid Signature'
                    return authenticated, data_jwt, 401

                except jwt.DecodeError:
                    # Excepción cuando hay un error de decodificación
                    print("error de decodificación")
                    data_jwt = 'Error Al Decodificar'
                    return authenticated, data_jwt, 403

        else:
            # No se proporcionó un token válido
            data_jwt= 'No Authorization'
            return authenticated , data_jwt , 404
