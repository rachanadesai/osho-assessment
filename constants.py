# TODO: Change the schema to use pydantic model for data validation
# Define the config schema
CONFIG_SCHEMA = {
    "status": bool,
    "brightness": str,
    "temparature": int
}

REQUEST_PAYLOAD = {
    "device_name": str,
    "config": CONFIG_SCHEMA,
    "timestamp": str
}