


prerequisites
=============
- git installed  
-  >= python3.6  
- pip3 installed  
- venv installed  
- sqlite3 installed  
- influxdb installed


setup
=====
- create virtualenv  
`python3 -m venv path/to/venv/wsys_env`

- activate virtualenv  
`source path/to/venv/wsys_env/bin/activate`

- install dependencies  
`pip3 install -r requirements.txt`

- enable i2c  
`sudo raspi-config`
- InterfaceOptions -> I2C

- create database  
`sqlite3 wsys_db.db`

- create tables  
navigate to <ip-address>/create




- export FLASK_ENV=development  
- export FLASK_APP=wsgi.py  
- flask run --host 0.0.0.0  
  
  
 wiring
 ======
  
 ![wiring](../wiring.png)
