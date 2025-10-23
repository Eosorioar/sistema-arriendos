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
    
    def listarArriendos(self):
        # CONSULTA DIRECTAMENTE LA BD CADA VEZ
        resultado = self.dao.getAllArriendos()
        arriendos = []
        if resultado is not None:
            for arr in resultado:
                cliente = self.cliente_dto.buscarCliente(arr[4])  # cliente_run
                empleado = self.empleado_dto.buscarEmpleado(arr[7])  # empleado_run  
                vehiculo = self.vehiculo_dto.buscarVehiculo(arr[10])  # patente
            
                if cliente and empleado and vehiculo:
                    arriendo = Arriendo(numArriendo=arr[0], fechaInicio=arr[1], fechaEntrega=arr[2],
                                      costoTotal=arr[3], cliente=cliente, empleado=empleado, vehiculo=vehiculo)
                    arriendos.append(arriendo)
        return arriendos
    
    def buscarArriendo(self, numArriendo):
        resultado = self.dao.findArriendo(numArriendo)
        if resultado:
            cliente = self.cliente_dto.buscarCliente(resultado[4])
            empleado = self.empleado_dto.buscarEmpleado(resultado[7])
            vehiculo = self.vehiculo_dto.buscarVehiculo(resultado[10])
            
            if cliente and empleado and vehiculo:
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
    
    def eliminarArriendo(self, numArriendo):
        resultado = self.dao.deleteArriendo(numArriendo)
        return resultado