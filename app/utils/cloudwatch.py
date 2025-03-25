import logging
import time
import statsd
import traceback
from functools import wraps
from flask import request, g
from datetime import datetime, timezone
# import app
# Configure logging with UTC time
logger = logging.getLogger('webapp')
logger.setLevel(logging.INFO)

handler = logging.FileHandler('/var/log/webapp/csye6225.log')
formatter = logging.Formatter('%(asctime)s UTC - %(name)s - %(levelname)s - %(message)s', 
                             '%Y-%m-%d %H:%M:%S')
# Set the timezone to UTC for the formatter
formatter.converter = lambda *args: datetime.now(timezone.utc).timetuple()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Configure StatsD client
statsd_client = statsd.StatsClient('localhost', 8125, prefix='webapp')

def log_api_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print(app.Log_file_path)
        endpoint = request.endpoint
        method = request.method
        
        # Log API call
        logger.info(f"API call received: {method} {request.path}")
        
        # Increment API counter
        metric_name = f"api.{endpoint}.{method.lower()}"
        statsd_client.incr(metric_name)
        
        # Measure API execution time
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Record API timing
            statsd_client.timing(f"{metric_name}.time", execution_time)
            logger.info(f"API call completed: {method} {request.path} in {execution_time:.2f}ms")
            
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            
            # Log exception with stack trace
            logger.error(f"Error in API call {method} {request.path}: {str(e)}")
            logger.error(traceback.format_exc())
            
            # Still record timing even for failed calls
            statsd_client.timing(f"{metric_name}.time", execution_time)
            
            # Re-raise the exception
            raise
    
    return wrapper

def time_database_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Record DB query timing
            statsd_client.timing("db.query.time", execution_time)
            logger.debug(f"Database query executed in {execution_time:.2f}ms")
            
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            
            # Still record timing even for failed queries
            statsd_client.timing("db.query.time", execution_time)
            logger.error(f"Database query error: {str(e)}")
            
            # Re-raise the exception
            raise
    
    return wrapper

def time_s3_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            # Record S3 operation timing
            statsd_client.timing("s3.operation.time", execution_time)
            logger.debug(f"S3 operation executed in {execution_time:.2f}ms")
            
            return result
        except Exception as e:
            end_time = time.time()
            execution_time = (end_time - start_time) * 1000
            
            # Still record timing even for failed operations
            statsd_client.timing("s3.operation.time", execution_time)
            logger.error(f"S3 operation error: {str(e)}")
            
            # Re-raise the exception
            raise
    
    return wrapper