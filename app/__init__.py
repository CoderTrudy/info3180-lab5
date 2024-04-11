from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect



app = Flask(__name__)
app.config.from_object(Config)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)




if __name__ == '__main__':
    app.run(debug=True)
