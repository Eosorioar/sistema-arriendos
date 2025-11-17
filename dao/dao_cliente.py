from conex import conn
import traceback

class daoCliente:
    def __init__(self):
        try:
            self.__conn = conn.Conex("localhost", "root", "", "arriendos_db")
        except Exception as ex:
            print(ex)

    def getConex(self):
        return self.__conn

    def addCliente(self, cliente):
        sql_persona = "INSERT INTO persona (run, nombre, apellido) VALUES (%s, %s, %s)"
        sql_cliente = "INSERT INTO cliente (run, telefono, direccion) VALUES (%s, %s, %s)"
        
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql_persona, (cliente.getRun(), cliente.getNombre(), cliente.getApellido()))
            cursor.execute(sql_cliente, (cliente.getRun(), cliente.getTelefono(), cliente.getDireccion()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Cliente agregado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje

    def findCliente(self, run):
        
        sql = """SELECT p.run, p.nombre, p.apellido, c.telefono, c.direccion 
                 FROM cliente c 
                 JOIN persona p ON c.run = p.run 
                 WHERE p.run = %s"""
        resultado = None
        c = self.getConex()
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (run,))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            c.closeConex()
        return resultado

    def updateCliente(self, cliente):
        sql_persona = "UPDATE persona SET nombre = %s, apellido = %s WHERE run = %s"
        sql_cliente = "UPDATE cliente SET telefono = %s, direccion = %s WHERE run = %s"
        
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql_persona, (cliente.getNombre(), cliente.getApellido(), cliente.getRun()))
            cursor.execute(sql_cliente, (cliente.getTelefono(), cliente.getDireccion(), cliente.getRun()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Cliente actualizado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje

    def deleteCliente(self, run):
        sql_cliente = "DELETE FROM cliente WHERE run = %s"
        sql_persona = "DELETE FROM persona WHERE run = %s"
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql_cliente, (run,))
            cursor.execute(sql_persona, (run,))

            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Cliente eliminado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje
    
    def getAllClientes(self):
        
        sql = """SELECT p.run, p.nombre, p.apellido, c.telefono, c.direccion 
                 FROM cliente c 
                 JOIN persona p ON c.run = p.run"""
        c = self.getConex()
        resultado = None
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            c.closeConex()
        return resultado