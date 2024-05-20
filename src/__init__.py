# Importacion De Librerias
from flask import Flask
from flask_cors import CORS
from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
from decouple import config as datos
#import whisper
# Routes
from src.routes import usuario
from src.routes import uploads
from src.routes import autenticacion
from src.routes import autorizacion
from src.routes import voicesuser

###############
app = Flask(__name__,  template_folder='templates')


def _init_app(config):
    # Configuration
    app.config.from_object(config)
    app.config['SECRET_KEY'] = datos('SECRET_KEY')
    app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(
        os.getcwd(), 'app', 'uploads')
    
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    #CORS(app, resources={r"/*": {"origins": "http://localhost:4200"}}) ##CORS DEFAULT
    CORS(app)
    # Blueprints
    app.register_blueprint(uploads.uploadsFile,
                           url_prefix='/uploads')
    app.register_blueprint(
        usuario.Usuarios_blueprint, url_prefix='/usuarios')
    app.register_blueprint(
        autenticacion.autenticacion, url_prefix='/autenticacion')
    app.register_blueprint(autorizacion.verify_token,
                           url_prefix='/verify_token')
    app.register_blueprint(voicesuser.recognition,url_prefix='/recognition')
    return app
