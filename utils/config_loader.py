import json
import os
from .constants import CONFIG_PATH

def load_domain_config():
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"⚠️ Error loading config: {e}")
        return {}

def get_domain_config(domain_key, domain_config):
    try:
        for key in domain_config.keys():
            from .helpers import normalize_domain
            if normalize_domain(key) == domain_key:
                return domain_config[key]
        return {}
    except Exception as e:
        print(f"⚠️ Error fetching domain config: {e}")
        return {}
