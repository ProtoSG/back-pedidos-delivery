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
                cursor.execute("INSERT INTO Pedido_Extra (pedido_id, extra_id, cantidad, sub_total) VALUES (%s, %s, %s, %s)", (pedido_id, extra_id, cantidad, sub_total_extra))
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_pedido_extra(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Pedido_Extra WHERE pedido_id = %s"
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
            connection.close()