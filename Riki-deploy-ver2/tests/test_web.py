from . import WikiBaseTestCase

import os

from flask import current_app
from flask import Flask
from flask import g
from flask import app
from wiki.web.forms import URLForm
from wiki.web.user import UserManager
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

class TestURLForm(WebContentTestCase):
    '''def test_validate_url(self):
            form = URLForm()
            assert URLForm.validate_url(form,'home')
        '''
    def test_clean_url(self):
            url = '/home'
            assert URLForm.clean_url(URLForm(), url) == url

class TestLoginForm(WebContentTestCase):
    def test_validate_name(self):
        self.fail()

    def test_validate_password(self):
        self.fail()

class TestUserManager(WebContentTestCase):

    def test_read(self):
        self.fail()

    def test_write(self):
        self.fail()

    def test_add_user(self):
        self.fail()

    def test_get_user(self):
        um = UserManager(current_app.config['USER_DIR'])
        self.assertIsNotNone(um.get_user('sam'))

    def test_delete_user(self):
        self.fail()

    def test_update(self):
        self.fail()

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
