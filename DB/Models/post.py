from .basemodel import *
from .user import User
from peewee import *
import datetime

@appmodels.register()
class Post(BaseModel):
    user = ForeignKeyField(User, backref='posts')
    message = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)
    is_published = BooleanField(default=True)