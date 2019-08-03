from db import *
import datetime

class Bicycles(db.Model):
    __tablename__ = 'Bicycles'

    def __init__(self, user_id="N/A", name="未填", num="未填",time=datetime.datetime.now(),address='N/A',photo='N/A',city='N/A',detail=' ',handler='none',status='not yet',score='0',total='0',updatedate=datetime.datetime.now(),level='0'):
        
        self.user_id = user_id
        self.name = name
        self.num = num
        self.time = time
        self.address = address
        self.photo = photo
        self.city = city
        self.detail = detail
        self.handler = handler
        self.status = status
        self.score = score
        self.total = total
        self.updatedate = updatedate
        self.level = level

class UserMsg(db.Model):
    __tablename__ = 'UserMsg'

    def __init__(self, user_id="N/A", user_msg = 'no'):

        self.user_id = user_id
        self.user_msg = user_msg
