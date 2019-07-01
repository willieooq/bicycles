from db import *
import datetime

class bicycles(db.Model):
    __tablename__ = 'bicycles'

    def __init__(self, UserId="N/A", Name="未填", Num='0000000000',Time=datetime.datetime.now(),Address='N/A',Photo='N/A',City='N/A',Detail='N/A',Handler='not',Status='N/A',Score='0',Updatedate=datetime.datetime.now()):
        
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
