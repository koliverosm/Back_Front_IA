## _____     Importacion De Librerias _____________________________##

from .user_actions.functions import funciones
from flask import jsonify
from .resources.procesamiento import nlp
from .resources.procesamiento.nlp import Preprocessing
import pickle
from keras.models import load_model
import json
#from transformers import GPT2LMHeadModel, GPT2Tokenizer
import os
# __ Desactivar Mensajes De La Consola
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# ______________________________________
## ________________________________________________________________##

search_name = nlp.CapturarNombre()
search_function = funciones()
dir_actual = os.path.dirname(__file__)  # Cargar El Directorio actual
# Cargar Nuestros  Modelos  PreEntrenados
intents = json.loads(open(dir_actual+'/resources/patrones/categorias.json').read())
words = pickle.load(open(dir_actual+'/resources/palabras/palabras.pkl', 'rb'))
classes = pickle.load(open(dir_actual+'/resources/clases/classes.pkl', 'rb'))
model = load_model(dir_actual+'/resources/modelo/initial_model.h5')
## _____________________________________________________________###

# Cargar Modelo Gpt-2
# Puedes usar otros tamaños de modelo como "gpt2-medium", "gpt2-large", etc.
#model_name = 'gpt2'
#tokenizer = GPT2Tokenizer.from_pretrained(model_name)
#modelgpt2 = GPT2LMHeadModel.from_pretrained(model_name)

## ____________________________________________________________####


class Asistente():

    '''async def modelogpt(text):

        input_ids = tokenizer.encode(text, return_tensors="pt")
        max_length = 20  # Longitud máxima del texto generado
        num_return_sequences = 1  # Número de secuencias de texto a generar
        output_sequences = modelgpt2.generate(
            input_ids, max_length=max_length, num_return_sequences=num_return_sequences, temperature=1.0)
        return tokenizer.decode(output_sequences[0], skip_special_tokens=True)'''

    @classmethod
    async def readtext(cls, message):
        try:
            intent, confidence = Preprocessing.predict_class(
                message, model, words, classes)
            if confidence < 0.5:  # Umbral de confianza ajustable según necesites
                promt = f'Usuario: {message} Sistema:'
                #respuestagpt = await cls.modelogpt(promt)
                '''  notification.notify(timeout=10, ticker='NAMI BASE',
                                    title="GPTGENERATED", message=f'{respuestagpt}', app_name='Nami', toast=True)'''
                respuestagpt ="Modelo Generativo"
                return respuestagpt
            else:
                response = await Preprocessing.get_response(intent, intents)
                if response == "generar_certificado":
                    response_ = await  search_function.generar_certificado(response)
                    return response_
                elif response == "nombre usuario":
                    print(search_name.process_message(message))
                    return search_name.process_message(message)
                else:
                    print("Respuesta General: ", response)
                    return response
        except Exception as error_general:
            print({"informacion": str(error_general)})
            return "Error En Chatnami", 500
