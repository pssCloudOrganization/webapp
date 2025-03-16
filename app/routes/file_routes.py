from flask import Blueprint
from app.controllers.file_controller import FileController

bp = Blueprint('file', __name__, url_prefix='/v1')

@bp.route('/file', methods=['POST', 'PUT', 'OPTIONS', 'HEAD'])
def add_file():
    return FileController.add_file()

@bp.route('/file/<string:file_id>', methods=['GET'])
def get_file(file_id):
    return FileController.get_file(file_id)

@bp.route('/file/<string:file_id>', methods=['DELETE'])
def delete_file(file_id):
    return FileController.delete_file(file_id)

@bp.app_errorhandler(404)
def not_found_handler(status_code):
    return FileController.not_found()
@bp.app_errorhandler(405)
def internal_server_err_handler(status_code):
    return FileController.bad_request()

@bp.after_request
def add_security_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response
