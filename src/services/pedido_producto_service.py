from src.database.db_mysql import get_connection
from src.models.pedido_producto_model import Pedido_Producto

class Pedido_Producto_Service():
    @staticmethod
    def insertar_productos_pedido(pedido_id, productos):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            for producto in productos:
                producto_id = producto['id']
                cantidad = producto['cantidad']
                sub_total_producto = producto['subtotal']
                cursor.execute("INSERT INTO Pedido_Producto (pedido_id, producto_id, cantidad, sub_total) VALUES (?, ?, ?, ?)", (pedido_id, producto_id, cantidad, sub_total_producto))
            connection.commit()
        finally:
            cursor.close()
            connection.sync()

    @classmethod
    def get_pedido_producto(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Pedido_Producto WHERE pedido_id = ?"
            cursor.execute(sql, (id))
            datos = cursor.fetchall()
            pedidos_productos = []
            for dato in datos:
                _pedido_producto = Pedido_Producto(dato[0], dato[1], dato[2], dato[3])
                pedidos_productos.append(_pedido_producto.to_json())
            return pedidos_productos
        except Exception as ex:
            return str(ex)
        finally:
            cursor.close()
            connection.sync()

    @classmethod
    def get_rank_producto(cls, date):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            date_intervals = {
                'dia': "date('now', 'localtime')",
                'semana': "date('now', '-7 day', 'localtime')",
                'mes': "date('now', '-1 month', 'localtime')",
                'año': "date('now', '-1 year', 'localtime')"
            }

            date_interval = date_intervals.get(date)

            if not date_interval:
                raise ValueError("Intervalo de fecha no válido")

            sql = """
                SELECT p.producto_id, p.nombre, COUNT(*) AS cantidad_ventas, SUM(pp.sub_total) AS total_ventas
                FROM Pedido_Producto pp
                JOIN Producto p ON pp.producto_id = p.producto_id
                JOIN Pedido pe ON pp.pedido_id = pe.pedido_id
                WHERE DATE(pe.fecha_hora) >= {}
                GROUP BY pp.producto_id, p.nombre
                ORDER BY cantidad_ventas DESC;
            """.format(date_interval)
            cursor.execute(sql)
            datos = cursor.fetchall()
            productos = []
            for dato in datos:
                producto = {
                    "producto_id" : dato[0],
                    "nombre" : dato[1],
                    "cantidad" : dato[2],
                    "total" : dato[3]
                }
                productos.append(producto)
            return productos
        except Exception as ex:
            return str(ex)
        finally:
            cursor.close()
            connection.sync()