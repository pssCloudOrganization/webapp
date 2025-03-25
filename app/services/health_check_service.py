# from app import db
# from app.models.health_check import HealthCheck

# class HealthCheckService:
#     @staticmethod
#     def perform_health_check():
#         try:
#             health_check = HealthCheck()
#             db.session.add(health_check)
#             db.session.commit()
#             return True
#         except Exception as e:
#             db.session.rollback()
#             return False

# app/services/health_check_service.py
from app import db
from app.models.health_check import HealthCheck
from app.utils.cloudwatch import time_database_query, logger

class HealthCheckService:
    @staticmethod
    def perform_health_check():
        try:
            logger.info("Performing health check")
            
            @time_database_query
            def create_health_check():
                health_check = HealthCheck()
                db.session.add(health_check)
                db.session.commit()
            
            create_health_check()
            logger.info("Health check completed successfully")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Health check failed: {str(e)}")
            return False
