from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import Config, TestConfig

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    if config_class.TESTING:
        config_class = TestConfig

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import health_check_routes, file_routes
    app.register_blueprint(health_check_routes.bp)
    app.register_blueprint(file_routes.bp)
    
    with app.app_context():
        db.create_all()
        
    return app
