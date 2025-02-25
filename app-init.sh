sudo groupadd csye6225
sudo useradd csye6225 --shell /usr/sbin/nologin -g csye6225
sudo mv /tmp/csye6225.service /etc/systemd/system/
sudo mkdir -p /opt/csye6225/webapp

sudo mv /tmp/webapp.zip /opt/csye6225/
sudo unzip -o /opt/csye6225/webapp.zip -d /opt/csye6225/webapp
sudo rm /opt/csye6225/webapp.zip
sudo chown -R csye6225:csye6225 /opt/csye6225
sudo chmod -R 755 /opt/csye6225

sudo mv /tmp/.env /opt/csye6225/webapp/.env
sudo chown csye6225:csye6225 /opt/csye6225/webapp/.env

cd /opt/csye6225/webapp
sudo -u csye6225 python3 -m venv venv
sudo -u csye6225 bash -c "source venv/bin/activate && pip install -r requirements.txt"

sudo systemctl daemon-reload
sudo systemctl enable csye6225
# sudo systemctl start csye6225
