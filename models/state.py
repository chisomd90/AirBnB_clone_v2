#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from models.city import City
from os import getenv
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ State class """
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade="all,delete", backref='state')
    else:
        name = ''

        @property
        def cities(self):
            '''width getter'''
            dict_ = models.storage.all(City)
            list_ = []
            for key, value in dict_.items:
                if value[state_id] == self.id:
                    list_.append(value[name])
            return (list_)
