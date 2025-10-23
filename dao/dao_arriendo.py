from conex import conn
import traceback

class daoArriendo:
    def __init__(self):
        try:
            self.__conn = conn.Conex("localhost", "root", "", "arriendos_db")
        except Exception as ex:
            print(ex)

    def getConex(self):
        return self.__conn

    def addArriendo(self, arriendo):
        sql = """INSERT INTO arriendo (numArriendo, fechaInicio, fechaEntrega, costoTotal, 
                 run_cliente, run_empleado, patente_vehiculo) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (arriendo.getNumArriendo(), arriendo.getFechaInicio(), 
                               arriendo.getFechaEntrega(), arriendo.getCostoTotal(),
                               arriendo.getCliente().getRun(), arriendo.getEmpleado().getRun(),
                               arriendo.getVehiculo().getPatente()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "Arriendo registrado satisfactoriamente"
            else:
                mensaje = "No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje

    def findArriendo(self, numArriendo):
        sql = """SELECT a.numArriendo, a.fechaInicio, a.fechaEntrega, a.costoTotal,
                    pc.run as cliente_run, pc.nombre as cliente_nombre, pc.apellido as cliente_apellido,
                    pe.run as empleado_run, pe.nombre as empleado_nombre, pe.apellido as empleado_apellido,
                    v.patente, v.marca, v.modelo
                FROM arriendo a
                JOIN cliente c ON a.run_cliente = c.run
                JOIN persona pc ON c.run = pc.run
                JOIN empleado e ON a.run_empleado = e.run  
                JOIN persona pe ON e.run = pe.run
                JOIN vehiculo v ON a.patente_vehiculo = v.patente
                WHERE a.numArriendo = %s"""
        resultado = None
        c = self.getConex()
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (numArriendo,))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            c.closeConex()
        return resultado

    def getAllArriendos(self):
        sql = """SELECT a.numArriendo, a.fechaInicio, a.fechaEntrega, a.costoTotal,
                pc.run as cliente_run, pc.nombre as cliente_nombre, pc.apellido as cliente_apellido,
                pe.run as empleado_run, pe.nombre as empleado_nombre, pe.apellido as empleado_apellido,
                v.patente, v.marca, v.modelo
            FROM arriendo a
            JOIN cliente c ON a.run_cliente = c.run
            JOIN persona pc ON c.run = pc.run
            JOIN empleado e ON a.run_empleado = e.run  
            JOIN persona pe ON e.run = pe.run
            JOIN vehiculo v ON a.patente_vehiculo = v.patente"""
        
        resultado = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
            cursor.close()
        except Exception as ex:
            print(f"Error en getAllArriendos: {ex}")
        finally:
            if 'c' in locals() and c:
                c.closeConex()
        return resultado
    
    def deleteArriendo(self, numArriendo):
        sql = "DELETE FROM arriendo WHERE numArriendo = %s"
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (numArriendo,))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "✅ Arriendo eliminado satisfactoriamente"
            else:
                mensaje = "ℹ️ No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "❌ Problemas con la base de datos... vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje
    