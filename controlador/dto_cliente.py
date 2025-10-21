from modelo.cliente import Cliente
from dao.dao_cliente import daoCliente

class ClienteDTO:
    def __init__(self):
        self.dao = daoCliente()
    
    def cargarClientesBase(self):
        resultado = self.dao.getAllClientes()
        if resultado is not None:
            for cli in resultado:
                # ✅ CORREGIDO - los índices ahora son correctos
                cliente = Cliente(run=cli[0], nombre=cli[1], apellido=cli[2], 
                                telefono=cli[3], direccion=cli[4])
                cliente.getListaClientes().append(cliente)
    
    def listarClientes(self):
        cliente = Cliente("", "", "", "", "")
        return cliente.getListaClientes()
    
    def buscarCliente(self, run):
        resultado = self.dao.findCliente(run)
        if resultado:
            # ✅ CORREGIDO - índices correctos
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