from datetime import datetime

class Vehiculo:
    __listaVehiculos = []
    
    def __init__(self, patente="", marca="", modelo="", año=0, precio=0, disponible="disponible"):
        self.__patente = patente
        self.__marca = marca
        self.__modelo = modelo
        self.__año = año
        self.__precio = precio
        self.__disponible = disponible

    def __str__(self):
        return f"{self.__patente} {self.__marca} {self.__modelo} {self.__disponible}"

    def getListaVehiculos(self):
        return self.__listaVehiculos

    def getPatente(self):
        return self.__patente

    def getMarca(self):
        return self.__marca

    def getModelo(self):
        return self.__modelo

    def getAño(self):
        return self.__año

    def getPrecio(self):
        return self.__precio

    def getDisponible(self):
        return self.__disponible

    def setMarca(self, marca):
        self.__marca = marca

    def setModelo(self, modelo):
        self.__modelo = modelo

    def setPrecio(self, precio):
        self.__precio = precio

    def setDisponible(self, disponible):
        self.__disponible = disponible