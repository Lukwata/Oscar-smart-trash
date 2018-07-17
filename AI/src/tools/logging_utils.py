"""Utility for logging."""
import os
import logging
import logging.config
import json


def setup_logging(default_path='logging.json', default_level=logging.INFO,
                  env_key='LOG_CFG', filename=None):
    """Setup logging configuration"""
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    current_path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_path, path)
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)

        if filename is None:
            filename = config['handlers']['file_handler']['filename']
        filename = os.path.join(current_path, filename)
        if os.path.exists(filename):
            f = open(filename, 'w')
            f.close()
        config['handlers']['file_handler']['filename'] = filename

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
