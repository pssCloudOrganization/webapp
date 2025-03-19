import boto3
import os
import uuid
from datetime import datetime
from app import db
from app.models.file import File

class FileService:
    @staticmethod
    def upload_file(file_obj):
        try:
            # Initialize S3 client
            s3 = boto3.client('s3')
            bucket_name = os.environ.get('S3_BUCKET_NAME')
            aws_region = os.environ.get('AWS_REGION')
            
            # Generate a unique file_id
            file_id = str(uuid.uuid4())
            
            # Get file extension
            file_extension = os.path.splitext(file_obj.filename)[1]
            
            # Create S3 key (path)
            s3_key = f"{file_id}{file_extension}"
            
            # Upload file to S3
            s3.upload_fileobj(file_obj, bucket_name, s3_key, ExtraArgs={'ContentType': file_obj.content_type})
            
            # Create file record in database
            response = s3.head_object(Bucket=bucket_name, Key=s3_key)
            file_record = File(
                id=file_id,
                file_name=file_obj.filename,
                url=f"{bucket_name}/{s3_key}",
                full_url=f"https://{bucket_name}.s3.{aws_region}.amazonaws.com/{s3_key}",
                content_type=response.get('ContentType'),
                file_size=response.get('ContentLength'),
                etag=response.get('ETag')
            )

            print("debug here")
            print("file_id", file_id)
            print("file_url", file_record.url)
            print("file_record", file_record)
            print("content_type", response.get('ContentType'))
            print("content_size", response.get('ContentLength'))
            print("etag", response.get('ETag').strip('"'))
            
            db.session.add(file_record)
            db.session.commit()
            
            # Return file metadata
            return {
                "file_name": file_record.file_name,
                "id": file_record.id,
                "url": file_record.url,
                "upload_date": file_record.upload_date.isoformat()
            }
        except Exception as e:
            db.session.rollback()
            print(f"Error uploading file: {str(e)}")
            return None
    
    @staticmethod
    def get_file(file_id):
        try:
            file_record = db.session.get(File, file_id)
            if not file_record:
                return None
            
            return {
                "file_name": file_record.file_name,
                "id": file_record.id,
                "url": file_record.url,
                "upload_date": file_record.upload_date.isoformat()
            }
        except Exception as e:
            print(f"Error retrieving file: {str(e)}")
            return None
    
    @staticmethod
    def delete_file(file_id):
        try:
            file_record = db.session.get(File, file_id)
            if not file_record:
                return False
            
            # Delete from S3
            s3 = boto3.client('s3')
            bucket_name = os.environ.get('S3_BUCKET_NAME')
            
            # Extract the S3 key from the URL
            s3_key = file_record.url.replace(f"{bucket_name}/", "")
            
            # Delete from S3
            s3.delete_object(Bucket=bucket_name, Key=s3_key)
            
            # Delete from database
            db.session.delete(file_record)
            db.session.commit()
            
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting file: {str(e)}")
            return False
