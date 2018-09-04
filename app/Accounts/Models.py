from datetime import date, datetime

from passlib.hash import pbkdf2_sha256 as sha256

# a list of the users in the temporary database
users = []
admin = []


class User:
    """A user class definition"""

    def __init__(self, username, firstname, secondname, surname, password, email):
        """initialise user class"""
        self.username = username
        self.firstname = firstname
        self.secondname = secondname
        self.surname = surname
        self.password = self.generate_hash(password)
        self.email = email
        self.image = None
        self.ID = self.__set_id()
        self.__isAdmin = False

        self.created = datetime.now()

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


class Admin(User):
    """An admin user is a User"""

    def __init__(self, username, firstname, secondname, surname, password, email):
        User.__init__(self, username=username, firstname=firstname, secondname=secondname, surname=surname,
                      password=password, email=email)
        self.ID = self.__set_id()
        self.__isAdmin = True

    def get_admin_status(self):
        return self.__isAdmin

    def __set_id(self):
        number = len(admin)
        number = number + 1
        admin.append(self)
        return number
