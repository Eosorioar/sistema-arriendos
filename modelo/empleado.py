from modelo.persona import Persona
from datetime import datetime
#USAMOS LA HERENCIA DE PERSONA USANDO SUPER
class Empleado(Persona):
    __listaEmpleados = []
    
    def __init__(self, run="", nombre="", apellido="", codigo=0, cargo="", password=""):
        super().__init__(run, nombre, apellido)
        self.__codigo = codigo
        self.__cargo = cargo
        self.__password = password

    def __str__(self):
        return f"{self.getRun()} {self.getNombre()} {self.getApellido()} {self.__cargo}"

    def getListaEmpleados(self):
        return self.__listaEmpleados

    def getCodigo(self):
        return self.__codigo

    def getCargo(self):
        return self.__cargo

    def getPassword(self):
        return self.__password

    def setCargo(self, cargo):
        self.__cargo = cargo

    def setPassword(self, password):
        self.__password = password