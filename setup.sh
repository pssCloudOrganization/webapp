#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status

# Prompt for required information
read -p "Enter the name of the zip file (without .zip extension): " PROJECT_NAME
read -p "Enter MySQL username for application: " MYSQL_USER
read -s -p "Enter MySQL password for application: " MYSQL_PASSWORD
echo

# Define variables
ZIP_FILE="$PROJECT_NAME.zip"
DB_NAME="health"
APP_GROUP="appgroup"
APP_USER="appuser"
APP_DIR="/opt/csye6225"

# Function to set up swap memory
setup_swap() {
    echo "Setting up swap memory..."
    if ! sudo swapon --show | grep -q swapfile; then
        sudo fallocate -l 1G /swapfile
        sudo chmod 600 /swapfile
        sudo mkswap /swapfile
        sudo swapon /swapfile
        echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    else
        echo "Swap memory already configured."
    fi
}

echo "Starting setup..."

# 1. Configure swap before doing anything
setup_swap

# 2. Install dependencies
echo "Updating system and installing dependencies..."
sudo apt update 
sudo apt -y upgrade 
sudo apt install -y unzip python3-pip python3.12-venv pkg-config libmysqlclient-dev mysql-server

# 3. Install MySQL and configure the database
echo "Installing and configuring MySQL..."
sudo systemctl restart mysql

# Use debian-sys-maint credentials to configure MySQL
sudo mysql --defaults-file=/etc/mysql/debian.cnf <<EOF
-- Check and remove existing application user if needed
DROP USER IF EXISTS '${MYSQL_USER}'@'localhost';
FLUSH PRIVILEGES;

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS ${DB_NAME};

-- Create dedicated application user
CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}';

GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${MYSQL_USER}'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

GRANT ALL PRIVILEGES ON test_${DB_NAME}.* TO '${MYSQL_USER}'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

EOF

# 4. Create Linux group and user for the application
echo "Creating Linux group and user..."
sudo groupadd -f "$APP_GROUP"
if id "$APP_USER" &>/dev/null; then
    echo "User $APP_USER already exists"
else
    sudo useradd -g "$APP_GROUP" -m -d "$APP_DIR" "$APP_USER"
fi

# 5. Transfer and extract project files directly into /opt/csye6225
echo "Extracting project files directly to $APP_DIR..."
if [ ! -f "$ZIP_FILE" ]; then
    echo "Error: Zip file '$ZIP_FILE' not found!"
    exit 1
fi
sudo unzip -o "$ZIP_FILE" -d "$APP_DIR"

# 6. Set up application directory and permissions
echo "Setting up application directory and permissions..."
sudo chown -R $APP_USER:$APP_GROUP $APP_DIR
sudo chmod -R 755 $APP_DIR

# 7. Navigate to the updated webapp folder
WEBAPP_DIR="$APP_DIR/$PROJECT_NAME/webapp"
cd "$WEBAPP_DIR"

# 8. Set up virtual environment
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# 9. Update .env file with application credentials
echo "Updating .env file with database credentials..."
cat <<EOL > ".env"
DATABASE_URL=mysql://$MYSQL_USER:$MYSQL_PASSWORD@localhost/$DB_NAME
TEST_DATABASE_URL=mysql://$MYSQL_USER:$MYSQL_PASSWORD@localhost/test_$DB_NAME
EOL

# 10. Install project dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 11. Initialize Flask DB
echo "Setting up Flask database..."
flask db init || echo "Flask DB already initialized."
flask db migrate -m "Initial migration" || echo "Migration step skipped (if already done)."
flask db upgrade
``
# 12. Run Flask application as appuser
echo "Starting Flask app..."
sudo -u $APP_USER bash -c "source $WEBAPP_DIR/venv/bin/activate && flask run --host=0.0.0.0 --port=5000"


echo "Setup complete!"
