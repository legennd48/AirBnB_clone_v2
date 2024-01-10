#!/usr/bin/python3
"""This module contains tests for the Amenity class."""
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
from models.base_model import BaseModel
from datetime import datetime
from unittest.mock import patch
from time import sleep
from os import getenv
import pycodestyle
import inspect
storage_type = getenv("HBNB_TYPE_STORAGE")


class TestAmenity(test_basemodel):
    """This class tests the Amenity class."""

    def __init__(self, *args, **kwargs):
        """Initialize an instance of TestAmenity."""
        super().__init__(*args, **kwargs)
        self.test_class = "Amenity"
        self.test_instance = Amenity

    def test_name_attribute(self):
        """Test the name attribute of the Amenity class."""
        new_instance = self.test_instance()
        self.assertEqual(type(new_instance.name), str)


class TestPEP8(unittest.TestCase):
    """This class tests the Amenity class for PEP8 style compliance."""
    def test_pep8_compliance(self):
        """Test that models/amenity.py conforms to PEP8."""
        pep8style = pycodestyle.StyleGuide(quiet=True)
        result = pep8style.check_files(['models/amenity.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")


class TestInheritance(unittest.TestCase):
    """This class tests if the Amenity class inherits from BaseModel."""
    def test_inheritance(self):
        """Test if Amenity is a subclass of BaseModel."""
        amenity_instance = Amenity()
        self.assertIsInstance(amenity_instance, Amenity)
        self.assertTrue(issubclass(type(amenity_instance), BaseModel))
        self.assertEqual(str(type(amenity_instance)),
                         "<class 'models.amenity.Amenity'>")


class TestAmenityAttributes(unittest.TestCase):
    """This class tests the attributes of the Amenity class."""
    def test_attribute_types(self):
        """Test the types of the attributes of the Amenity class."""
        with patch('models.amenity'):
            instance = Amenity()
            self.assertEqual(type(instance), Amenity)
            instance.name = "Barbie"
            expected_attr_types = {
                    "id": str,
                    "created_at": datetime,
                    "updated_at": datetime,
                    "name": str,
                    }
            instance_dict = instance.to_dict()
            expected_dict_attrs = [
                    "id",
                    "created_at",
                    "updated_at",
                    "name",
                    "__class__"
                    ]
            self.assertCountEqual(instance_dict.keys(), expected_dict_attrs)
            self.assertEqual(instance_dict['name'], 'Barbie')
            self.assertEqual(instance_dict['__class__'], 'Amenity')

            for attr, attr_type in expected_attr_types.items():
                with self.subTest(attr=attr, attr_type=attr_type):
                    self.assertIn(attr, instance.__dict__)
                    self.assertIs(type(instance.__dict__[attr]), attr_type)
            self.assertEqual(instance.name, "Barbie")

    def test_id_and_created_at(self):
        """Test the id and created_at attributes of the Amenity class."""
        amenity_1 = Amenity()
        sleep(2)
        amenity_2 = Amenity()
        sleep(2)
        amenity_3 = Amenity()
        sleep(2)
        amenity_list = [amenity_1, amenity_2, amenity_3]
        for instance in amenity_list:
            amenity_id = instance.id
            with self.subTest(amenity_id=amenity_id):
                self.assertIs(type(amenity_id), str)
        self.assertNotEqual(amenity_1.id, amenity_2.id)
        self.assertNotEqual(amenity_1.id, amenity_3.id)
        self.assertNotEqual(amenity_2.id, amenity_3.id)
        self.assertTrue(amenity_1.created_at <= amenity_2.created_at)
        self.assertTrue(amenity_2.created_at <= amenity_3.created_at)
        self.assertNotEqual(amenity_1.created_at, amenity_2.created_at)
        self.assertNotEqual(amenity_1.created_at, amenity_3.created_at)
        self.assertNotEqual(amenity_3.created_at, amenity_2.created_at)

    def test_str_method(self):
        """
        Test the __str__ method of the Amenity class.
        """
        amenity_instance = Amenity()
        str_output = "[Amenity] ({}) {}".format(
            amenity_instance.id, amenity_instance.__dict__)
        self.assertEqual(str_output, str(amenity_instance))

    @patch('models.storage')
    def test_save_method(self, mock_storage):
        """Test the save method of the Amenity class."""
        instance = Amenity()
        created_at = instance.created_at
        sleep(2)
        updated_at = instance.updated_at
        instance.save()
        new_created_at = instance.created_at
        sleep(2)
        new_updated_at = instance.updated_at
        self.assertNotEqual(updated_at, new_updated_at)
        self.assertEqual(created_at, new_created_at)
        self.assertTrue(mock_storage.save.called)


class TestAmenityMethods(unittest.TestCase):
    """Test the methods of the Amenity class."""

    def test_is_subclass(self):
        """Test that Amenity is a subclass of BaseModel."""
        amenity_instance = Amenity()
        self.assertIsInstance(amenity_instance, BaseModel)
        self.assertTrue(hasattr(amenity_instance, "id"))
        self.assertTrue(hasattr(amenity_instance, "created_at"))
        self.assertTrue(hasattr(amenity_instance, "updated_at"))

    def test_name_attr(self):
        """Test the name attribute of the Amenity class."""
        amenity_instance = Amenity()
        self.assertTrue(hasattr(amenity_instance, "name"))
        if storage_type == 'db':
            self.assertEqual(amenity_instance.name, None)
        else:
            self.assertEqual(amenity_instance.name, "")

    def test_to_dict_creates_dict(self):
        """Test the to_dict method of the Amenity class."""
        amenity_instance = Amenity()
        print(amenity_instance.__dict__)
        new_dict = amenity_instance.to_dict()
        self.assertEqual(type(new_dict), dict)
        self.assertFalse("_sa_instance_state" in new_dict)
        for attr in amenity_instance.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_dict)
        self.assertTrue("__class__" in new_dict)

    def test_to_dict_values(self):
        """Test the values of the dictionary returned by to_dict."""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        amenity_instance = Amenity()
        new_dict = amenity_instance.to_dict()
        self.assertEqual(new_dict["__class__"], "Amenity")
        self.assertEqual(type(new_dict["created_at"]), str)
        self.assertEqual(type(new_dict["updated_at"]), str)
        self.assertEqual(new_dict["created_at"],
                         amenity_instance.created_at.strftime(t_format))
        self.assertEqual(new_dict["updated_at"],
                         amenity_instance.updated_at.strftime(t_format))

    def test_str(self):
        """Test the __str__ method of the Amenity class."""
        amenity_instance = Amenity()
        string = "[Amenity] ({}) {}".format(
            amenity_instance.id, amenity_instance.__dict__)
        self.assertEqual(string, str(amenity_instance))
