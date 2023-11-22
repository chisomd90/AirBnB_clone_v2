#!/usr/bin/python3
'''New engine DBStorage
'''
from os import getenv
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class DBStorage():
    '''a storage class'''
    __engine = None
    __session = None
    def __init__(self):
        '''class constructor'''
        db_user = getenv('HBNB_MYSQL_USER')
        db_pass = getenv('HBNB_MYSQL_PWD')
        db_name = getenv('HBNB_MYSQL_DB')
        db_host = getenv('HBNB_MYSQL_HOST')
        db_env = getenv('HBNB_ENV')
        url_ = 'mysql+mysqldb://{}:{}@{}:3306/{}'
        url = url_.format(db_user, db_pass, db_host, db_name)
        self.__engine = create_engine(url, pool_pre_ping=True)
        # Base.metadata.create_all(self.__engine)
        # self.__session = Session(self.__engine)
        
        if db_env == 'test':
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        '''all method'''
        dict_ = {}
        # all_class = [User, Place, State, City, Amenity, Review]
        all_class = [State, City, User]
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dict_[key] = obj
        else:
            for cls_ in all_class:
                objs = self.__session.query(cls_).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dict_[key] = obj

        return(dict_)

    def new(self, obj):
        '''new objectt'''
        self.__session.add(obj)

    def save(self):
        '''commit changes'''
        self.__session.commit()


    def delete(self, obj=None):
        '''delete obj frm session'''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''reload'''
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(
                sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session
