#!/usr/bin/python3
''' Test module for the console.py'''
from models import storage
from models import State
from models.engine.db_storage import DBStorage
from io import StringIO
import sys
import models
import unittest
from console import HBNBCommand
from unittest.mock import create_autospec
from os import getenv


storage_type = getenv("HBNB_TYPE_STORAGE", "fs")


class TestConsole(unittest.TestCase):
    ''' Test the console module'''
    def setUp(self):
        '''setup for test module'''
        self.std_out_backup = sys.stdout
        self.output_capture = StringIO()
        sys.stdout = self.output_capture

    def tearDown(self):
        ''''''
        sys.stdout = self.std_out_backup

    def create_console_instance(self):
        ''' HBNBCommand class instance'''
        return HBNBCommand()

    def test_quit(self):
        ''' Test quit '''
        console_instance = self.create_console_instance()
        self.assertTrue(console_instance.onecmd("quit"))

    def test_EOF(self):
        ''' Test EOF'''
        console_instance = self.create_console_instance()
        self.assertTrue(console_instance.onecmd("EOF"))

    def test_all(self):
        ''' Test all '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("all")
        self.assertTrue(isinstance(self.output_capture.getvalue(), str))

    @unittest.skipIf(storage_type == "db", "Testing database storage only")
    def test_show(self):
        '''
            Test show
        '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("create User")
        user_identifier = self.output_capture.getvalue()
        sys.stdout = self.std_out_backup
        self.output_capture.close()
        self.output_capture = StringIO()
        sys.stdout = self.output_capture
        console_instance.onecmd("show User " + user_identifier)
        output_string = (self.output_capture.getvalue())
        sys.stdout = self.std_out_backup
        self.assertTrue(str is type(output_string))

    @unittest.skipIf(storage_type == "db", "Testing database storage only")
    def test_show_class_name(self):
        '''
            Testing the error messages missing class name.
        '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("create User")
        user_identifier = self.output_capture.getvalue()
        sys.stdout = self.std_out_backup
        self.output_capture.close()
        self.output_capture = StringIO()
        sys.stdout = self.output_capture
        console_instance.onecmd("show")
        output_string = (self.output_capture.getvalue())
        sys.stdout = self.std_out_backup
        self.assertEqual("** class name missing **\n", output_string)

    def test_show_class_name(self):
        '''
            Test missing id errors
        '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("create User")
        user_identifier = self.output_capture.getvalue()
        sys.stdout = self.std_out_backup
        self.output_capture.close()
        self.output_capture = StringIO()
        sys.stdout = self.output_capture
        console_instance.onecmd("show User")
        output_string = (self.output_capture.getvalue())
        sys.stdout = self.std_out_backup
        self.assertEqual("** instance id missing **\n", output_string)

    @unittest.skipIf(storage_type == "db", "Testing database storage only")
    def test_show_no_instance_found(self):
        '''
            Test show message error for id missing
        '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("create User")
        user_identifier = self.output_capture.getvalue()
        sys.stdout = self.std_out_backup
        self.output_capture.close()
        self.output_capture = StringIO()
        sys.stdout = self.output_capture
        console_instance.onecmd("show User " + "124356876")
        output_string = (self.output_capture.getvalue())
        sys.stdout = self.std_out_backup
        self.assertEqual("** no instance found **\n", output_string)

    def test_create(self):
        '''
            Test create
        '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("create User email=lgnd@hbnb.com password=app")
        self.assertTrue(isinstance(self.output_capture.getvalue(), str))

    def test_class_name(self):
        '''
            Testing missing class name.
        '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("create")
        output_string = (self.output_capture.getvalue())
        self.assertEqual("** class name missing **\n", output_string)

    def test_class_name_doesnt_exist(self):
        '''
            More test on error messages.
        '''
        console_instance = self.create_console_instance()
        console_instance.onecmd("create Binita")
        output_string = (self.output_capture.getvalue())
        self.assertEqual("** class doesn't exist **\n", output_string)

    @unittest.skipIf(storage_type != 'db', "Testing DBstorage only")
    def test_create_db(self):
        console_instance = self.create_console_instance()
        console_instance.onecmd("create State name=California")
        result_set = storage.all("State")
        self.assertTrue(len(result_set) > 0)
