from . import WikiBaseTestCase

import os

from flask import current_app
from flask import Flask
from flask import g
from flask import app
from wiki.web.forms import URLForm
from wiki.web.user import UserManager
from wiki.web.user import User
class WebContentTestCase(WikiBaseTestCase):
    """
        Various test cases around web content.
    """

    def test_index_missing(self):
        """
            Assert the wiki will correctly play the content missing
            index page, if no index page exists.
        """
        rsp = self.app.get('/')
        assert b"You did not create any content yet." in rsp.data
        assert rsp.status_code == 200


TEST_FILE_PATH = '/Users/Nick/Documents/GitHub/SEWiki/Riki-deploy-ver2/tests/'

class TestUserManager(WebContentTestCase):

    def setUp(self):
        super(TestUserManager, self).setUp()
        self.file = os.path.join(TEST_FILE_PATH, 'users.json')

    def test_invalid_authentication_method(self):
        m = UserManager(TEST_FILE_PATH)
        self.assertRaises(NotImplementedError, m.add_user, m, 'bobby', 12345, authentication_method='this will cause an error')

    def test_read(self):
        self.fail()

    def test_write(self):
        self.fail()

    def test_add_user(self):
        self.fail()

    def test_get_user(self):
        self.fail()

    def test_delete_user(self):
        self.fail()

    def test_update(self):
        self.fail()

'''
class TestUser(WebContentTestCase):
    def test_get(self):
        self.fail()

    def test_set(self):
        self.fail()

    def test_save(self):
        self.fail()

    def test_is_authenticated(self):
        self.fail()

    def test_is_active(self):
        self.fail()

    def test_is_anonymous(self):
        self.fail()

    def test_get_id(self):
        self.fail()

    def test_check_password(self):
        self.fail()
'''
