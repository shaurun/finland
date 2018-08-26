# Create your models here.
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Model

from FinLand.mongo import MongoDBClient

client = MongoDBClient('mongodb://heroku_4nzjwz0z:dcvtdbro5ppqqahpdrc8m83lcl@ds131902.mlab.com/heroku_4nzjwz0z', 31902)
client.connect('heroku_4nzjwz0z')

class ReturnMatrix(Model):
    pass



"""
class User(AbstractBaseUser):
    _collection = "users"

    _username = "name"
    _password = "password"
    _email = "email"
    _id = "_id"

    id = None
    username = None
    password = None
    email = None
    is_active = True

    REQUIRED_FIELDS = []

    def __init__(self, dbUser):
        self.id = dbUser[self._id]
        self.username = dbUser[self._username]
        self.password = dbUser[self._password]
        #self.email = dbUser[self._email] or None

    def get_username(self):
        "Return the identifying username for this User"
        return self.username;

    def clean(self):
        pass

    @classmethod
    def get(cls, username, password):
        dbUser = client.find_document(cls._collection, {cls._username: username, cls._password: password})
        return User(dbUser)

    @classmethod
    def create(cls, username, password):
        client.insert_document(cls._collection, {cls._username: username, cls._password: password})
        dbUser = client.find_document(cls._collection, {cls._username: username, cls._password: password})
        return User(dbUser)

    def __str__(self):
        return self.username;
"""


#class UserManager(BaseUserManager):
    #""""
        #Handles user creation using mongo db
    #"""
    #def create_user(self, username, password):
       # """
        #Creates and saves a User with the given username and password.
        #"""
        #return User.create(username, password)

