from .basemodel import *
from peewee import *

@appmodels.register()
class User(BaseModel):
    username = CharField(unique=True)
    followers = ForeignKeyField("self", backref='following')