import hashlib
import json

# Define a helper function to hash the config data
def hash_config(config):
    config_str = json.dumps(config, sort_keys=True)
    return hashlib.sha256(config_str.encode()).hexdigest()