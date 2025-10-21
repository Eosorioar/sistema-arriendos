from conex import conn
import traceback

class daoUser:
    def __init__(self):
        try:
            self.__conn = conn.Conex("localhost", "root", "", "arriendos_db")
        except Exception as ex:
            print(ex)

    def getConex(self):
        return self.__conn
    
    def cargaUsuariosBase(self):
        c = self.getConex()
        result = None
        try:
            cursor = c.getConex().cursor()
            cursor.execute("select username, email, password, create_time from user")
            result = cursor.fetchall()
        except Exception as ex:
            print(ex)
        finally:
            c.closeConex()
        return result
    
    def buscarUsuario(self, user):
        sql = "select username, email, password, create_time from user where username = %s"
        resultado = None
        c = self.getConex()

        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (user.getUsername(),))
            #fetchone, rescata del cursor una sola fila (tupla)
            resultado = cursor.fetchone()

        except Exception as ex:
            print(traceback.print_exc())
        finally:
            c.closeConex()
        return resultado

    def validarLogin(self,user):
        sql = "select username, password from user where username = %s"
        resultado = None
        c = self.getConex()
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (user.getUsername(),))
            resultado = cursor.fetchone()
        except Exception as ex:
            print(traceback.print_exc())
        finally:
            c.closeConex()
        
        return resultado
    def actualizarUsuario(self, user):
        sql = "update user set email=%s, password = %s where username = %s"
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (user.getEmail(), user.getPassword(), user.getUsername()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje ="Datos modificados satisfactoriamente"
            else:
                mensaje="No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos..vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje
    def eliminarUsuario(self, user):
        sql = "delete from user  where username = %s"
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (user.getUsername(),))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje ="Usuario eliminado satisfactoriamente"
            else:
                mensaje="No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos..vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje
    def agregarUsuario(self,user):
        sql = "insert into user (username, email, password, create_time) values (%s,%s,%s,%s)"
        c = self.getConex()
        mensaje = ""
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (user.getUsername(),user.getEmail(), user.getPassword(),user.getCreate_time()))
            c.getConex().commit()
            filas = cursor.rowcount
            if filas > 0:
                mensaje ="Datos agregados satisfactoriamente"
            else:
                mensaje="No se realizaron cambios"
        except Exception as ex:
            print(traceback.print_exc())
            mensaje = "Problemas con la base de datos..vuelva a intentarlo"
        finally:
            c.closeConex()
        return mensaje



