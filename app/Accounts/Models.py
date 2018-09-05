import re
from datetime import datetime

from passlib.hash import pbkdf2_sha256 as sha256

# a list of the users in the temporary database
users = []
admin = []


class User:
    """A user class definition"""

    def __init__(self):
        """initialise user class"""
        self.username = None
        self.firstname = None
        self.secondname = None
        self.surname = None
        self.password = None
        self.email = None
        self.image = None
        self.ID = None
        self.__isAdmin = False

        self.created = datetime.now()

    def add_user(self, username, firstname, secondname, surname, password, email):
        self.username = username
        self.firstname = firstname
        self.secondname = secondname
        self.surname = surname
        self.password = self.generate_hash(password)
        self.email = email
        self.image = None
        self.created = datetime.now()
        self.ID = self.__set_id()
        return self

    def __set_id(self):
        """assign user id incrementaly"""
        number = len(users)
        number = number + 1
        users.append(self)
        return number

    def set_image_url(self, path):
        self.image = path

    def get_admin_status(self):
        return self.__isAdmin

    @staticmethod
    def generate_hash(password):
        """Hash all passwords """
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        """validate passwords against existing hashes"""
        return sha256.verify(password, hash)

    @staticmethod
    def validate_email(email):
        if len(email) > 5:
            if re.match("^.+@([?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?))$", email) is not None:
                return True
        return False

    def update_user_list(self):
        for user in users:
            if user.ID == self.ID:
                user = self
                return

    def get_user(self, email, password):
        """fetch user details"""
        count = 0
        # return user if present
        for user in users:
            if user.email == email and self.verify_hash(password, user.password):
                count += 1
                return user

        # return false if credentials not present
        if count == 0:
            return False


class Admin(User):
    """An admin user is a User"""

    def __init__(self):
        User.__init__(self)
        self.__isAdmin = True

    def add_user(self, username, firstname, secondname, surname, password, email):
        self.username = username
        self.firstname = firstname
        self.secondname = secondname
        self.surname = surname
        self.password = self.generate_hash(password)
        self.email = email
        self.image = None
        self.created = datetime.now()
        self.ID = self.__set_id()
        return self

    def get_admin_status(self):
        return self.__isAdmin

    def __set_id(self):
        number = len(admin)
        number = number + 1
        admin.append(self)
        return number

    def update_user_list(self):
        """update the user list on updation of user attributes"""
        for user in admin:
            if user.ID == self.ID:
                user = self
                return

    def get_user(self, email, password):
        """fetch admin details"""
        count = 0
        # return user if present
        for user in admin:
            if user.email == email and self.verify_hash(password, user.password):
                count += 1
                return user

        # return false if credentials not present
        if count == 0:
            return False
