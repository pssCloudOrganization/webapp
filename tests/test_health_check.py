import pytest
from flask.testing import FlaskClient
from app import create_app, db
from app.models.health_check import HealthCheck
from app.services.health_check_service import HealthCheckService
from config.config import TestConfig
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
    
    drop_database(engine.url)

@pytest.fixture(autouse=True)
def db_session(app):
    with app.app_context():
        db.session.begin_nested()
        yield db.session
        db.session.rollback()

@pytest.fixture
def client(app):
    return app.test_client()



def test_get_health_check(client: FlaskClient):
    # Test a successful GET request
    response = client.get('/healthz')
    assert response.status_code == 200
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_post_health_check(client: FlaskClient):
    # Test that POST requests are not allowed
    response = client.post('/healthz')
    assert response.status_code == 405
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_put_health_check(client: FlaskClient):
    # Test that PUT requests are not allowed
    response = client.put('/healthz')
    assert response.status_code == 405
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_delete_health_check(client: FlaskClient):
    # Test that DELETE requests are not allowed
    response = client.delete('/healthz')
    assert response.status_code == 405
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_patch_health_check(client: FlaskClient):
    # Test that PATCH requests are not allowed
    response = client.patch('/healthz')
    assert response.status_code == 405
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_get_health_check_with_payload(client: FlaskClient):
    # Test that GET requests with a payload return 400
    response = client.get('/healthz', data='payload')
    assert response.status_code == 400
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_get_health_check_with_args(client: FlaskClient):
    # Test that GET requests with a payload return 400
    response = client.get('/healthz?name=hello')
    assert response.status_code == 400
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_database_connection(client: FlaskClient):
    # Test database connection by checking if a record is inserted
    response = client.get('/healthz')
    assert response.status_code == 200
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'


def test_database_insert_failure(client: FlaskClient, monkeypatch):
    # Simulate a database insert failure
    def mock_perform_health_check():
        return False

    monkeypatch.setattr(HealthCheckService, 'perform_health_check', mock_perform_health_check)
    response = client.get('/healthz')
    assert response.status_code == 503
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'

def test_internal_server_error(client: FlaskClient, monkeypatch):
    # Simulate an unexpected exception during health check
    def mock_perform_health_check():
        raise Exception("Simulated internal server error")

    monkeypatch.setattr(HealthCheckService, 'perform_health_check', mock_perform_health_check)
    
    response = client.get('/healthz')
    assert response.status_code == 500
    assert 'Cache-Control' in response.headers and response.headers['Cache-Control'] == 'no-cache, no-store, must-revalidate'
