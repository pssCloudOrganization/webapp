from flask import Response, request, jsonify, make_response
from app.services.health_check_service import HealthCheckService

class HealthCheckController:
    @staticmethod
    def health_check():
        if request.method != 'GET':
            return HealthCheckController.method_not_allowed()

        if request.data or request.args or request.content_type:
            return HealthCheckController.bad_request()
        
        result = HealthCheckService.perform_health_check()
        status_code = 200 if result else 504
        
        return HealthCheckController.create_response(status_code)
    

    #helper functions from here
    @staticmethod
    def method_not_allowed():
        return HealthCheckController.create_response(405)
    
    @staticmethod
    def not_found():
        return HealthCheckController.create_response(404)
    
    @staticmethod
    def bad_request():
        return HealthCheckController.create_response(400)

    @staticmethod
    def internal_server_err():
        return HealthCheckController.create_response(500)
    
    @staticmethod
    def create_response(status_code):
        response = Response(status=status_code)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        return response
