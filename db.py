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

class UserData(db.Model):
    __tablename__ = 'userdata'
    user_id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64))
    num = db.Column(db.String(64))
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    level = db.Column(db.Integer)
    user_msg = db.Column(db.String(64))
    # bicycles = db.relationship("Bicycles", back_populates="userdata")

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
    # userdata = db.relationship("UserData", back_populates="bicycles")

# test = Bicycles.query.filter(Bicycles.user_id == '666').first()
# print('city',test.city)
# print('name',test.userdata.name)

if __name__ == '__main__':
    manager.run()
