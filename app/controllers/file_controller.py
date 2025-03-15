from flask import Response, request, jsonify
from app.services.file_service import FileService
import uuid

class FileController:
    @staticmethod
    def add_file():
        if request.method != 'POST':
            return FileController.method_not_allowed()
        
        if 'profilePic' not in request.files:
            return FileController.bad_request()
        
        file = request.files['profilePic']
        if file.filename == '':
            return FileController.bad_request()
        
        # Check if the file extension is allowed
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            return FileController.bad_request()
        
        result = FileService.upload_file(file)
        if not result:
            return FileController.internal_server_err()
        
        return jsonify(result), 201

    
    @staticmethod
    def get_file():
        if request.method != 'GET':
            return FileController.method_not_allowed()
        
        file_id = request.args.get('id')
        if not file_id:
            return FileController.bad_request()
        
        result = FileService.get_file(file_id)
        if not result:
            return FileController.not_found()
        
        return jsonify(result), 200
    
    @staticmethod
    def delete_file():
        if request.method != 'DELETE':
            return FileController.method_not_allowed()
        
        file_id = request.args.get('id')
        if not file_id:
            return FileController.bad_request()
        
        result = FileService.delete_file(file_id)
        if not result:
            return FileController.not_found()
        
        return '', 204
    
    # Helper functions from here
    @staticmethod
    def method_not_allowed():
        return FileController.create_response(405)
    
    @staticmethod
    def not_found():
        return FileController.create_response(404)
    
    @staticmethod
    def bad_request():
        return FileController.create_response(400)
    
    @staticmethod
    def unauthorized():
        return FileController.create_response(401)

    @staticmethod
    def internal_server_err():
        return FileController.create_response(500)
    
    @staticmethod
    def create_response(status_code):
        response = Response(status=status_code)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
