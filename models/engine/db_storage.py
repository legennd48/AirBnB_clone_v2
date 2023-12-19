#!/usr/bin/python3
'''
New DB storage engine
'''

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.base_model import Base
from os import getenv
import models


class DBStorage:
    '''
    New DataBase
    '''
    __engine = None
    __session = None

    def __init__(self):
        ''' initialisation '''
        user = getenv('HBNB_MYSQL_USER')
        pw = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        dbN = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
                                      user, pw, host, dbN), pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.dropall(sellf.__engine)

    def all(self, cls=None):
        '''
        Returns Dict Rep of objects
        '''
        dict = {}
        if cls is None:
            classes = [State, City, User, Place, Review, Amenity]
            for clas in classes:
                obj = self.__session.query(clas)
                for item in obj:
                    key = "{}.{}".format(obj.__class__.__name__,
                                         obj.id)
                    dict[key] = item
            return dict
        else:
            objects = self.__session.query(cls)
            for obj in objects:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                dict[key] = obj
            return dict

    def new(self, obj):
        '''
        adds the object to current DB session
        '''
        self.__session.add(obj)

    def save(self):
        '''
        saves all changes to current DB
        '''
        self.__session.commit()

    def delete(self, obj=None):
        '''
        delete from the current db if obj != None
        '''
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        '''
        create all tables in database
        '''
        self.__session = Base.metadata.create_all(self.__engine)
        new = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(new)
        self.__session = Session()

    def close(self):
        '''

        '''
        self.session.close()
