# Database
# from src.bd.bd import MyDbEnty

from src.models.m_client import UserFile
from ..dto.dtoImage import ImagenDTO
from mysql.connector import Error
from mysql.connector import IntegrityError
from flask import jsonify
from ..bd import bdxamm as base
bd = base.MyDbEnty()


class uploads():
    async def load_userFile_form(self, dataUser: UserFile, IMAGEN: ImagenDTO):
        try:
        
            # Ejecutar el procedimiento almacenado
            print(f' Datos: {dataUser.get_username} {dataUser.get_password} {dataUser.get_email} {IMAGEN.get_namefile}{ IMAGEN.get_id_face}')

            connection = bd.conectar_con_bd()
            cursor = connection.cursor()  # type: ignore
            cursor.execute("Call Insert_dataUser(%s,%s,%s,%s,%s,%s)",
                           (dataUser.get_username, dataUser.get_password, dataUser.get_email, IMAGEN.get_namefile, IMAGEN.get_datafile, IMAGEN.get_id_face,))
           
           # result = await cursor.fetchone()
           #  print(result)

           # result = cursor.fetchone()
            cursor.close()
            connection.commit()
            bd.kill_conexion(connection)
            return jsonify({"info": f"Resul 1: "}), 201
        except IntegrityError as error:
            return jsonify({"error": "Violación de la integridad de la clave única", "informacion": str(error)}), 500

        except Exception as error_general:
            return jsonify({"error": "Error general", "informacion": str(error_general)}), 500
        '''except Error as error:
            if error.errno == 1644:
                
                return jsonify({"error": "Los datos ya existen en la base de datos"}), 400
            elif error.errno == 1305:
                
                return jsonify({"error": "El procedimiento almacenado no existe"}), 500
            else:
                
                return jsonify({"error": "Error desconocido", "informacion": str(error)}), 500'''

    async def loadfile(self, IMAGEN: ImagenDTO):
        try:
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()  # type: ignore
            # cursor.execute("SET GLOBAL max_allowed_packet=67108864;")
            # Ejecutar el procedimiento almacenado
            cursor.execute("Call almacenar_foto (%s, %s , %s)",
                           (IMAGEN.get_namefile, IMAGEN.get_datafile, IMAGEN.get_id_face))

            # Capturar la salida del procedimiento almacenado
           # result = cursor.fetchone()
           # print('Varible ',result)
           # success_message = result[1] if result else None
           # print('Seccess Message',success_message)
            cursor.close()
            connection.commit()  # type: ignore
            bd.kill_conexion(connection)

            return jsonify({"generated": IMAGEN.id_face}), 201
        except Error as error:
            if error.errno == 1644:
                bd.kill_conexion(connection)
                return jsonify({"error": "Los datos ya existen en la base de datos"}), 400
            elif error.errno == 1305:
                return jsonify({"error": "El procedimiento almacenado no existe"}), 500
            else:
                return jsonify({"error": "Error desconocido", "informacion": str(error)}), 500

    def downloadfile(self, json):
        try:
            id = json.get('id')
            connection = bd.conectar_con_bd()
            cursor = connection.cursor()  # type: ignore
            cursor.execute("Call obtener_foto(%s)", (id,))
            rv = cursor.fetchall()
            cursor.close()
            bd.kill_conexion(connection)

            # Verificar si se obtuvieron resultados
            if rv is not None:

                for result in rv:
                    # Suponiendo que 'namefile' es el primer elemento y 'datafile' el segundo en el resultado
                    namefile = result[0]  # type: ignore
                    datafile = result[1]  # type: ignore
                    id_face = result[2]  # type: ignore
                    return ImagenDTO(namefile, datafile, id_face), 200
                else:
                    # No se encontraron registros para el id dado
                    return {"error": "No se encontró el registro."}, 404

        except IntegrityError as error:
            return jsonify({"error": "Violación de la integridad de la clave única", "informacion": str(error)}), 500

        except Exception as error_general:
            return jsonify({"error": "Error general", "informacion": str(error_general)}), 500
