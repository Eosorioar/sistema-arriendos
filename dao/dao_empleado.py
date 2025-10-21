from conex import conn
import traceback

class daoEmpleado:
    def __init__(self):
        try:
            self.__conn = conn.Conex("localhost", "root", "", "arriendos_db")
        except Exception as ex:
            print(ex)

    def getConex(self):
        return self.__conn
    
    def addEmpleado(self, empleado):
        # PRIMERO insertar en persona
        sql_persona = "INSERT INTO persona (run, nombre, apellido) VALUES (%s, %s, %s)"
        # LUEGO insertar en empleado
        sql_empleado = "INSERT INTO empleado (run, codigo, cargo, password) VALUES (%s, %s, %s, %s)"
        
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            
            # 1. Insertar en tabla persona
            cursor.execute(sql_persona, (empleado.getRun(), empleado.getNombre(), empleado.getApellido()))
            
            # 2. Insertar en tabla empleado
            cursor.execute(sql_empleado, (empleado.getRun(), empleado.getCodigo(), empleado.getCargo(), empleado.getPassword()))
            
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Empleado agregado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje

    def findEmpleado(self, run):
        # JOIN para obtener datos de persona y empleado
        sql = """SELECT p.run, p.nombre, p.apellido, e.codigo, e.cargo, e.password 
                 FROM empleado e 
                 JOIN persona p ON e.run = p.run 
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

    def updateEmpleado(self, empleado):
        # Actualizar ambas tablas
        sql_persona = "UPDATE persona SET nombre = %s, apellido = %s WHERE run = %s"
        sql_empleado = "UPDATE empleado SET cargo = %s, password = %s WHERE run = %s"
        
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            # Actualizar persona
            cursor.execute(sql_persona, (empleado.getNombre(), empleado.getApellido(), empleado.getRun()))
            # Actualizar empleado
            cursor.execute(sql_empleado, (empleado.getCargo(), empleado.getPassword(), empleado.getRun()))
            
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Empleado actualizado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje

    def deleteEmpleado(self, run):
        # Al tener CASCADE, eliminar de empleado elimina también de persona
        sql = "DELETE FROM empleado WHERE run = %s"
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (run,))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Empleado eliminado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje

    def getAllEmpleados(self):
        # JOIN para obtener todos los empleados
        sql = """SELECT p.run, p.nombre, p.apellido, e.codigo, e.cargo, e.password 
                 FROM empleado e 
                 JOIN persona p ON e.run = p.run"""
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

    def validarLogin(self, run, password):
        sql = "SELECT run, password FROM empleado WHERE run = %s"
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