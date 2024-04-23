TF_ENABLE_ONEDNN_OPTS=0
import json
from keras.models import load_model
import pickle
from .procesamiento.nlp import Preprocessing
from .procesamiento import nlp
import os
search_name = nlp.CapturarNombre()
basepath = os.path.dirname(__file__)
# Cargar Los Modulos PreProsesados
intents =  json.loads(open(basepath+'/patrones/categorias.json').read())
words = pickle.load(open(basepath+'/palabras/palabras.pkl', 'rb'))
classes = pickle.load(open(basepath+'/clases/classes.pkl', 'rb'))
model = load_model(basepath+'/modelo/initial_model.h5')

# Funcion Que generar El PDF

class Asistente():

    def view_pdf(self ,response: str):

        return "view_pdf"
    '''while True:
        message = input("TU:  ")
        intent, confidence = Preprocessing.predict_class(
            message, model, words, classes)

        if confidence < 0.5:  # Umbral de confianza ajustable según necesites
            print("No se encontró un patrón relevante. Redirigiendo al modelo de texto generativo.")
        else:
            response = Preprocessing.get_response(intent, intents)
            if response == "crear volante pdf":
                response_ = view_pdf(response)
                print("Respuesta: ", response_)
            
            elif response == "nombre usuario":
                print(search_name.process_message(message))
            
            else:
                print("Respuesta General: ", response)'''
    @classmethod
    async def readtext(self , message):
        intent, confidence = Preprocessing.predict_class(
            message, model, words, classes)

        if confidence < 0.5:  # Umbral de confianza ajustable según necesites
            print("No se encontró un patrón relevante. Redirigiendo al modelo de texto generativo.")
            return 'No se encontró un patrón relevante. Redirigiendo al modelo de texto generativo'
        else:
            response = Preprocessing.get_response(intent, intents)
            if response == "crear volante pdf":
                response_ = self.view_pdf(response)
                print("Respuesta: ", response_)
                return response_
            elif response == "nombre usuario":
                print(search_name.process_message(message))
                return search_name.process_message(message)
            else:
                print("Respuesta General: ", response)
                return response

        return {"response": 'sin respuesta'}




    