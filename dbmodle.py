from db import *
import datetime

class UserData(db.Model):
    __tablename__ = 'userdata'

    def __init__(self, user_id = "N/A", name = "未填", num = "未填", score = '0' ,\
         total = '0', level = '0', user_msg = 'no'):

        self.user_id = user_id
        self.name = name
        self.num = num
        self.score = score
        self.total = total
        self.level = level
        self.user_msg = user_msg
        
class Bicycles(db.Model):
    __tablename__ = 'bicycles'

    def __init__(self, user_id="N/A",time = datetime.datetime.now(),address = "未填",\
        photo='N/A',city="未填",detail='no',handler='none',status='not yet',updatedate=datetime.datetime.now()):
        
        self.user_id = user_id
        self.time = time
        self.address = address
        self.photo = photo
        self.city = city
        self.detail = detail
        self.handler = handler
        self.status = status
        self.updatedate = updatedate
