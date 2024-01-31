#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table
from os import getenv
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review", backref="place",
                               cascade='all, delete, delete-orphan')
        amenities = relationship('Amenity',
                                 secondary='place_amenity', viewonly=False,
                                 back_populates='place_amenities')
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            '''
            Returns the list review instances if
            Review.place_id == curr place.id
            '''
            all_reviews = []
            for review in models.storage.all(Review).values():
                if review.place_id == self.id:
                    all_reviews.append(review)
                    return all_reviews

        @property
        def amenities(self):
            ''' returns the list of amenity instances '''
            amenity_list = []
            for obj in models.storage.all(Amenity).values():
                if obj.place_id == self.id:
                    amenity_list.append(obj)
            return amenity_list

        @amenities.setter
        def amenities(self, obj=None):
            ''' adds an Amenity.id to the attribute amenity_ids'''
            if obj is not None:
                if isinstance(obj, Amenity) and obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)
