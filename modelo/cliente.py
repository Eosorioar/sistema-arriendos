from modelo.persona import Persona

class Cliente(Persona):
    __listaClientes = []
    
    def __init__(self, run="", nombre="", apellido="", telefono="", direccion=""):
        super().__init__(run, nombre, apellido)
        self.__telefono = telefono
        self.__direccion = direccion

    def __str__(self):
        return f"{self.getRun()} {self.getNombre()} {self.getTelefono()}"

    def getListaClientes(self):
        return self.__listaClientes

    def getTelefono(self):
        return self.__telefono

    def getDireccion(self):
        return self.__direccion

    def setTelefono(self, telefono):
        self.__telefono = telefono

    def setDireccion(self, direccion):
        self.__direccion = direccion