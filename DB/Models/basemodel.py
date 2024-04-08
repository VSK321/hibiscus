from peewee import *
from AppLoc import AppModels

appmodels = AppModels()

db = SqliteDatabase('rose_base.db')

class BaseModel(Model):
    class Meta:
        database = db