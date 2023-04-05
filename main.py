from flask import Flask, render_template, json, jsonify, render_template_string
from flask_socketio import SocketIO
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os, shutil
from wtforms.validators import InputRequired
import io
import zipfile
from util.PDFServicesSDK.adobeAPI.src.extractpdf.extract_txt_table_info_with_figure_tables_rendition_from_pdf import ExtractAPI
from util.json2html.Json_converter import jsontohtml


app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Clearing Resources...')
    for files in os.listdir(app.config['UPLOAD_FOLDER']):
            path = os.path.join(app.config['UPLOAD_FOLDER'], files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
    print('Client disconnected')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        buf_stream = io.BufferedReader(file)
        extract = ExtractAPI(file.filename, buf_stream)
        result_zip = extract.adobe_extract()

        with zipfile.ZipFile(result_zip, 'r') as zip_ref:
            zip_ref.extractall(app.config['UPLOAD_FOLDER'])
        zip_ref.close()

        os.remove(result_zip)

        jsonobj = jsontohtml(app.config['UPLOAD_FOLDER'] + "/structuredData.json")
        html = jsonobj.json2html()

    

        return render_template_string(html)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    socketio.run(app)