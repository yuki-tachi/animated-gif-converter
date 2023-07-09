from flask import Flask

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = {'mov', 'avi', 'mp4', 'wmv'}

app = Flask(__name__, static_folder='./static')
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

import flaskr.main
