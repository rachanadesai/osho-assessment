# TODO: Change the schema to use pydantic model for data validation
# Define the config schema
CONFIG_SCHEMA = {
    "status": bool,  # True: ON, False: OFF
    "brightness": str,
    "temparature": int
}

REQUEST_PAYLOAD = {
    "device_name": str,  # TODO: Use ENUM, so we accept only valid device names
    "config": CONFIG_SCHEMA
}