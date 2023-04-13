from flask import Flask, render_template, json, jsonify, render_template_string, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_socketio import SocketIO
from wtforms import FileField, SubmitField, BooleanField
from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
import os, shutil
from wtforms.validators import InputRequired
import io
import zipfile
import tempfile
from util.PDFServicesSDK.adobeAPI.src.extractpdf.extract_txt_table_info_with_figure_tables_rendition_from_pdf import ExtractAPI
from util.json2html.Json_converter import jsontohtml
from util.soundscape import Sonify
import secrets



app = Flask(__name__)
socketio = SocketIO(app)
app.config['SECRET_KEY'] = 'supersecretkey'

def clean_resources():
    dir = session['UPLOAD_FOLDER']
    print('Clearing Resources at ', dir)
    shutil.rmtree(dir)
    session.pop('UPLOAD_FOLDER', None)

@socketio.on('connect')
def test_connect():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    clean_resources()
    print('Client disconnected')


class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired(), FileAllowed(['pdf'], "Wrong file format. Only PDFs allowed.")])
    submit = SubmitField("Upload File")
    remove_citations_toggle = BooleanField("Remove In-text Citations")
    sonify_images_toggle = BooleanField("Sonify Images")

@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])                
def home():
    form = UploadFileForm()
    error = ''
    if form.validate_on_submit():
        secretStr = secrets.token_hex(16)
        app.config['UPLOAD_FOLDER'] = 'static/' + secretStr
        session['UPLOAD_FOLDER'] = os.getcwd() + '/' + app.config['UPLOAD_FOLDER']
        file = form.file.data
        remove_citations = form.remove_citations_toggle.data

        sonify_images = form.sonify_images_toggle.data

        try:
            buf_stream = io.BufferedReader(file)
            extract = ExtractAPI(file.filename, buf_stream)
            result_zip = extract.adobe_extract()

            with zipfile.ZipFile(result_zip, 'r') as zip_ref:
                zip_ref.extractall(app.config['UPLOAD_FOLDER'])
            zip_ref.close()

            os.remove(result_zip)
        except Exception:
            error = 'Failed to extract from PDF. Please try again.'
            return render_template('index.html', form=form, error=error)
        
        if sonify_images:
            if os.path.exists(app.config['UPLOAD_FOLDER'] + '/figures'):
                try:
                    sonify = Sonify(app.config['UPLOAD_FOLDER'])
                    sonify.sonifyPDFImages()
                except Exception:
                    error = 'Failed to sonify images. Please try again.'
                    clean_resources()
                    return render_template('index.html', form=form, error=error)

        try:
            jsonobj = jsontohtml(app.config['UPLOAD_FOLDER'], remove_citations, sonify_images)
            html = jsonobj.json2html()
        except Exception:
            error = 'Failed to generate HTML. Please try again.'
            clean_resources()
            return render_template('index.html', form=form, error=error)

        return render_template_string(html)

    return render_template('index.html', form=form, error='')

if __name__ == '__main__':
    socketio.run(app)

