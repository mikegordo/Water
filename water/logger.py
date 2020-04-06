from logging.config import dictConfig

from flask import Flask

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'log/water.log'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'file']
    }
})

app = Flask(__name__)
