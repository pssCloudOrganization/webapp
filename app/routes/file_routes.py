from flask import Blueprint
from app.controllers.file_controller import FileController

bp = Blueprint('file', __name__, url_prefix='/v1')

@bp.route('/file', methods=['POST', 'PUT', 'OPTIONS', 'HEAD'])
def add_file():
    return FileController.add_file()

@bp.route('/file', methods=['GET'])
def get_file():
    return FileController.get_file()

@bp.route('/file', methods=['DELETE'])
def delete_file():
    return FileController.delete_file()

@bp.app_errorhandler(404)
def not_found_handler(status_code):
    return FileController.not_found()
