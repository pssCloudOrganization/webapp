from flask import Blueprint
from app.controllers.health_check_controller import HealthCheckController
from app.utils.cloudwatch import log_api_call
import app

bp = Blueprint('health', __name__)

@bp.route('/healthz', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@log_api_call
def health_check():
    return HealthCheckController.health_check()

@bp.route('/cicd', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
@log_api_call
def health_check():
    return HealthCheckController.health_check()

@bp.app_errorhandler(404)
@log_api_call
def not_found_handler(status_code):
    return HealthCheckController.not_found()

@bp.app_errorhandler(500)
@log_api_call
def internal_server_err_handler(status_code):
    return HealthCheckController.internal_server_err()
