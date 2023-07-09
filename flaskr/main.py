from flaskr import app
from flask import render_template, request, redirect
from werkzeug.utils import secure_filename
import os, subprocess, sys

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
    
    convert_to_path = os.path.join('./flaskr/static/upload', secure_filename(convert_file.filename))
    convert_file.save(convert_to_path)

    width = request.form.get('width', type=int)

    fps = request.form.get('fps', type=int)

    # i - インプットファイル
    # f - フォーマット、mp4とかflvとか
    # y - 強制上書きオプション
    cmd = ['ffmpeg', '-y', '-i', convert_to_path]

    #　フレームレート設定
    if(fps != None and fps > 0):
        cmd.append('-r')
        cmd.append(f'{fps}')

    if(width != None and fps > 0):
        cmd.append('-vf')
        cmd.append(f'scale={width}:-1')

    # 最後に出力先を追加
    cmd.append(f'./flaskr/static/output/{convert_file.filename}.gif')
    cp = subprocess.run(cmd)

    if cp.returncode != 0:
        print('ls failed.', file=sys.stderr)
        sys.exit(1)

    return render_template('index.html', output=f'static/output/{convert_file.filename}.gif')

if __name__=='__main__':
    app.run(debug=True)
