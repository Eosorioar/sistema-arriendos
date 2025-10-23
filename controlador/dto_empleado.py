from modelo.empleado import Empleado
from dao.dao_empleado import daoEmpleado
from utils.encoder import Encoder

class EmpleadoDTO:
    def __init__(self):
        self.dao = daoEmpleado()
    
    def listarEmpleados(self):
        # CONSULTA DIRECTAMENTE LA BD CADA VEZ
        resultado = self.dao.getAllEmpleados()
        empleados = []
        if resultado is not None:
            for emp in resultado:
                empleado = Empleado(run=emp[0], nombre=emp[1], apellido=emp[2], 
                                  codigo=emp[3], cargo=emp[4], password=emp[5])
                empleados.append(empleado)
        return empleados
    
    def buscarEmpleado(self, run):
        resultado = self.dao.findEmpleado(run)
        if resultado:
            return Empleado(run=resultado[0], nombre=resultado[1], apellido=resultado[2], 
                          codigo=resultado[3], cargo=resultado[4], password=resultado[5])
        return None
    
    def validarLogin(self, run, password):
        # Primero buscar el empleado completo para verificar credenciales
        empleado_completo = self.dao.findEmpleado(run)
        
        if empleado_completo:
            # Verificar contraseña
            if Encoder().decode(password, empleado_completo[5]):  # password está en índice 5
                # Retornar el empleado completo
                return Empleado(
                    run=empleado_completo[0], 
                    nombre=empleado_completo[1], 
                    apellido=empleado_completo[2],
                    codigo=empleado_completo[3], 
                    cargo=empleado_completo[4], 
                    password=empleado_completo[5]
                )
        return None
    
    def agregarEmpleado(self, run, nombre, apellido, codigo, cargo, password):
        resultado = self.dao.addEmpleado(Empleado(run, nombre, apellido, codigo, cargo, Encoder().encode(password)))
        return resultado
    
    def actualizarEmpleado(self, run, nombre, apellido, cargo, password):
        resultado = self.dao.updateEmpleado(Empleado(run, nombre, apellido, 0, cargo, Encoder().encode(password)))
        return resultado
    
    def eliminarEmpleado(self, run):
        resultado = self.dao.deleteEmpleado(run)
        return resultado