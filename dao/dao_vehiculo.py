from conex import conn
import traceback

class daoVehiculo:
    def __init__(self):
        try:
            self.__conn = conn.Conex("localhost", "root", "", "arriendos_db")
        except Exception as ex:
            print(ex)

    def getConex(self):
        return self.__conn

    def addVehiculo(self, vehiculo):
        sql = "INSERT INTO vehiculo (patente, marca, modelo, año, precio, disponible) VALUES (%s, %s, %s, %s, %s, %s)"
        c = self.getConex()
        mensaje = ""
        try:
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
            c.closeConex()
        return mensaje

    def findVehiculo(self, patente):
        sql = "SELECT patente, marca, modelo, año, precio, disponible FROM vehiculo WHERE patente = %s"
        resultado = None
        c = self.getConex()
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (patente,))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            c.closeConex()
        return resultado

    def updateVehiculo(self, vehiculo):
        sql = "UPDATE vehiculo SET marca = %s, modelo = %s, año = %s, precio = %s, disponible = %s WHERE patente = %s"
        c = self.getConex()
        mensaje = ""
        try:
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
            c.closeConex()
        return mensaje

    def deleteVehiculo(self, patente):
        sql = "DELETE FROM vehiculo WHERE patente = %s"
        c = self.getConex()
        mensaje = ""
        try:
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
            c.closeConex()
        return mensaje

    def getAllVehiculos(self):
        c = self.getConex()
        resultado = None
        try:
            cursor = c.getConex().cursor()
            cursor.execute("SELECT patente, marca, modelo, año, precio, disponible FROM vehiculo")
            resultado = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            c.closeConex()
        return resultado

    def getVehiculosDisponibles(self):
        c = self.getConex()
        resultado = None
        try:
            cursor = c.getConex().cursor()
            cursor.execute("SELECT patente, marca, modelo, año, precio, disponible FROM vehiculo WHERE disponible = 'disponible'")
            resultado = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            c.closeConex()
        return resultado