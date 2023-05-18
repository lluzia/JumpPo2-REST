import os
import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'jumppo.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
SQLALCHEMY_DATABASE_URI = "postgresql://localhost/jumpopo_postgres"

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

SECRET = os.urandom(32)
