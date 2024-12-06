from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
load_dotenv()

env = os.getenv('ENV', 'local')

# Select environment based on the ENV environment variable
if env == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif env == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')

elif os.getenv('ENV') == 'ghci':
    print("Running in GitHub CI mode")
    app.config.from_object('config.GithubCIConfig')

db = SQLAlchemy(app)

default_username="admin"
default_password=os.getenv('ADMINPASS')

from iebank_api.models import Account

with app.app_context():
    db.create_all()
CORS(app, supports_credentials=True, expose_headers=["pass", "user", "apass", "auser"])

from iebank_api import routes