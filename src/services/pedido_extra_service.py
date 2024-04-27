from src.database.db_mysql import get_connection
from src.models.pedido_extra_model import Pedido_Extra
class Pedido_Extra_Service():
    def insertar_extras_pedido(pedido_id, extras):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            for extra in extras:
                extra_id = extra['id']
                cantidad = extra['cantidad']
                sub_total_extra = extra['subtotal']
                cursor.execute("INSERT INTO Pedido_Extra (pedido_id, extra_id, cantidad, sub_total) VALUES (?, ?, ?, ?)", (pedido_id, extra_id, cantidad, sub_total_extra))
            connection.commit()
        finally:
            cursor.close()
            connection.sync()

    @classmethod
    def get_pedido_extra(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Pedido_Extra WHERE pedido_id = ?"
            cursor.execute(sql, (id))
            datos = cursor.fetchall()
            pedidos_extras = []
            for dato in datos:
                _pedido_extra = Pedido_Extra(dato[0], dato[1], dato[2], dato[3])
                pedidos_extras.append(_pedido_extra.to_json())
            return pedidos_extras
        except Exception as ex:
            return str(ex)
        finally:
            cursor.close()
            connection.sync()

    @classmethod
    def get_rank_extra(cls, date):
        try:
            connection  = get_connection()
            cursor = connection.cursor()
            date_intervals = {
                'dia': 'CURDATE()',
                'semana': 'DATE_SUB(NOW(), INTERVAL 7 DAY)',
                'mes': 'DATE_SUB(NOW(), INTERVAL 1 MONTH)',
                'año': 'DATE_SUB(NOW(), INTERVAL 1 YEAR)'
            }

            date_interval = date_intervals.get(date)
            if not date_interval:
                raise ValueError("Intervalo de fecha no válido")

            sql = """
                SELECT e.extra_id, e.nombre, SUM(pe.cantidad) AS cantidad_ventas
                FROM Pedido_Extra pe
                JOIN Extra e ON pe.extra_id = e.extra_id
                JOIN Pedido p ON pe.pedido_id = p.pedido_id
                WHERE DATE(p.fecha_hora) >= {}
                GROUP BY pe.extra_id, e.nombre
            """.format(date_interval)

            cursor.execute(sql)
            datos = cursor.fetchall()
            extras = []
            for dato in datos:
                extra = {
                    "extra_id" : dato[0],
                    "nombre" : dato[1],
                    "cantidad" : dato[2]
                }
                extras.append(extra)
            return extras
        except Exception as ex:
            return str(ex)
        finally:
            cursor.close()
            connection.sync()
            