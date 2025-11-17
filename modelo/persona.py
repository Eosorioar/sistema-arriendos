from datetime import datetime

class Persona:
    __listaPersonas = []
    
    def __init__(self, run, nombre, apellido):
        self.__run = run
        self.__nombre = nombre
        self.__apellido = apellido

    def __str__(self):
        return f"{self.__run} {self.__nombre} {self.__apellido}"

    def getListaPersonas(self):
        return self.__listaPersonas

    def getRun(self):
        return self.__run

    def getNombre(self):
        return self.__nombre

    def getApellido(self):
        return self.__apellido

    def setNombre(self, nombre):
        self.__nombre = nombre

    def setApellido(self, apellido):
        self.__apellido = apellido