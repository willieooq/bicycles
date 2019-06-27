from db import *


class PictureDate(db.Model):
    __tablename__ = 'Bicycles'

    def __init__(self, UserId, Name, Num,Time,Address,Photo,City,Detail,Handler,Status,Score,Updatedate):
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
