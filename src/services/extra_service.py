from src.database.db_mysql import get_connection
from src.models.extra_model import Extra

class Extra_Service():

    @classmethod
    def post_extra(cls, extra):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO Extra (nombre, precio) VALUES (%s, %s)"
            cursor.execute(sql, (extra.nombre, extra.precio))
            connection.commit()
            return True, 'Extra registrada'
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_extra(cls):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Extra"
            cursor.execute(sql)
            datos = cursor.fetchall()
            extras = []
            for dato in datos:
                extra = Extra(dato[1], dato[2], dato[0])
                extras.append(extra.to_json())
            return extras
        except Exception as ex:
            return str(ex)
        
    @classmethod
    def get_extra_by_id(cls, id):
        try:
            conneciton = get_connection()
            cursor = conneciton.cursor()
            sql = "SELECT * FROM Extra WHERE extra_id = %s"
            cursor.execute(sql, (id))
            dato = cursor.fetchone()
            if dato:
                extra = Extra(dato[1], dato[2], dato[0])
                return extra.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
        
    @classmethod
    def update_extra(cls, extra):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "UPDATE Extra SET nombre = %s, precio = %s WHERE extra_id = %s"
            cursor.execute(sql, (extra.nombre, extra.precio, extra.id))
            connection.commit()
            return True, "Extra actualizada"
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete_extra(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM Extra WHERE extra_id = %s"
            cursor.execute(sql, (id))
            connection.commit()
            return True, "Extra eliminada"
        except Exception as ex:
            return False, str(ex)
