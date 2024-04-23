######### Importaciones Para El Uso De Backend MVC########
from flask import jsonify
from config import config
from decouple import config as datos
from src import _init_app
from datetime import datetime, timedelta
from flask_cors import CORS
import whisper
################# END###################################
## INICIALIZADOR DEL BACKEND LLAMANDO LA CLASE INIT_APP##
configuracion = (config['development'])
app = _init_app(configuracion)

# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}})
CORS(app)
################# END###################################


@app.route('/')
def index():
    nameproyect = 'Backend Desarrollado En Python'
    name = 'Nami Asistente(Chatbot Prov.101)'
    teams = 'Kevin Oliveros - Isaac Perez - Roberto Lineros'
    date = datetime.now()
    date = date - timedelta(days=30 + 2)
    print(date)
    return jsonify({'Development:': name, 'Proyecto: ': nameproyect, 'Teams: ': teams, 'Fecha De Inicio': date}), 200

############### END####################################
# SALIDA PRINCIPAL AL ERROR DE RUTAS NO ENCNONTRADAS#


def pagina_no_encontrada(error):
    return "<h1>Señor Usuario La Pagina A Donde Intenta Acceder No Existe...</h1>", 404
##################### END################################

hosting:str = datos('HOST') # type: ignore
if __name__ == "__main__":
    #app.config['MODEL'] = whisper.load_model("small")
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host=datos('HOST'), port=datos('PORT'))   # type: ignore