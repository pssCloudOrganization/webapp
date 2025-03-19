from app import db
import uuid
from datetime import datetime, timezone

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    full_url = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.Date, default=datetime.now(timezone.utc).date)
    content_type = db.Column(db.String(100))
    file_size = db.Column(db.Integer)
    etag = db.Column(db.String(255))
    