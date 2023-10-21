from . import app
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os, subprocess, sys

def allowed_file(filename) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_secure_absolute_path_to_temp(filename: str) -> str:
    return os.path.join(f'{app.root_path}/temp', secure_filename(filename))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        print('convert get')
        return render_template('index.html', output="")

    if 'convert_file' not in request.files:
        print("no convert_file part")
        return redirect(request.url)
    
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
    cmd = ['ffmpeg', '-y', '-i', convert_to_path]

    fps = request.form.get('fps', type=int)
    #　フレームレート設定
    if(fps != None and fps > 0):
        cmd.append('-r')
        cmd.append(f'{fps}')

    width = request.form.get('width', type=int)
    if(width != None and fps > 0):
        cmd.append('-vf')
        cmd.append(f'scale={width}:-1')

    # 最後に出力先を追加
    cmd.append(f'{app.root_path}/static/converted/{convert_file.filename}.gif')
    cp = subprocess.run(cmd)

    if cp.returncode != 0:
        print('ls failed.', file=sys.stderr)
        sys.exit(1)

    return render_template('index.html', converted=f'static/converted/{convert_file.filename}.gif')
