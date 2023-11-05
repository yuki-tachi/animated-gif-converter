from flask import Flask

def create_app():
    UPLOAD_FOLDER = './static'
    ALLOWED_EXTENSIONS = {'mov', 'avi', 'mp4', 'wmv'}

    app = Flask(__name__, static_folder='./static')
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

    return app

# 循環インポート避け
import flaskr.main