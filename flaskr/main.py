from flask import render_template, request, redirect, Flask, url_for
from werkzeug.utils import secure_filename
import math, os, sys, subprocess, base64, re, uuid

def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_secure_absolute_path_to_temp(filename: str) -> str:
    return os.path.join(f'./flaskr/temp', secure_filename(filename))

def convert_size_format(size: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
    i = math.floor(math.log(size, 1024)) if size > 0 else 0
    size = round(size / 1024 ** i, 2)

    return f"{size} {units[i]}"

def create_app():
    ALLOWED_EXTENSIONS = {'mov', 'avi', 'mp4', 'wmv'}
    
    app = Flask(__name__, static_folder='./static')
    print(app.root_path)
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    return app

def get_base64() -> str:
    uploadimage_base64 = ""
    with open(f'./flaskr/static/converted/output.gif',"rb") as imagefile:
        # bytesファイルのデータをbase64にエンコードする
        uploadimage_base64 = base64.b64encode(imagefile.read())

    # base64形式のデータを文字列に変換する。その際に、「b'」と「'」の文字列を除去する
    uploadimage_base64_string = re.sub('b\'|\'', '', str(uploadimage_base64))

    return f'data:image/gif;base64,{uploadimage_base64_string}'  

app = create_app()

@app.route('/redirect/')
def redirect_example():
    # url_for で index() に紐付いた URL を生成
    # 生成された URL にリダイレクト
    app = {'file_name': 'static/converted/3c1cc385-bb67-4032-af26-dc57c2a38309.gif'}
    return redirect(url_for('index', app=app)) 

@app.route('/', methods=['GET', 'POST'])
def index(app:dict[str, any] = None):
    print(os.getcwd())

    return render_template('index.html', app=app)


@app.route('/processing', methods=['GET', 'POST'])
def processing():
    if 'convert_file' not in request.files:
        print("no convert_file part")
        return render_template('index.html')
    
    convert_file = request.files.get('convert_file')

    if convert_file.filename == '':
        print("No selected file")
        return redirect(request.url)
    
    if not allowed_file(convert_file.filename):
        return redirect(request.url)
    
    convert_to_path = get_secure_absolute_path_to_temp(convert_file.filename)
    convert_file.save(convert_to_path)

    # i - インプットファイル
    # f - フォーマット、mp4とかflvとか
    # y - 強制上書きオプション
    cmd = ['docker', 'exec', 'ffmpeg', 'ffmpeg', '-y', '-i', convert_to_path]

    fps = request.form.get('fps', type=int)
    #　フレームレート設定
    if(fps != None and fps > 0):
        cmd.append('-r')
        cmd.append(f'{fps}')

    width = request.form.get('width', type=int)
    if(width != None and fps > 0):
        cmd.append('-vf')
        cmd.append(f'scale={width}:-1')

    file_name = uuid.uuid4()
    # 最後に出力先を追加
    cmd.append(f'./flaskr/static/converted/{file_name}.gif')
    cp = subprocess.run(cmd)

    if cp.returncode != 0:
        print('ls failed.', file=sys.stderr)
        sys.exit(1)


    base_size=os.path.getsize(convert_to_path)
    converted_size=os.path.getsize(f'./flaskr/static/converted/{file_name}.gif')

    # filebinary = get_base64()
    # os.remove(convert_to_path)
    # os.remove(f'./flaskr/static/converted/output.gif')
    app = {
        'file_name': f'static/converted/{str(file_name)}.gif',
        'base_size_formatted': convert_size_format(base_size),
        'converted_size_formatted': convert_size_format(converted_size),
        'fps': fps,
        'width': width,
    }

    return render_template('index.html', app = app)
    # return url_for('index', app = app)
