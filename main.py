from flask import Flask, render_template, json, jsonify
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os, shutil
from wtforms.validators import InputRequired
import io
import zipfile
import tempfile
from util.PDFServicesSDK.adobeAPI.src.extractpdf.extract_txt_table_info_with_figure_tables_rendition_from_pdf import ExtractAPI

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir() + '/'

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

        with open(f"{app.config['UPLOAD_FOLDER']}/structuredData.json", 'r') as myfile:
            data = json.loads((myfile.read()))
        
        text_dump = ""
        for t in data.get('elements'):
            text_dump += t.get('Text', '<IMAGE/TABLE>')
            text_dump += '\n'

        for files in os.listdir(app.config['UPLOAD_FOLDER']):
            path = os.path.join(app.config['UPLOAD_FOLDER'], files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)
 
        
        return render_template('success.html',  title="page", jsonfile=text_dump)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)