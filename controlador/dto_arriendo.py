from modelo.arriendo import Arriendo
from dao.dao_arriendo import daoArriendo
from controlador.dto_cliente import ClienteDTO
from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_vehiculo import VehiculoDTO
from modelo.cliente import Cliente  
from modelo.empleado import Empleado
from modelo.vehiculo import Vehiculo

class ArriendoDTO:
    def __init__(self):
        self.dao = daoArriendo()
        self.cliente_dto = ClienteDTO()
        self.empleado_dto = EmpleadoDTO()
        self.vehiculo_dto = VehiculoDTO()
    
    def listarArriendos(self):
        resultado = self.dao.getAllArriendos()
        arriendos = []

        if resultado is not None:
            for arr in resultado:
                try:
                    # Crear objetos completos desde los datos del JOIN
                    cliente = Cliente(arr[4], arr[5], arr[6], "", "")
                    empleado = Empleado(arr[7], arr[8], arr[9], 0, "", "")
                    vehiculo = Vehiculo(arr[10], arr[11], arr[12], 0, 0, "")
                    
                    arriendo = Arriendo(
                        numArriendo=arr[0],
                        fechaInicio=arr[1],
                        fechaEntrega=arr[2],
                        costoTotal=arr[3],
                        cliente=cliente,
                        empleado=empleado,
                        vehiculo=vehiculo
                    )
                    arriendos.append(arriendo)

                except Exception as e:
                    print(f"Error creando arriendo: {e}")
                    continue
        return arriendos
    
    def buscarArriendo(self, numArriendo):
        # Mismo patrón simple que VehiculoDTO
        resultado = self.dao.findArriendo(numArriendo)
        if resultado:
            # Crear objetos desde los datos del JOIN
            cliente = Cliente(resultado[4], resultado[5], resultado[6], "", "")
            empleado = Empleado(resultado[7], resultado[8], resultado[9], 0, "", "")
            vehiculo = Vehiculo(resultado[10], resultado[11], resultado[12], 0, 0, "")
            
            arriendo_encontrado = Arriendo(
                numArriendo=resultado[0],
                fechaInicio=resultado[1],
                fechaEntrega=resultado[2],
                costoTotal=resultado[3],
                cliente=cliente,
                empleado=empleado,
                vehiculo=vehiculo
            )
            return arriendo_encontrado
        return None
    
    def agregarArriendo(self, numArriendo, fechaInicio, fechaEntrega, costoTotal, run_cliente, run_empleado, patente_vehiculo):
        # Mismo patrón que otros DTOs - recibir parámetros primitivos
        # Buscar objetos completos primero
        cliente = self.cliente_dto.buscarCliente(run_cliente)
        empleado = self.empleado_dto.buscarEmpleado(run_empleado)
        vehiculo = self.vehiculo_dto.buscarVehiculo(patente_vehiculo)
        
        if cliente and empleado and vehiculo:
            # Crear arriendo con objetos completos
            arriendo = Arriendo(numArriendo, fechaInicio, fechaEntrega, costoTotal, cliente, empleado, vehiculo)
            resultado = self.dao.addArriendo(arriendo)
            return resultado
        return "❌ Error: Cliente, empleado o vehículo no encontrado"
    
    def actualizarArriendo(self, numArriendo, fechaInicio, fechaEntrega, costoTotal, run_cliente, run_empleado, patente_vehiculo):
        # Nuevo método para actualizar
        cliente = self.cliente_dto.buscarCliente(run_cliente)
        empleado = self.empleado_dto.buscarEmpleado(run_empleado)
        vehiculo = self.vehiculo_dto.buscarVehiculo(patente_vehiculo)
        
        if cliente and empleado and vehiculo:
            arriendo = Arriendo(numArriendo, fechaInicio, fechaEntrega, costoTotal, cliente, empleado, vehiculo)
            resultado = self.dao.updateArriendo(arriendo)
            return resultado
        return "❌ Error: Cliente, empleado o vehículo no encontrado"
    
    def eliminarArriendo(self, arriendo):
        # Mantener consistencia - recibir objeto
        resultado = self.dao.deleteArriendo(arriendo.getNumArriendo())
        return resultado