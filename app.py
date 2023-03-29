from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from sqlalchemy import desc
from constants import REQUEST_PAYLOAD
from utils import hash_config
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello Osho</h2>'

print("------ In OSHO ---------");

# connect to Postgresql Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# TODO: Create separate file for DB Models
# Database Model for generic IoT device
class Devices(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    device_id = db.Column(db.Integer, nullable=False)
    device_name = db.Column(db.String)
    config = db.Column(JSON)
    config_hash = db.Column(db.String, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True),
                            server_default=func.now(),
                            onupdate=func.now())

    def __init__(self, device_id, device_name, config, config_hash):
        self.device_id = device_id
        self.device_name = device_name
        self.config = config
        self.config_hash = config_hash

    # convert to dict
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

 
db.create_all()

# TODO: apply authorisation (oauth2 or basic auth)
# GET endpoint that retrieves the current config and a number of previous config
@app.route('/api/devices/<device_id>', methods=['GET'])
def get_device_by_id(device_id):
    devices_configs = []
    devices = db.session.query(Devices).filter_by(device_id=device_id).order_by(desc(Devices.updated_at)).all()
    if not devices:
        # TODO: Improve error handlimg
        return jsonify({"message": "Invalid device Id"}), 404
    for device in devices:
        devices_configs.append(device.as_dict())
    return jsonify(devices_configs)

# TODO: apply authorisation (oauth2 or basic auth)
# TODO: Improve request data validation
# POST endpoint that adds the stored config if it does not exists
@app.route('/api/devices/<device_id>', methods=['POST'])
def update_device_by_id(device_id):
    # Get the request data
    data = request.get_json()

    # Validate the request data
    if not all(key in data for key in REQUEST_PAYLOAD.keys()):
        # TODO: Improve error handling, and status codes
        return jsonify({"message": "Invalid request data"}), 400
    
    # Hash the config data
    config_hash = hash_config(data['config'])

    # Find the most recent config for the device
    recent_config = db.session.query(Devices).filter(Devices.device_id==device_id).order_by(desc(Devices.created_at)).first()
    
    # Check if the config data already exists in the database
    if recent_config and recent_config.config_hash == config_hash:
        return jsonify({'message': 'Device config already exists.'}), 400
    
    # Insert the new config into the database
    _add = Devices(device_id, data['device_name'], data['config'], config_hash)
    db.session.add(_add)
    db.session.commit()

    new_config = db.session.query(Devices).filter(Devices.id == _add.id).one()
    return jsonify(new_config.as_dict()), 200


if __name__ == "__main__":
    app.run(debug=True)