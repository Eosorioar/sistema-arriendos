from modelo.vehiculo import Vehiculo
from dao.dao_vehiculo import daoVehiculo

class VehiculoDTO:
    def __init__(self):
        self.dao = daoVehiculo()
    
    def listarVehiculos(self):
        # CONSULTA DIRECTAMENTE LA BD CADA VEZ
        resultado = self.dao.getAllVehiculos()
        vehiculos = []
        if resultado is not None:
            for veh in resultado:
                vehiculo = Vehiculo(patente=veh[0], marca=veh[1], modelo=veh[2], 
                                  año=veh[3], precio=veh[4], disponible=veh[5])
                vehiculos.append(vehiculo)
        return vehiculos
    
    def buscarVehiculo(self, patente):
        resultado = self.dao.findVehiculo(patente)
        return Vehiculo(resultado[0], resultado[1], resultado[2], resultado[3], resultado[4], resultado[5]) if resultado else None
    
    def agregarVehiculo(self, patente, marca, modelo, año, precio):
        resultado = self.dao.addVehiculo(Vehiculo(patente, marca, modelo, año, precio, "disponible"))
        return resultado
    
    def actualizarVehiculo(self, patente, marca, modelo, año, precio, disponible):
        resultado = self.dao.updateVehiculo(Vehiculo(patente, marca, modelo, año, precio, disponible))
        return resultado
    
    def eliminarVehiculo(self, patente):
        resultado = self.dao.deleteVehiculo(patente)
        return resultado
    
    def listarVehiculosDisponibles(self):
        resultado = self.dao.getVehiculosDisponibles()
        vehiculos = []
        if resultado is not None:
            for veh in resultado:
                vehiculos.append(Vehiculo(veh[0], veh[1], veh[2], veh[3], veh[4], veh[5]))
        return vehiculos
    
