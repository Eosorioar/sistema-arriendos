from modelo.cliente import Cliente
from dao.dao_cliente import daoCliente

class ClienteDTO:
    def __init__(self):
        self.dao = daoCliente()
    
    def listarClientes(self):
        # CONSULTA DIRECTAMENTE LA BD CADA VEZ
        resultado = self.dao.getAllClientes()
        clientes = []
        if resultado is not None:
            for cli in resultado:
                cliente = Cliente(run=cli[0], nombre=cli[1], apellido=cli[2], 
                                telefono=cli[3], direccion=cli[4])
                clientes.append(cliente)
        return clientes
    
    def buscarCliente(self, run):
        resultado = self.dao.findCliente(run)
        if resultado:
            return Cliente(run=resultado[0], nombre=resultado[1], apellido=resultado[2], 
                         telefono=resultado[3], direccion=resultado[4])
        return None
    
    def agregarCliente(self, run, nombre, apellido, telefono, direccion):
        resultado = self.dao.addCliente(Cliente(run, nombre, apellido, telefono, direccion))
        return resultado
    
    def actualizarCliente(self, run, nombre, apellido, telefono, direccion):
        resultado = self.dao.updateCliente(Cliente(run, nombre, apellido, telefono, direccion))
        return resultado
    
    def eliminarCliente(self, run):
        resultado = self.dao.deleteCliente(run)
        return resultado
    
    # ELIMINAS cargarClientesBase() - YA NO SE NECESITA    