import pytest
from flask.testing import FlaskClient
from app import create_app, db
from app.models.file import File
from app.services.file_service import FileService
from config.config import TestConfig
import uuid
import json
import io
from unittest.mock import patch, MagicMock
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

@pytest.fixture(scope='session')
def app():
    # Create the test database
    engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URI)
    if not database_exists(engine.url):
        create_database(engine.url)

    app = create_app(config_class=TestConfig)
    
    with app.app_context():
        db.create_all()

    yield app

    # Drop the test database after all tests
    with app.app_context():
        db.session.remove()
        db.drop_all()
    
    # drop_database(engine.url)
    try:
        drop_database(engine.url)
    except Exception as e:
        print(f"Warning: Could not drop database: {e}")

@pytest.fixture(autouse=True)
def db_session(app):
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_s3():
    with patch('boto3.client') as mock_client:
        s3_mock = MagicMock()
        mock_client.return_value = s3_mock
        yield s3_mock

def test_add_file(client: FlaskClient, mock_s3):
    # Create a mock file
    file_data = io.BytesIO(b'test file content')
    
    # Test successful file upload
    response = client.post(
        '/v1/file',
        data={'profilePic': (file_data, 'test.jpg')},
        content_type='multipart/form-data'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'file_name' in data
    assert 'id' in data
    assert 'url' in data
    assert 'upload_date' in data
    
    # Test missing file
    response = client.post('/v1/file')
    assert response.status_code == 400

def test_get_file(client: FlaskClient):
    # Create a test file record
    file_id = str(uuid.uuid4())
    file = File(
        id=file_id,
        file_name='test.jpg',
        url='test-bucket/test.jpg'
    )
    db.session.add(file)
    db.session.commit()
    
    # Test successful file retrieval
    response = client.get(f'/v1/file/{file_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == file_id
    
    # Test file not found
    response = client.get('/v1/file/nonexistent-id')
    assert response.status_code == 404
    
    # Test missing id parameter
    response = client.get('/v1/file')
    assert response.status_code == 400

def test_delete_file(client: FlaskClient, mock_s3):
    # Create a test file record
    file_id = str(uuid.uuid4())
    file = File(
        id=file_id,
        file_name='test.jpg',
        url='test-bucket/test.jpg'
    )
    db.session.add(file)
    db.session.commit()
    
    # Test successful file deletion
    response = client.delete(f'/v1/file/{file_id}')
    assert response.status_code == 204
    
    # Test file not found
    response = client.delete('/v1/file/nonexistent-id')
    assert response.status_code == 404
    
    # Test missing id parameter
    response = client.delete('/v1/file')
    assert response.status_code == 400
