from datetime import datetime

class User:
    __listaUser = []
    def __init__(self, username, email="", password="", create_time=datetime.now()):
        self.__username = username
        self.__email = email
        self.__password = password
        self.__create_time = create_time

    def __str__(self):
        return "{0} {1} {2}".format(self.__username, self.__email, self.__create_time)
    def getListaUser(self):
        return self.__listaUser
    def getUsername(self):
        return self.__username
    def getEmail(self):
        return self.__email
    def getPassword(self):
        return self.__password
    def getCreate_time(self):
        return self.__create_time
    def setEmail(self, email):
        self.__email = email