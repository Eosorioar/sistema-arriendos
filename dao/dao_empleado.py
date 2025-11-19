from conex import conn
import traceback

class daoEmpleado:
    def __init__(self):
        # Solo inicializar variables, NO crear conexión aquí
        self.host = "localhost"
        self.user = "root" 
        self.passwd = ""
        self.database = "arriendos_db"

    def getConex(self):
        # Crear NUEVA conexión cada vez que se necesite
        return conn.Conex(self.host, self.user, self.passwd, self.database)
    
    def addEmpleado(self, empleado):
        
        sql_persona = "INSERT INTO persona (run, nombre, apellido) VALUES (%s, %s, %s)"
        
        sql_empleado = "INSERT INTO empleado (run, codigo, cargo, password) VALUES (%s, %s, %s, %s)"
        
        
        mensaje = ""
        c = None  # Inicializar como None
        try:
            c = self.getConex()  # Nueva conexión
            cursor = c.getConex().cursor()
            
           
            cursor.execute(sql_persona, (empleado.getRun(), empleado.getNombre(), empleado.getApellido()))
            

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
            if c:
                c.closeConex()
        return mensaje

    def findEmpleado(self, run):

        sql = """SELECT p.run, p.nombre, p.apellido, e.codigo, e.cargo, e.password 
                 FROM empleado e 
                 JOIN persona p ON e.run = p.run 
                 WHERE p.run = %s"""
        resultado = None
        c = None
        try:
            c = self.getConex()  # Nueva conexión
            cursor = c.getConex().cursor()
            cursor.execute(sql, (run,))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            if c:
                c.closeConex()
        return resultado

    def updateEmpleado(self, empleado):

        sql_persona = "UPDATE persona SET nombre = %s, apellido = %s WHERE run = %s"
        sql_empleado = "UPDATE empleado SET cargo = %s, password = %s WHERE run = %s"
        

        mensaje = ""
        c = None
        try:
            c = self.getConex()  # Nueva conexión
            cursor = c.getConex().cursor()
            
            cursor.execute(sql_persona, (empleado.getNombre(), empleado.getApellido(), empleado.getRun()))
            
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
            if c:
                c.closeConex()
        return mensaje

    def deleteEmpleado(self, run):
        sql_empleado = "DELETE FROM empleado WHERE run = %s"
        sql_persona = "DELETE FROM persona WHERE run = %s"

        
        mensaje = ""
        c = None
        try:
            c = self.getConex()  # Nueva conexión
            cursor = c.getConex().cursor()
            
            cursor.execute(sql_empleado, (run,))
            cursor.execute(sql_persona, (run,))
            
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
            if c:
                c.closeConex()
        return mensaje

    def getAllEmpleados(self):
        
        sql = """SELECT p.run, p.nombre, p.apellido, e.codigo, e.cargo, e.password 
                 FROM empleado e 
                 JOIN persona p ON e.run = p.run"""
        
        resultado = None
        c = None
        try:
            c = self.getConex()  # Nueva conexión
            cursor = c.getConex().cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            if c:
                c.closeConex()
        return resultado

    def validarLogin(self, run, password):
        sql = "SELECT run, password FROM empleado WHERE run = %s"
        resultado = None
        c = None
        try:
            c = self.getConex()  # Nueva conexión
            cursor = c.getConex().cursor()
            cursor.execute(sql, (run,))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            if c:
                c.closeConex()
        return resultado