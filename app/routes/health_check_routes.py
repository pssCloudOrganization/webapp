from flask import Blueprint
from app.controllers.health_check_controller import HealthCheckController
import app

bp = Blueprint('health', __name__)

@bp.route('/healthz', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def health_check():
    return HealthCheckController.health_check()
