from flask_app import app
from flask_app import UploadFileForm

def test_SubmitValidPDFWithToggles(client):
    form = dict(file = {'data':'tests/3292147.3292161.pdf'}, remove_citations_toggle = {'data': True}, sonify_images_toggle = {'data': True})
    
    response =  client.post(
        '/home',
        data=form
    )
    assert response.status_code == 200

def test_SubmitInvalidPDFWithToggles(client):
    form = dict(file = {'data':'tests/3292147.3292161.ppt'}, remove_citations_toggle = {'data': True}, sonify_images_toggle = {'data': True})
    response =  client.post(
        '/home',
        data=dict(form)
    )
    assert Exception


def test_SubmitInvalidPDFWithoutToggles(client):
    form = dict(file = {'data':'tests/fake.pdf'}, remove_citations_toggle = {'data': True}, sonify_images_toggle = {'data': True})

    response =  client.post(
        '/home',
        data=dict(form)
    )
    assert Exception

def test_SubmitPDFWithoutSonifyToggle(client):
    form = dict(file = {'data':'tests/3292147.3292161.pdf'}, remove_citations_toggle = {'data': True}, sonify_images_toggle = {'data': False})
    response =  client.post(
        '/home',
        data=dict(form)
    )
    assert response.status_code == 200

def test_SubmitPDFWithoutCitationToggle(client):
    form = dict(file = {'data':'tests/3292147.3292161.pdf'}, remove_citations_toggle = {'data': False}, sonify_images_toggle = {'data': True})
    response =  client.post(
        '/home',
        data=dict(form)
    )
    assert response.status_code == 200

def test_SubmitPDFWithoutAllToggles(client):
    form = dict(file = {'data':'tests/3292147.3292161.pdf'}, remove_citations_toggle = {'data': False}, sonify_images_toggle = {'data': False})
    response =  client.post(
        '/home',
        data=dict(form)
    )
    assert response.status_code == 200

from util.PDFServicesSDK.adobeAPI.src.extractpdf.extract_txt_table_info_with_figure_tables_rendition_from_pdf import ExtractAPI
from util.json2html.Json_converter import jsontohtml
from util.soundscape import Sonify
import io
import zipfile
import os

def test_unitExtraction(client):
    #file = io.open('tests/3292147.3292161.pdf', "rb")
    with io.open('tests/3292147.3292161.pdf', 'rb') as f:
        buf_stream = io.BufferedReader(f)
        extract = ExtractAPI('tests/3292147.3292161.pdf', buf_stream)
        result_zip = extract.adobe_extract()

    os.remove(result_zip)

    assert result_zip

def test_unitJsonToHtml(client):
    file = 'tests/'
    jsonobj = jsontohtml(file, False, False, '')
    html = jsonobj.json2html()

    assert html

def test_unitSonify(client):
    sonify = Sonify('tests/')
    sonify.sonifyPDFImages()

    assert sonify

def test_unitcitationRemoval(client):
    file = 'tests/'
    jsonobj = jsontohtml(file, True, False, '')
    html = jsonobj.json2html()

    assert html
