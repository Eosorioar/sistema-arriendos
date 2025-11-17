from modelo.cliente import Cliente
from dao.dao_cliente import daoCliente

class ClienteDTO:
    def __init__(self):
        self.dao = daoCliente()
    
    def listarClientes(self):
        resultado = self.dao.getAllClientes()
        clientes = []
        if resultado is not None:
            for cli in resultado:
                
                cliente = Cliente(
                    run=cli[0],
                    nombre=cli[1], 
                    apellido=cli[2],
                    telefono=cli[3], 
                    direccion=cli[4]
                )
                clientes.append(cliente)
        return clientes
    
    def buscarCliente(self, cliente):
        resultado = self.dao.findCliente(cliente.getRun())
        if resultado:
           
            cliente_encontrado = Cliente(
                run=resultado[0],
                nombre=resultado[1], 
                apellido=resultado[2],
                telefono=resultado[3], 
                direccion=resultado[4]
            )
            return cliente_encontrado
        return None
    
    def agregarCliente(self, cliente):
        resultado = self.dao.addCliente(cliente)
        return resultado
    
    def actualizarCliente(self, cliente):
        resultado = self.dao.updateCliente(cliente)
        return resultado
    
    def eliminarCliente(self, cliente):
        resultado = self.dao.deleteCliente(cliente.getRun())
        return resultado