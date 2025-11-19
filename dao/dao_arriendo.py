from conex import conn
import traceback

class daoArriendo:
    def __init__(self):
        self.host = "localhost"
        self.user = "root" 
        self.passwd = ""
        self.database = "arriendos_db"

    def getConex(self):
        return conn.Conex(self.host, self.user, self.passwd, self.database)

    def addArriendo(self, arriendo):
        # CORREGIDO: Usar columnas correctas de la BD
        sql = """INSERT INTO arriendo (numArriendo, fechaInicio, fechaEntrega, 
                 costo_total_pesos, costo_total_uf, valor_uf_dia,
                 run_cliente, run_empleado, patente_vehiculo) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        
        mensaje = ""
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            
            # Calcular valores UF (por ahora usar valores fijos)
            costo_total_pesos = arriendo.getCostoTotal()
            costo_total_uf = round(costo_total_pesos / 35000, 2)  # Ejemplo
            valor_uf_dia = 35000  # Ejemplo
            
            cursor.execute(sql, (
                arriendo.getNumArriendo(), 
                arriendo.getFechaInicio(), 
                arriendo.getFechaEntrega(),
                costo_total_pesos,
                costo_total_uf,
                valor_uf_dia,
                arriendo.getCliente().getRun(), 
                arriendo.getEmpleado().getRun(),
                arriendo.getVehiculo().getPatente()
            ))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "✅ Arriendo registrado satisfactoriamente"
            else:
                mensaje = "ℹ️ No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "❌ Problemas con la base de datos... vuelva a intentarlo"
        finally:
            if c:
                c.closeConex()
        return mensaje

    def findArriendo(self, numArriendo):
        # CORREGIDO: Usar columnas correctas
        sql = """SELECT a.numArriendo, a.fechaInicio, a.fechaEntrega, a.costo_total_pesos,
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
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql, (numArriendo,))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            if c:
                c.closeConex()
        return resultado

    def getAllArriendos(self):
        # CORREGIDO: Usar columnas correctas
        sql = """SELECT a.numArriendo, a.fechaInicio, a.fechaEntrega, a.costo_total_pesos,
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
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()

        except Exception as ex:
            print(f"Error en getAllArriendos: {ex}")
        finally:
            if c:
                c.closeConex()
        return resultado

    # Los métodos updateArriendo y deleteArriendo se mantienen igual

    def updateArriendo(self, arriendo):
        sql = """UPDATE arriendo SET fechaInicio = %s, fechaEntrega = %s, costoTotal = %s,
                 run_cliente = %s, run_empleado = %s, patente_vehiculo = %s 
                 WHERE numArriendo = %s"""
        mensaje = ""
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql, (arriendo.getFechaInicio(), arriendo.getFechaEntrega(),
                               arriendo.getCostoTotal(), arriendo.getCliente().getRun(),
                               arriendo.getEmpleado().getRun(), arriendo.getVehiculo().getPatente(),
                               arriendo.getNumArriendo()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje = "✅ Arriendo actualizado satisfactoriamente"
            else:
                mensaje = "ℹ️ No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "❌ Problemas con la base de datos... vuelva a intentarlo"
        finally:
            if c:
                c.closeConex()
        return mensaje

    def deleteArriendo(self, numArriendo):
        sql = "DELETE FROM arriendo WHERE numArriendo = %s"
        mensaje = ""
        c = None
        try:
            c = self.getConex()
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
            if c:
                c.closeConex()
            return mensaje
    def tieneArriendosSuperpuestos(self, patente, fecha_inicio, fecha_entrega):
        """
        Verifica si el vehículo tiene arriendos superpuestos en las fechas
        """
        sql = """SELECT numArriendo FROM arriendo 
                 WHERE patente_vehiculo = %s 
                 AND ((fechaInicio BETWEEN %s AND %s) 
                      OR (fechaEntrega BETWEEN %s AND %s)
                      OR (%s BETWEEN fechaInicio AND fechaEntrega)
                      OR (%s BETWEEN fechaInicio AND fechaEntrega))"""
    
        resultado = None
        c = None
        try:
            c = self.getConex()
            cursor = c.getConex().cursor()
            cursor.execute(sql, (patente, fecha_inicio, fecha_entrega, 
                               fecha_inicio, fecha_entrega, fecha_inicio, fecha_entrega))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(f"Error verificando superposición: {ex}")
        finally:
            if c:
                c.closeConex()
        return resultado
