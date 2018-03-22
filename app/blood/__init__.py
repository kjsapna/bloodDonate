from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:@127.0.0.1/db_sahayog'
app.secret_key = 'SaHaYogSem-7'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'sahayog.project@gmail.com'
app.config['MAIL_PASSWORD'] = 'sahayogadmin123'
mail = Mail(app)
db.init_app(app)


import blood.routes
