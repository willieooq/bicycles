from db import *
import datetime

class Bicycles(db.Model):
    __tablename__ = 'Bicycles'

    def __init__(self, UserId='NA', Name='NA', Num='0000000000',Time=datetime.datetime.now(),Address='NA',Photo='NA',City='NA',Detail='NA',Handler='not',Status='NA',Score='0',Updatedate=datetime.datetime.now()):
        
        self.UserId = UserId
        self.Name = Name
        self.Num = Num
        self.Time = Time
        self.Address = Address
        self.Photo = Photo
        self.City = City
        self.Detail = Detail
        self.Handler = Handler
        self.Status = Status
        self.Score = Score
        self.Updatedate = Updatedate
