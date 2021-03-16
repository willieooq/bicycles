from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI;
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class UserData(db.Model):
    __tablename__ = 'userdata'
    user_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    num = db.Column(db.String(64))
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    level = db.Column(db.Integer)
    user_msg = db.Column(db.String(64))

class Bicycles(db.Model):
    __tablename__ = 'bicycles'
    ID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64),db.ForeignKey('userdata.user_id'))
    time = db.Column(db.TIMESTAMP)
    address = db.Column(db.String(64))
    photo = db.Column(db.String(64))
    city = db.Column(db.String(64))
    detail = db.Column(db.String(64))
    handler = db.Column(db.String(64))
    status = db.Column(db.String(64))
    updatedate = db.Column(db.TIMESTAMP)

if __name__ == '__main__':
    manager.run()
