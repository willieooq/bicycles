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


class PictureDate(db.Model):
    __tablename__ = 'Bicycles'

    UserId = db.Column(db.Integer, primary_key=True)
#    Userid = db.Column(db.Integer, unique=True)
    Name = db.Column(db.String(64))
    Num = db.Column(db.Integer)
    Time = db.Column(db.TIMESTAMP)
    Address = db.Column(db.String(64))
    Photo = db.Column(db.String(64))
    City = db.Column(db.String(64))
    Detail = db.Column(db.String(64))
    Handler = db.Column(db.String(64))
    Status = db.Column(db.String(64))
    Score = db.Column(db.Integer)
    Updatedate =db.Column(db.TIMESTAMP)
        
##insert_data = PictureDate(Uuid='w', Title='t', Description='f')
##db.session.add(insert_data)
##db.session.commit()
##print("DONE")
if __name__ == '__main__':
    manager.run()
