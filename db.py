from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ouwlmxtvewdibl:05f09b74d57c0cf93c2594966a1e03e06c7ba3605d56b46d8ecce6f61da50131@ec2-54-83-192-245.compute-1.amazonaws.com:5432/df3vg11r7cab9s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Bicycles(db.Model):
    __tablename__ = 'Bicycles'
    user_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    num = db.Column(db.String(64))
    time = db.Column(db.TIMESTAMP)
    address = db.Column(db.String(64))
    photo = db.Column(db.String(64))
    city = db.Column(db.String(64))
    detail = db.Column(db.String(64))
    handler = db.Column(db.String(64))
    status = db.Column(db.String(64))
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    updatedate = db.Column(db.TIMESTAMP)
    level = db.Column(db.Integer)
class UserMsg(db.Model):
    __tablename__ = 'UserMsg'
    user_id = db.Column(db.String(64), primary_key=True)
    user_msg = db.Column(db.String(64))
    
if __name__ == '__main__':
    manager.run()
