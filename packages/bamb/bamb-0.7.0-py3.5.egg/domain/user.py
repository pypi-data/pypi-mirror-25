
class User(object):

    def __init__(self, account, name="", privilege="", client=None):

        self.__account = account
        self.__name = name
        self.__client_object = client
        self.__privilege = privilege

    @property
    def account(self):
        return self.__account

    @property
    def name(self):
        return self.__name

    @property
    def privilege(self):
        return self.__privilege

    @property
    def client_object(self):
        return self.__client_object

    @name.setter
    def name(self, value):
        self.__name = value

    @privilege.setter
    def privilege(self, value):
        self.__privilege = value

    @client_object.setter
    def client_object(self, obj):
        self.__client_object = obj