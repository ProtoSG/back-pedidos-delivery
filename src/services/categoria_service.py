from src.database.db_mysql import get_connection
from src.models.categoria_model import Categoria

class Categoria_Service():

    @classmethod
    def post_categoria(cls, categoria):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO Categoria (nombre) VALUES (%s)"
            cursor.execute(sql, (categoria.nombre))
            connection.commit()
            return True, 'Categoria registrada'
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_categoria(cls):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Categoria"
            cursor.execute(sql)
            datos = cursor.fetchall()
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
            conneciton = get_connection()
            cursor = conneciton.cursor()
            sql = "SELECT * FROM Categoria WHERE categoria_id = %s"
            cursor.execute(sql, (id))
            dato = cursor.fetchone()
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
            cursor = connection.cursor()
            sql = "UPDATE Categoria SET nombre = %s WHERE categoria_id = %s"
            cursor.execute(sql, (categoria.nombre, categoria.id))
            connection.commit()
            return True, "Categoria actualizada"
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def delete_categoria(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM Categoria WHERE categoria_id = %s"
            cursor.execute(sql, (id))
            connection.commit()
            return True, "Categoria eliminada"
        except Exception as ex:
            return False, str(ex)

    @classmethod
    def get_rank(cls, date):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            date_intervlas = {
                'dia' : 'CURDATE()',
                'semana': 'DATE_SUB(NOW(), INTERVAL 7 DAY)',
                'mes': 'DATE_SUB(NOW(), INTERVAL 1 MONTH)',
                'año': 'DATE_SUB(NOW(), INTERVAL 1 YEAR)'
            }
            date_interval = date_intervlas.get(date)

            sql = """
                SELECT c.categoria_id, c.nombre, SUM(pp.sub_total) AS total
                FROM Producto p
                JOIN Categoria c ON p.categoria_id = c.categoria_id
                JOIN Pedido_Producto pp ON p.producto_id = pp.producto_id
                JOIN Pedido pe ON pp.pedido_id = pe.pedido_id
                WHERE DATE(pe.fecha_hora) >= CURDATE()
                GROUP BY c.categoria_id, c.nombre;
            """.format(date_interval)

            cursor.execute(sql)
            datos = cursor.fetchall()
            categorias = []
            for dato in datos:
                categoria = {
                    "id" : dato[0],
                    "nombre" : dato[1],
                    "total" : dato[2]
                }
                categorias.append(categoria)
            return categorias
        except Exception as ex:
            return str(ex)
        finally:
            cursor.close()
            connection.close()