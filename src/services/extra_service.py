from src.database.db_mysql import get_connection
from src.models.extra_model import Extra
from sqlalchemy import text

class Extra_Service():

    @classmethod
    def post_extra(cls, extra):
        try:
            connection = get_connection()
            sql = text("INSERT INTO Extra (nombre, precio, imagen_url) VALUES (:nombre, :precio, :imagen_url)")
            connection.execute(sql, {
                'nombre': extra.nombre,
                'precio': extra.precio, 
                'imagen_url': extra.imagen_url
            })
            connection.commit()
            return True, 'Extra registrada'
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def get_extra(cls):
        try:
            connection = get_connection()
            sql = text("SELECT * FROM Extra")
            datos = connection.execute(sql).fetchall()
            extras = []
            for dato in datos:
                extra = Extra(dato['nombre'], dato['precio'], dato['imagen_url'], dato['extra_id'])
                extras.append(extra.to_json())
            return extras
        except Exception as ex:
            return str(ex)
        
    @classmethod
    def get_extra_by_id(cls, id):
        try:
            connection = get_connection()
            sql = text("SELECT * FROM Extra WHERE extra_id = :id")
            dato = connection.execute(sql, {'id': id}).fetchone()
            if dato:
                extra = Extra(dato['nombre'], dato['precio'], dato['imagen_url'], dato['extra_id'])
                return extra.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
        
    @classmethod
    def update_extra(cls, extra):
        try:
            connection = get_connection()
            sql = text("UPDATE Extra SET nombre = :nombre, precio = :precio, imagen_url = :imagen_url WHERE extra_id = :id")
            connection.execute(sql, {
                'nombre': extra.nombre, 
                'precio': extra.precio, 
                'imagen_url': extra.imagen_url, 
                'id': extra.id
            })
            connection.commit()
            return True, "Extra actualizada"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def delete_extra(cls, id):
        try:
            connection = get_connection()
            sql = text("DELETE FROM Extra WHERE extra_id = :id")
            connection.execute(sql, {'id': id})
            connection.commit()
            return True, "Extra eliminada"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()
