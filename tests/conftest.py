import os
import tempfile
from flask_app import app as flask_app
import pytest


@pytest.fixture
def app():
    with flask_app.app_context():
        flask_app.config['WTF_CSRF_ENABLED'] = False
        flask_app.config['SECRET_KEY'] = 'supersecretkey'
        yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()
