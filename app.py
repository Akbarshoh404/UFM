from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes after app and db initialization to avoid circular imports
from routes.user_routes import *
from routes.project_routes import *
from routes.proposal_routes import *
from routes.contract_routes import *
from routes.payment_routes import *
from routes.message_routes import *

if __name__ == "__app__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))