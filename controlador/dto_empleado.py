from modelo.empleado import Empleado
from dao.dao_empleado import daoEmpleado
from utils.encoder import Encoder

class EmpleadoDTO:
    def __init__(self):
        self.dao = daoEmpleado()
    
    def listarEmpleados(self):
        resultado = self.dao.getAllEmpleados()
        empleados = []
        if resultado is not None:
            for emp in resultado:
                empleado = Empleado(
                    run=emp[0], 
                    nombre=emp[1], 
                    apellido=emp[2],
                    codigo=emp[3], 
                    cargo=emp[4], 
                    password=emp[5]
                )
                empleados.append(empleado)
        return empleados
    
    def buscarEmpleado(self, run):
        empleado = Empleado(run, "", "", 0, "", "")
        resultado = self.dao.findEmpleado(empleado.getRun())  
        if resultado:
            empleado_encontrado = Empleado(
                run=resultado[0],
                nombre=resultado[1], 
                apellido=resultado[2],
                codigo=resultado[3], 
                cargo=resultado[4], 
                password=resultado[5]
            ) 
            return empleado_encontrado
        return None 
    
    def validarLogin(self, empleado):  
        empleado_completo = self.dao.findEmpleado(empleado.getRun())  
        if empleado_completo:
            if Encoder().decode(empleado.getPassword(), empleado_completo[5]): 
                empleado_valido = Empleado(
                     run=empleado_completo[0],
                nombre=empleado_completo[1], 
                apellido=empleado_completo[2],
                codigo=empleado_completo[3], 
                cargo=empleado_completo[4], 
                password=empleado_completo[5]
                )
                return empleado_valido
        return None
    
    def agregarEmpleado(self, run, nombre, apellido, codigo, cargo, clave): 
        empleado = Empleado(run, nombre, apellido, codigo, cargo, clave)
        empleado.setPassword(Encoder().encode(empleado.getPassword()))
        resultado = self.dao.addEmpleado(empleado)
        return resultado
    
    def actualizarEmpleado(self, run, nombre, apellido, cargo, clave):
        empleado_existente = self.buscarEmpleado(run)
        
        if not empleado_existente:
            return "Empleado no encontrado"
        empleado = Empleado(run, nombre, apellido, empleado_existente.getCodigo(), cargo, clave)
        empleado.setPassword(Encoder().encode(empleado.getPassword()))
        resultado = self.dao.updateEmpleado(empleado)
        return resultado

    def eliminarEmpleado(self, run):
        empleado= Empleado(run, "", "", 0, "", "")
        resultado = self.dao.deleteEmpleado(empleado.getRun())  
        return resultado