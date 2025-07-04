from src.database.db_mysql import get_connection
from src.models.extra_model import Extra

class ExtraService:
    """
    Servicio para operaciones relacionadas con extras.
    """

    @classmethod
    def post_extra(cls, extra):
        try:
            connection = get_connection()
            sql = "INSERT INTO Extra (nombre, precio, imagen_url) VALUES (?, ?, ?)"
            connection.execute(sql, (
                extra.nombre,
                extra.precio,
                extra.imagen_url,
            ))
            connection.commit()
            return True, 'Extra registrada'
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def get_extra(cls):
        """
        Obtiene todos los extras.
        Returns:
            list: Lista de extras o mensaje de error.
        """
        try:
            connection = get_connection()
            sql = "SELECT * FROM Extra"
            datos = connection.execute(sql).fetchall()
            print("DATOS: ", datos)
            extras = []
            for dato in datos:
                extra = Extra(dato[1], dato[2], dato[3], dato[0])
                extras.append(extra.to_json())
            return extras
        except Exception as ex:
            return str(ex)

    @classmethod
    def get_extra_by_id(cls, id):
        """
        Obtiene un extra por su ID.
        Args:
            id (int): ID del extra.
        Returns:
            dict or None: Extra encontrado o None si no existe.
        """
        try:
            connection = get_connection()
            sql = "SELECT * FROM Extra WHERE extra_id = (?)"
            dato = connection.execute(sql, ( id, )).fetchone()
            if dato:
                extra = Extra(dato[1], dato[2], dato[3], dato[0])
                return extra.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)

    @classmethod
    def update_extra(cls, extra):
        """
        Actualiza la información de un extra existente.
        Args:
            extra (Extra): Objeto extra con los datos actualizados.
        Returns:
            tuple: (bool, str) indicando éxito y mensaje.
        """
        try:
            connection = get_connection()
            sql = "UPDATE Extra SET nombre = ?, precio = ?, imagen_url = ? WHERE extra_id = ?"
            connection.execute(sql, (
                extra.nombre,
                extra.precio,
                extra.imagen_url,
                extra.id,
            ))
            connection.commit()
            return True, "Extra actualizada"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def delete_extra(cls, id):
        """
        Elimina un extra por su ID.
        Args:
            id (int): ID del extra a eliminar.
        Returns:
            tuple: (bool, str) indicando éxito y mensaje.
        """
        try:
            connection = get_connection()
            sql = "DELETE FROM Extra WHERE extra_id = (?)"
            connection.execute(sql, ( id, ))
            connection.commit()
            return True, "Extra eliminada"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()
