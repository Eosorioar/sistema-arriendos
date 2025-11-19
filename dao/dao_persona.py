from conex import conn
import traceback

class daoPersona:
    def __init__(self):
        try:
            self.__conn = conn.Conex("localhost", "root", "", "arriendos_db")
        except Exception as ex:
            print(ex)

    def getConex(self):
        return self.__conn

    def existePersona(self, run):
        sql = "SELECT run FROM persona WHERE run = %s"
        c = self.getConex()
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (run,))
            resultado = cursor.fetchone()
            return resultado is not None
        except Exception as ex:
            print(traceback.print_exc())
            return False
        finally:
            c.closeConex()

    def existePersona(self, run):
        """

        Verifica si una persona existe (en cualquier tabla)
        """
        sql = "SELECT run FROM persona WHERE run = %s"
        c = self.getConex()
        try:
            cursor = c.getConex().cursor()
            cursor.execute(sql, (run,))
            resultado = cursor.fetchone()
            return resultado is not None
        except Exception as ex:
            print(traceback.print_exc())
            return False
        finally:
            c.closeConex()