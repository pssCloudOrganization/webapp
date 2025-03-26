sudo groupadd csye6225
sudo useradd csye6225 --shell /usr/sbin/nologin -g csye6225
sudo mv /tmp/csye6225.service /etc/systemd/system/
sudo mkdir -p /opt/csye6225/webapp


sudo mkdir -p /var/log/webapp/
# sudo touch csye6225.log
sudo mv /tmp/cloudwatch-config.json /opt/
sudo wget https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
# sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/cloudwatch-config.json -s
# sudo systemctl enable amazon-cloudwatch-agent
# sudo systemctl restart amazon-cloudwatch-agent



sudo mv /tmp/webapp.zip /opt/csye6225/
sudo unzip -o /opt/csye6225/webapp.zip -d /opt/csye6225/webapp
sudo rm /opt/csye6225/webapp.zip
sudo chown -R csye6225:csye6225 /opt/csye6225
sudo chmod -R 755 /opt/csye6225

# sudo mv /tmp/.env /opt/csye6225/webapp/.env
# sudo chown csye6225:csye6225 /opt/csye6225/webapp/.env

cd /opt/csye6225/webapp
sudo -u csye6225 python3 -m venv venv
sudo -u csye6225 bash -c "source venv/bin/activate && pip install -r requirements.txt"

sudo systemctl daemon-reload
sudo systemctl enable csye6225
# sudo systemctl start csye6225
