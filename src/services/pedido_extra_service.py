from src.database.db_mysql import get_connection
from src.models.pedido_extra_model import PedidoExtra

class PedidoExtraService():

    @staticmethod
    def insertar_extras_pedido(pedido_id, extras):
        try:
            connection = get_connection()
            for extra in extras:
                extra_id = extra['id']
                cantidad = extra['cantidad']
                sub_total_extra = extra['subtotal']
                sql = "INSERT INTO Pedido_Extra (pedido_id, extra_id, cantidad, sub_total) VALUES (?, ?, ?, ?)"
                connection.execute(sql, (
                    pedido_id, 
                    extra_id,
                    cantidad,
                    sub_total_extra,
                ))
            connection.commit()
        finally:
            connection.close()

    @classmethod
    def get_pedido_extra(cls, id):
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido_Extra WHERE pedido_id = ?"
            datos = connection.execute(sql, (id, )).fetchall()
            pedidos_extras = []
            for dato in datos:
                # Mapear por índice: (pedido_id, extra_id, cantidad, sub_total)
                _pedido_extra = PedidoExtra(dato[0], dato[1], dato[2], dato[3])
                pedidos_extras.append(_pedido_extra.to_json())
            return pedidos_extras
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def get_rank_extra(cls, date):
        try:
            connection  = get_connection()
            date_intervals ={
                'dia': "date('now', 'localhost', '-5 hours')",
                'semana': "date('now', '-7 day', 'localtime', '-5 hours')",
                'mes': "date('now', '-1 month', 'localtime', '-5 hours')",
                'año': "date('now', '-1 year', 'localtime', '-5 hours')"
            }

            date_interval = date_intervals.get(date)
            if not date_interval:
                raise ValueError("Intervalo de fecha no válido")

            sql = ""
            if date == 'dia':
                sql = """
                    SELECT e.extra_id, e.nombre, SUM(pe.cantidad) AS cantidad_ventas
                    FROM Pedido_Extra pe
                    JOIN Extra e ON pe.extra_id = e.extra_id
                    JOIN Pedido p ON pe.pedido_id = p.pedido_id
                    WHERE DATE(p.fecha_hora) = ?
                    GROUP BY pe.extra_id, e.nombre
                """
            else:
                sql = """
                    SELECT e.extra_id, e.nombre, SUM(pe.cantidad) AS cantidad_ventas
                    FROM Pedido_Extra pe
                    JOIN Extra e ON pe.extra_id = e.extra_id
                    JOIN Pedido p ON pe.pedido_id = p.pedido_id
                    WHERE DATE(p.fecha_hora) <= ?
                    GROUP BY pe.extra_id, e.nombre
                """
            datos = connection.execute(sql, ( date_interval, )).fetchall()
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
            connection.close()
