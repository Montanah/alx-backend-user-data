#!/usr/bin/env python3
""" End-to-end integration test
"""

import requests
import time
import os
import signal
import subprocess
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from utils import register_user, log_in_wrong_password, profile_unlogged, \
    log_in, profile_logged, log_out, reset_password_token, update_password


class TestAuth(unittest.TestCase):
    """ Auth integration test
    """

    @classmethod
    def setUpClass(cls):
        """ Run only once before starting the test server
        """
        cls.get_env = PropertyMock(return_value='http://0.0.0.0:5000/')
        cls.p = patch('auth.getenv', cls.get_env)
        cls.p.start()
        cls.proc = subprocess.Popen(['./app.py'], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        """ Run only once after all test methods
        """
        cls.p.stop()
        cls.proc.kill()
        cls.proc.communicate()

    def setUp(self):
        """ Run before each test method
        """
        requests.delete('http://0.0.0.0:5000/')
        requests.post('http://0.0.0.0:5000/')
        self.register_user = register_user
        self.log_in_wrong_password = log_in_wrong_password
        self.profile_unlogged = profile_unlogged
        self.log_in = log_in
        self.profile_logged = profile_logged
        self.log_out = log_out
        self.reset_password_token = reset_password_token
        self.update_password = update_password

    def tearDown(self):
        """ Run after each test method
        """
        requests.delete('http://0.0.0.0:5000/')
        requests.post('http://0.0.0.0:5000/')
                      
    def test_register_user(self):
        """ Test register_user
        """
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), {'message': ''})

    def test_log_in_wrong_password(self):
        """ Test log_in_wrong_password
        """
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.json(), {'message': ''})
                                    
    def test_profile_unlogged(self):
        """ Test profile_unlogged
        """
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.get('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json(), {'message': ''})                                

    def test_log_in(self):
        """ Test valid_login
        """
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.json(), {'message': ''})
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json(), {'message': ''})
                                    
    def test_profile_logged(self):
        """ Test profile_logged
        """
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.get('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.get('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json(), {'message': ''})
                                    
    def test_log_out(self):
        """ Test log_out
        """
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.delete('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json(), {'message': ''})
                                    
    def test_reset_password_token(self):
        """ Test get_reset_password_token
        """

        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), {'message': ''})
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), {'message': ''})
        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json(), {'message': ''})
                                    
    def test_update_password(self):
        """ Test update_password
        """

        r = requests.post('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        reset_token = r.json().get('reset_token')
        r = requests.put('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json(), {'email': ''})
        r = requests.put('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json(), {'message': ''})
        r = requests.put('http://0.0.0.0:5000/')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.json(), {'message': ''})
                                    

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
