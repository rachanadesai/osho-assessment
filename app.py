from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
import os
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello Osho</h2>'

# connect to Postgresql Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# Database Model for generic IoT device
class Devices(db.Model):
  __tablename__ = 'devices'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  device_id = db.Column(db.Integer, nullable=False)
  config = db.Column(JSON)

  created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
  updated_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           onupdate=func.now())

  def __init__(self, device_id, config):
    self.device_id = device_id
    self.config = config

 
db.create_all()


if __name__ == "__main__":
    app.run(debug=True)