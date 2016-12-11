#!/bin/sh
sudo apt-get -y update
sudo apt-get install -y python-psycopg2
sudo apt-get install python-dev 
sudo service postgresql status
if [ "$?" -gt "0" ]; then
  echo "Not installed".
  sudo apt-get install libpq-dev
  sudo apt-get --assume-yes update
  sudo apt-get --assume-yes install postgresql postgresql-contrib
else
  echo "Intalled"
fi

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get install -y mongodb-org
mongo --eval "use customers_certs"
mongo --eval "db.addUser({user:"mongodb",pwd:"password",roles:["readWrite"]});"
sudo -u postgres psql -d template1 "alter user postgres with password 'password'"
sudo -u postgres psql -d postgres -c "create table customers(id serial,customer_name varchar(200),customer_email varchar(255),password varchar(300))"
sudo apt-get install python-virtualenv
virtualenv cloudflare
cd cloudflare
source bin/activate
pip install flask
pip install flask-sqlalchemy
pip install subprocess32
pip install pymongo
