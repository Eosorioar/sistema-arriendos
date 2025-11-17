from datetime import datetime

class Arriendo:
    __arriendos = []
    
    def __init__(self, numArriendo=0, fechaInicio=None, fechaEntrega=None, costoTotal=0, cliente=None, empleado=None, vehiculo=None):
        self.__numArriendo = numArriendo
        self.__fechaInicio = fechaInicio
        self.__fechaEntrega = fechaEntrega
        self.__costoTotal = costoTotal
        self.__cliente = cliente
        self.__empleado = empleado
        self.__vehiculo = vehiculo

    def __str__(self):
        return f"Arriendo {self.__numArriendo} - {self.__cliente.getNombre()} - {self.__vehiculo.getPatente()}"

    def getArriendos(self):
        return self.__arriendos

    def getNumArriendo(self):
        return self.__numArriendo

    def getFechaInicio(self):
        return self.__fechaInicio

    def getFechaEntrega(self):
        return self.__fechaEntrega

    def getCostoTotal(self):
        return self.__costoTotal

    def getCliente(self):
        return self.__cliente

    def getEmpleado(self):
        return self.__empleado

    def getVehiculo(self):
        return self.__vehiculo

    
    def setNumArriendo(self, numArriendo):
        self.__numArriendo = numArriendo

    def setFechaInicio(self, fechaInicio):
        self.__fechaInicio = fechaInicio

    def setFechaEntrega(self, fechaEntrega):
        self.__fechaEntrega = fechaEntrega

    def setCostoTotal(self, costoTotal):
        self.__costoTotal = costoTotal

    def setCliente(self, cliente):
        self.__cliente = cliente

    def setEmpleado(self, empleado):
        self.__empleado = empleado

    def setVehiculo(self, vehiculo):
        self.__vehiculo = vehiculo
    # === FIN SETTERS ===