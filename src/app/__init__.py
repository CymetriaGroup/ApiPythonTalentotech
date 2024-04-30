from flask import Flask
from flask_cors import CORS
from app.estudiantes.estudiantes import estudiantes



def createApp():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(estudiantes)
    return app