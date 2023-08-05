from domain import user

class UserManager(object):

    def __init__(self):
        self.__online_users = {}

    def user_login(self, u):
        if isinstance(u, user.User):
            self.__online_users[u.account] = u

    def user_logout(self, account):
        self.__online_users.pop(account, None)

    @property
    def online_users(self):
        return self.__online_users

