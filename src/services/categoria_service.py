from src.database.db_mysql import get_connection
from src.models.categoria_model import Categoria
from sqlalchemy import text

class Categoria_Service():

    @classmethod
    def post_categoria(cls, categoria):
        try:
            connection = get_connection()
            sql = text("INSERT INTO Categoria (nombre) VALUES (:nombre)")
            connection.execute(sql, {'nombre' : categoria.nombre})
            connection.commit()
            return True, 'Categoria registrada'
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def get_categoria(cls):
        try:
            connection = get_connection()
            if connection is not None:
                sql = text("SELECT * FROM Categoria")
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
        try:
            connection = get_connection()
            sql = text("SELECT * FROM Categoria WHERE categoria_id = :id")
            dato = connection.execute(sql, {
                "id" : id
            }).fetchone()
            if dato:
                categoria = Categoria(dato[1], dato[0])
                return categoria.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
        
    @classmethod
    def update_categoria(cls, categoria):
        try:
            connection = get_connection()
            sql = text("UPDATE Categoria SET nombre = :nombre WHERE categoria_id = :categoria_id")
            connection.execute(sql, {
                "nombre" : categoria.nombre, 
                "categoria_id" : categoria.id
            })
            connection.commit()
            return True, "Categoria actualizada"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def delete_categoria(cls, id):
        try:
            connection = get_connection()
            sql = text("DELETE FROM Categoria WHERE categoria_id = :id")
            connection.execute(sql, {"id" : id})
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

            sql = text("""
                SELECT c.categoria_id, c.nombre, SUM(pp.sub_total) AS total
                FROM Producto p
                JOIN Categoria c ON p.categoria_id = c.categoria_id
                JOIN Pedido_Producto pp ON p.producto_id = pp.producto_id
                JOIN Pedido pe ON pp.pedido_id = pe.pedido_id
                WHERE DATE(pe.fecha_hora) <= :date_interval
                GROUP BY c.categoria_id, c.nombre;
            """)
            
            datos = connection.execute(sql, {'date_interval': date_interval}).fetchall()
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