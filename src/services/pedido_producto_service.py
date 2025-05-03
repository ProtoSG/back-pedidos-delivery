from src.database.db_mysql import get_connection
from src.models.pedido_producto_model import Pedido_Producto

class Pedido_Producto_Service():

    def insertar_productos_pedido(pedido_id, productos):
        print("insertar")
        try:
            connection = get_connection()
            for producto in productos:
                producto_id = producto['id']
                cantidad = producto['cantidad']
                sub_total_producto = producto['subtotal']
                sql = "INSERT INTO Pedido_Producto (pedido_id, producto_id, cantidad, sub_total) VALUES (?, ?, ?, ?)"
                connection.execute(sql, (
                    pedido_id,
                    producto_id,
                    cantidad,
                    sub_total_producto,
                ))
            connection.commit()
        finally:
            connection.close()

    @classmethod
    def get_pedido_producto(cls, id):
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido_Producto WHERE pedido_id = ?"
            datos = connection.execute(sql, (id, )).fetchall()
            pedidos_productos = []
            for dato in datos:
                _pedido_producto = Pedido_Producto(dato['pedido_id'], dato['producto_id'], dato['cantidad'], dato['sub_total'])
                pedidos_productos.append(_pedido_producto.to_json())
            return pedidos_productos
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def get_rank_producto(cls, date):
        try:
            connection = get_connection()
            date_intervals = {
                'dia': "date('now', 'localhost', '-5 hours')",
                'semana': "date('now', '-7 day', 'localtime', '-5 hours')",
                'mes': "date('now', '-1 month', 'localtime', '-5 hours')",
                'año': "date('now', '-1 year', 'localtime', '-5 hours')"
            }

            date_interval = date_intervals.get(date)
            if not date_interval:
                raise ValueError("Intervalo de fecha no válido")

            sql = ""
            datos = []
            if date == 'dia':
                sql = """
                    SELECT p.producto_id, p.nombre, COUNT(*) AS cantidad_ventas, SUM(pp.sub_total) AS total_ventas
                    FROM Pedido_Producto pp
                    JOIN Producto p ON pp.producto_id = p.producto_id
                    JOIN Pedido pe ON pp.pedido_id = pe.pedido_id
                    WHERE DATE(pe.fecha_hora) = date('now', 'localtime', '-5 hours')
                    GROUP BY pp.producto_id, p.nombre
                    ORDER BY cantidad_ventas DESC;
                """
                datos = connection.execute(sql).fetchall()
            else:
                sql = """
                    SELECT p.producto_id, p.nombre, COUNT(*) AS cantidad_ventas, SUM(pp.sub_total) AS total_ventas
                    FROM Pedido_Producto pp
                    JOIN Producto p ON pp.producto_id = p.producto_id
                    JOIN Pedido pe ON pp.pedido_id = pe.pedido_id
                    WHERE DATE(pe.fecha_hora) <= ?
                    GROUP BY pp.producto_id, p.nombre
                    ORDER BY cantidad_ventas DESC;
                """
                datos = connection.execute(sql, ( date_interval, )).fetchall()
            print("RANK: ", datos)
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
            connection.close()
