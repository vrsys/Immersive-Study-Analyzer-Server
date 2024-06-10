import json
import os
import threading
import time
from os import listdir
from os.path import isfile, join
from flask import Flask, request, send_from_directory
from werkzeug.serving import make_server
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ANNOTATION_FOLDER = os.path.join(app.root_path, 'annotations')
ALLOWED_EXTENSIONS = {'wav', 'txt', 'recordmeta'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ANNOTATION_FOLDER'] = ANNOTATION_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello():
    return 'Hello, World!'


@app.route('/all_recording_names', methods=['GET'])
def get_all_recording_names():
    files = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
    recording_names = []
    for file in files:
        if '.txt' in file and '_sound' not in file and '_arb' not in file:
            clean_name = file.replace('.txt', '')
            recording_names.append(clean_name)
    json_object = {"replayNames" : recording_names}
    return json_object


@app.route('/get_transform_recording/<name>', methods=['GET'])
def get_transform_recording(name):
    files = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
    file_name = ''
    for file in files:
        if '.txt' in file and '_sound' not in file and '_arb' not in file and name in file:
            file_name = file
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=file_name,  as_attachment=True)


@app.route('/get_sound_recording/<name>', methods=['GET'])
def get_sound_recording(name):
    files = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
    file_name = ''
    for file in files:
        if '.txt' in file and '_sound' in file and name in file:
            file_name = file
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=file_name,  as_attachment=True)


@app.route('/get_meta_recording/<name>', methods=['GET'])
def get_meta_recording(name):
    files = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
    file_name = ''
    for file in files:
        if '.recordmeta' in file and name in file:
            file_name = file
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=file_name,  as_attachment=True)


@app.route('/get_arb_recording/<name>', methods=['GET'])
def get_arb_recording(name):
    files = [f for f in listdir(app.config['UPLOAD_FOLDER']) if isfile(join(app.config['UPLOAD_FOLDER'], f))]
    file_name = ''
    for file in files:
        if '.txt' in file and '_arb' in file and name in file:
            file_name = file
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=file_name,  as_attachment=True)


@app.route('/upload/<filename>', methods=['PUT'])
def upload_file(filename):
    if allowed_file(filename):
        filename = secure_filename(filename)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
            f.write(request.stream.read())

        return "Success"


@app.route('/annotations/<recording_name>', methods=['POST', 'GET'])
def annotation(recording_name):
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            try:
                content = json.loads(file.read())
                filename = secure_filename(recording_name + '_' + file.filename)
                with open(os.path.join(app.config['ANNOTATION_FOLDER'], filename), 'w') as f:
                    json.dump(content, f)
                return "Success"
            except Exception as e:
                return e

    if request.method == 'GET':
        files = [f for f in listdir(app.config['ANNOTATION_FOLDER']) if isfile(join(app.config['ANNOTATION_FOLDER'], f))]
        annotations = []
        for file in files:
            if recording_name in file:
                f = open(join(app.config['ANNOTATION_FOLDER'], file), 'r')
                content = json.loads(f.read())
                return content
                annotations.append(content)
        return ""



class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('0.0.0.0', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


if __name__ == '__main__':
    if os.environ.get('GITHUB_ACTIONS'):
        timeout = 10
        server_thread = ServerThread(app)
        server_thread.start()
        time.sleep(timeout)
        server_thread.shutdown()
        server_thread.join()
    else:
        app.run(host='0.0.0.0')