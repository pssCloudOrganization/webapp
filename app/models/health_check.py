from app import db
from datetime import datetime, timezone

class HealthCheck(db.Model):
    __tablename__ = 'health_check_logs'
    check_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    datetime = db.Column(db.DateTime, default=datetime.now(timezone.utc))
