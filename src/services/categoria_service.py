from src.database.db_mysql import get_connection
from src.models.categoria_model import Categoria

class CategoriaService:
    """
    Servicio para operaciones relacionadas con categorías.
    """

    @classmethod
    def post_categoria(cls, categoria):
        try:
            connection = get_connection()
            sql = "INSERT INTO Categoria (nombre) VALUES (?)"
            connection.execute(sql, ( categoria.nombre, ))
            connection.commit()
            return True, 'Categoria registrada'
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def get_categoria(cls):
        """
        Obtiene todas las categorías.
        Returns:
            list: Lista de categorías o mensaje de error.
        """
        try:
            connection = get_connection()
            if connection is not None:
                sql = "SELECT * FROM Categoria"
                datos = connection.execute(sql).fetchall()
                categorias = []
                for dato in datos:
                    categoria = Categoria(dato[1], dato[0])
                    categorias.append(categoria.to_json())
                return categorias
        except Exception as ex:
            return str(ex)
        
    @classmethod
    def get_categoria_by_id(cls, id):
        """
        Obtiene una categoría por su ID.
        Args:
            id (int): ID de la categoría.
        Returns:
            dict or None: Categoría encontrada o None si no existe.
        """
        try:
            connection = get_connection()
            sql = "SELECT * FROM Categoria WHERE categoria_id = (?)"
            dato = connection.execute(sql, ( id, )).fetchone()
            if dato:
                categoria = Categoria(dato[1], dato[0])
                return categoria.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
        
    @classmethod
    def update_categoria(cls, categoria):
        """
        Actualiza la información de una categoría existente.
        Args:
            categoria (Categoria): Objeto categoría con los datos actualizados.
        Returns:
            tuple: (bool, str) indicando éxito y mensaje.
        """
        try:
            connection = get_connection()
            sql = "UPDATE Categoria SET nombre = ? WHERE categoria_id = ?"
            connection.execute(sql, (
                categoria.nombre, 
                categoria.id,
            ))
            connection.commit()
            return True, "Categoria actualizada"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def delete_categoria(cls, id):
        """
        Elimina una categoría por su ID.
        Args:
            id (int): ID de la categoría a eliminar.
        Returns:
            tuple: (bool, str) indicando éxito y mensaje.
        """
        try:
            connection = get_connection()
            sql = "DELETE FROM Categoria WHERE categoria_id = (?)"
            connection.execute(sql, (id, ))
            connection.commit()
            return True, "Categoria eliminada"
        except Exception as ex:
            return False, str(ex)

    @classmethod
    def get_rank(cls, date):
        try:
            connection = get_connection()
            date_intervals = {
                'dia': "date('now', 'localhost', '-5 hours')",
                'semana': "date('now', '-7 day', 'localtime', '-5 hours')",
                'mes': "date('now', '-1 month', 'localtime', '-5 hours')",
                'año': "date('now', '-1 year', 'localtime', '-5 hours')"
            }
            date_interval = date_intervals.get(date)

            sql = """
                SELECT c.categoria_id, c.nombre, SUM(pp.sub_total) AS total
                FROM Producto p
                JOIN Categoria c ON p.categoria_id = c.categoria_id
                JOIN PedidoProducto pp ON p.producto_id = pp.producto_id
                JOIN Pedido pe ON pp.pedido_id = pe.pedido_id
                WHERE DATE(pe.fecha_hora) <= ?
                GROUP BY c.categoria_id, c.nombre;
            """
            
            datos = connection.execute(sql, ( date_interval, )).fetchall()
            categorias = []
            for dato in datos:
                categoria = {
                    "id": dato[0],
                    "nombre": dato[1],
                    "total": dato[2]
                }
                categorias.append(categoria)
            return categorias
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()
