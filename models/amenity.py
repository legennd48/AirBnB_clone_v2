#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity
from os import getenv


class Amenity(BaseModel, Base):
    '''
    amenity clss for amenities
    '''
    __tablename__ = 'amenities'
    if getenv("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(60), nullable=False)
        place_amenities = relationship('Place', secondary=place_amenity,
                                       back_populates="amenities")
    else:
        name = ''
