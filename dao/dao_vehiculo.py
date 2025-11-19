from conex import conn
import traceback

class daoVehiculo:
    def __init__(self):
        # Solo inicializar variables, NO crear conexión aquí
        self.host = "localhost"
        self.user = "root" 
        self.passwd = ""
        self.database = "arriendos_db"

    def getConex(self):
        # Crear NUEVA conexión cada vez que se necesite
        return conn.Conex(self.host, self.user, self.passwd, self.database)

    def addVehiculo(self, vehiculo):
        sql = "INSERT INTO vehiculo (patente, marca, modelo, año, precio_uf, disponible) VALUES (%s, %s, %s, %s, %s, %s)"
        mensaje = ""
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql, (vehiculo.getPatente(), vehiculo.getMarca(), vehiculo.getModelo(), 
                               vehiculo.getAño(), vehiculo.getPrecio(), vehiculo.getDisponible()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Vehículo agregado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            if c:
                c.closeConex()
        return mensaje

    def findVehiculo(self, patente):
        sql = "SELECT patente, marca, modelo, año, precio_uf, disponible FROM vehiculo WHERE patente = %s"
        resultado = None
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql, (patente,))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            if c:
                c.closeConex()
        return resultado

    def updateVehiculo(self, vehiculo):
        sql = "UPDATE vehiculo SET marca = %s, modelo = %s, año = %s, precio_uf = %s, disponible = %s WHERE patente = %s"
        mensaje = ""
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql, (vehiculo.getMarca(), vehiculo.getModelo(), vehiculo.getAño(), 
                               vehiculo.getPrecio(), vehiculo.getDisponible(), vehiculo.getPatente()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Vehículo actualizado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            if c:
                c.closeConex()
        return mensaje

    def deleteVehiculo(self, patente):
        sql = "DELETE FROM vehiculo WHERE patente = %s"
        
        mensaje = ""
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql, (patente,))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Vehículo eliminado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            if c:
                c.closeConex()
        return mensaje

    def getAllVehiculos(self):

        resultado = None
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute("SELECT patente, marca, modelo, año, precio_uf, disponible FROM vehiculo")
            resultado = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            if c:
                c.closeConex()
        return resultado

    def getVehiculosDisponibles(self):

        resultado = None
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute("SELECT patente, marca, modelo, año, precio_uf, disponible FROM vehiculo WHERE disponible IN ('disponible', 'reservado')")
            resultado = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            if c:
                c.closeConex()
        return resultado