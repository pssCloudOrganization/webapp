from app import db
from app.models.health_check import HealthCheck

class HealthCheckService:
    @staticmethod
    def perform_health_check():
        try:
            health_check = HealthCheck()
            db.session.add(health_check)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
