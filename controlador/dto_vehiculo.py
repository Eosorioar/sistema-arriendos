from modelo.vehiculo import Vehiculo
from dao.dao_vehiculo import daoVehiculo

class VehiculoDTO:
    def __init__(self):
        self.dao = daoVehiculo()
    
    def listarVehiculos(self):
        resultado = self.dao.getAllVehiculos()
        vehiculos = []
        if resultado is not None:
            for veh in resultado:
               
                vehiculo = Vehiculo(
                    patente=veh[0],
                    marca=veh[1], 
                    modelo=veh[2],
                    año=veh[3], 
                    precio=veh[4],
                    disponible=veh[5]
                )
                vehiculos.append(vehiculo)
        return vehiculos
    
    def buscarVehiculo(self, vehiculo):
        resultado = self.dao.findVehiculo(vehiculo.getPatente())
        if resultado:
           
            vehiculo_encontrado = Vehiculo(
                patente=resultado[0],
                marca=resultado[1], 
                modelo=resultado[2],
                año=resultado[3], 
                precio=resultado[4],
                disponible=resultado[5]
            )
            return vehiculo_encontrado
        return None
    
    def agregarVehiculo(self, vehiculo):
        # Asegurar estado "disponible" por defecto
        if not vehiculo.getDisponible():
            vehiculo.setDisponible("disponible")
        resultado = self.dao.addVehiculo(vehiculo)
        return resultado
    
    def actualizarVehiculo(self, vehiculo):
        resultado = self.dao.updateVehiculo(vehiculo)
        return resultado
    
    def eliminarVehiculo(self, vehiculo):
        resultado = self.dao.deleteVehiculo(vehiculo.getPatente())
        return resultado
    
    def listarVehiculosDisponibles(self):
        resultado = self.dao.getVehiculosDisponibles()
        vehiculos = []
        if resultado is not None:
            for veh in resultado:
                vehiculo = Vehiculo(
                    patente=veh[0],
                    marca=veh[1], 
                    modelo=veh[2],
                    año=veh[3], 
                    precio=veh[4],
                    disponible=veh[5]
                )
                vehiculos.append(vehiculo)
        return vehiculos