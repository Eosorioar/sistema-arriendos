from modelo.arriendo import Arriendo
from dao.dao_arriendo import daoArriendo
from controlador.dto_cliente import ClienteDTO
from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_vehiculo import VehiculoDTO

class ArriendoDTO:
    def __init__(self):
        self.dao = daoArriendo()
        self.cliente_dto = ClienteDTO()
        self.empleado_dto = EmpleadoDTO()
        self.vehiculo_dto = VehiculoDTO()
    
    def cargarArriendosBase(self):
        resultado = self.dao.getAllArriendos()
        if resultado is not None:
            for arr in resultado:
                # Buscar los objetos completos
                cliente = self.cliente_dto.buscarCliente(arr[4])
                empleado = self.empleado_dto.buscarEmpleado(arr[7])
                vehiculo = self.vehiculo_dto.buscarVehiculo(arr[10])
                
                if cliente and empleado and vehiculo:
                    arriendo = Arriendo(numArriendo=arr[0], fechaInicio=arr[1], fechaEntrega=arr[2],
                                      costoTotal=arr[3], cliente=cliente, empleado=empleado, vehiculo=vehiculo)
                    arriendo.getArriendos().append(arriendo)
    
    def listarArriendos(self):
        arriendo = Arriendo(0, None, None, 0, None, None, None)
        return arriendo.getArriendos()
    
    def buscarArriendo(self, numArriendo):
        resultado = self.dao.findArriendo(numArriendo)
        if resultado:
            cliente = Cliente(resultado[4], resultado[5], resultado[6], resultado[7], resultado[8])
            empleado = Empleado(resultado[9], resultado[10], resultado[11], 0, resultado[12], "")
            vehiculo = Vehiculo(resultado[13], resultado[14], resultado[15], resultado[16], resultado[17])
            
            return Arriendo(resultado[0], resultado[1], resultado[2], resultado[3], 
                          cliente, empleado, vehiculo)
        return None
    
    def agregarArriendo(self, numArriendo, fechaInicio, fechaEntrega, costoTotal, run_cliente, run_empleado, patente_vehiculo):
        cliente = self.cliente_dto.buscarCliente(run_cliente)
        empleado = self.empleado_dto.buscarEmpleado(run_empleado)
        vehiculo = self.vehiculo_dto.buscarVehiculo(patente_vehiculo)
        
        if cliente and empleado and vehiculo:
            arriendo = Arriendo(numArriendo, fechaInicio, fechaEntrega, costoTotal, cliente, empleado, vehiculo)
            resultado = self.dao.addArriendo(arriendo)
            return resultado
        return "Error: Cliente, empleado o vehículo no encontrado"