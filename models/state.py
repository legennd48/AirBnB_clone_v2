#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """
        Getter property that returns the list of city instances
        if City.state_id == current State.id
        """
        cities_list = []
        for city in storage.all("City").values():
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
