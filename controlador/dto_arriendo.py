from modelo.arriendo import Arriendo
from dao.dao_arriendo import daoArriendo
from controlador.dto_cliente import ClienteDTO
from controlador.dto_empleado import EmpleadoDTO
from controlador.dto_vehiculo import VehiculoDTO
from modelo.cliente import Cliente  # ← AGREGAR ESTOS IMPORTS
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
                    cliente = Cliente(
                        run=arr[4],      # cliente_run
                        nombre=arr[5],   # cliente_nombre  
                        apellido=arr[6], # cliente_apellido
                        telefono="",     # No disponible en el JOIN
                        direccion=""     # No disponible en el JOIN
                    )
                
                    empleado = Empleado(
                        run=arr[7],      # empleado_run
                        nombre=arr[8],   # empleado_nombre
                        apellido=arr[9], # empleado_apellido
                        codigo=0,        # No disponible en el JOIN
                        cargo="",        # No disponible en el JOIN
                        password=""      # No disponible en el JOIN
                    )
                
                    vehiculo = Vehiculo(
                        patente=arr[10], # patente
                        marca=arr[11],   # marca
                        modelo=arr[12],  # modelo
                        año=0,           # No disponible en el JOIN
                        precio=0,        # No disponible en el JOIN
                        disponible=""    # No disponible en el JOIN
                    )
                
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
    
    def buscarArriendo(self, arriendo):
        resultado = self.dao.findArriendo(arriendo.getNumArriendo())
        if resultado:
            # CORREGIDO: Usar constructores con imports
            cliente_buscar = Cliente(resultado[4], "", "", "", "")
            empleado_buscar = Empleado(resultado[7], "", "", 0, "", "")
            vehiculo_buscar = Vehiculo(resultado[10], "", "", 0, 0, "")
            
            cliente = self.cliente_dto.buscarCliente(cliente_buscar)
            empleado = self.empleado_dto.buscarEmpleado(empleado_buscar)
            vehiculo = self.vehiculo_dto.buscarVehiculo(vehiculo_buscar)
            
            if cliente and empleado and vehiculo:
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
    
    def agregarArriendo(self, arriendo):
        # CORREGIDO: Ya recibe objeto completo
        cliente = self.cliente_dto.buscarCliente(arriendo.getCliente())
        empleado = self.empleado_dto.buscarEmpleado(arriendo.getEmpleado())
        vehiculo = self.vehiculo_dto.buscarVehiculo(arriendo.getVehiculo())
        
        if cliente and empleado and vehiculo:
            arriendo.setCliente(cliente)
            arriendo.setEmpleado(empleado)
            arriendo.setVehiculo(vehiculo)
            resultado = self.dao.addArriendo(arriendo)
            return resultado
        return "Error: Cliente, empleado o vehículo no encontrado"
    
    def eliminarArriendo(self, arriendo):
        resultado = self.dao.deleteArriendo(arriendo.getNumArriendo())
        return resultado