## webapp

# Prerequisites to run the app locally
    1.) Install Python 3.9.x
    2.) Install the latest version of MySQL

# Build and Deploy instructions
    1.) Fork the Organization repository in your own namespace.
    2.) Clone the repository using SSH.
    3.) Create a Virtual Environment.
        python3 -m venv venv
    4.) Activate the Virtual Environment.
        for windows:
        venv\Scripts\activate
        for Linux/mac:
        source venv/bin/activate
    5.) Install required dependencies.
        pip install -r requirements.txt
        This command will install essential python libraries and frameworks for the application to work.
        these include Flask, SQLAlchemy, mysqlclient and python-dotenv.
    6.) create a .env file and set the MySQL database URL.
        DATABASE_URL=mysql://<username>:<password>@localhost/<databasename>
    7.) initialize database and run the flask application.
        flask db init
        flask db migrate
        flask db upgrade
        flask run
# Running Tests
    python -m pytest tests/
# Usage
    Once the application is running, you can use it to perform health checks on your application.


