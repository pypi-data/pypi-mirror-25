"""User database classes. Useful for network servers.

Example:
    >>> from dtplib.UserDB import UserDB
    >>> database = UserDB("users.db")
    >>> database.new("myname", "password123")
    >>> database.validLogin("myname", "password123")
    True
    >>> database.validLogin("wrongname", "wrongpassword")
    False
    >>> database.getUsers()
    ['myname']
    >>> database.getInfo("myname")
    None
    >>> database.setInfo("myname", ("foo", "bar"))
    >>> database.getInfo("myname")
    ('foo', 'bar')
    >>> database.remove("myname")
    >>> database.getUsers()
    []
    >>> database.delete()
"""

import os
import hashlib
try:
    import cPickle as pickle
except:
    import pickle

class UserDBError(Exception):
    pass

class UserDB:
    """Create user databases with hashed passwords.

    'filename' is the file in which the user database is stored.
    'hashFunction' can be any typical hash algorithm: md5, sha1,
    sha256, etc. The default algorithm is md5.
    """
    def __init__(self, filename, hashFunction = "md5"):
        self.filename = filename
        if hashFunction not in hashlib.algorithms:
            raise UserDBError("invalid hash algorithm")
        self.hashFunction = hashFunction
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                self.users = pickle.load(f)
        else:
            open(filename, "w").close()
            self.users = {}

    def validLogin(self, username, password):
        """Check if a username password combination is valid."""
        if username not in self.users:
            return False
        h = hashlib.new(self.hashFunction)
        h.update(password)
        hashedPassword = h.hexdigest()
        return self.users[username][0] == hashedPassword

    def new(self, username, password, info = None):
        """Create a new user with specified username, password, and
        info (optional).
        """
        if username in self.users:
            raise UserDBError("user already exists")
        h = hashlib.new(self.hashFunction)
        h.update(password)
        hashedPassword = h.hexdigest()
        self.users[username] = [hashedPassword, info]
        open(self.filename, "w").close()
        with open(self.filename, "w") as f:
            pickle.dump(self.users, f)

    def remove(self, username):
        """Delete a user from the database."""
        if username not in self.users:
            raise UserDBError("user does not exist")
        self.users.pop(username)
        open(self.filename, "w").close()
        with open(self.filename, "w") as f:
            pickle.dump(self.users, f)

    def getUsers(self):
        """Get a list of all users in the database."""
        return self.users.keys()

    def getInfo(self, username):
        """Get the info of a user. If no info exists, a NoneType is
        returned.
        """
        if username not in self.users:
            raise UserDBError("user does not exist")
        return self.users[username][1]

    def setInfo(self, username, info):
        """Set the info of a user."""
        if username not in self.users:
            raise UserDBError("user does not exist")
        self.users[username][1] = info
        open(self.filename, "w").close()
        with open(self.filename, "w") as f:
            pickle.dump(self.users, f)

    def delete(self):
        """Delete the database."""
        os.remove(self.filename)
        self.users = None

if __name__ == "__main__":
    pass
