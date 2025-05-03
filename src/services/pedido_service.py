from src.database.db_mysql import get_connection
from src.services.pedido_producto_service import Pedido_Producto_Service
from src.services.pedido_extra_service import Pedido_Extra_Service
from datetime import datetime, timedelta

class Pedido_Service():

    def insertar_pedido(total, fecha_hora):
        try:
            connection = get_connection()
            sql = "INSERT INTO Pedido (total, fecha_hora) VALUES (?, ?)"
            pedido_id = connection.execute(sql, (
                total,
                fecha_hora,
            )).lastrowid
            connection.commit()
            return pedido_id
        finally:
            connection.close()

    @classmethod
    def post_pedido(cls, pedido, productos, extras):
        try:
            pedido_id = Pedido_Service.insertar_pedido(pedido.total, pedido.fecha_hora)
            Pedido_Producto_Service.insertar_productos_pedido(pedido_id, productos)
            Pedido_Extra_Service.insertar_extras_pedido(pedido_id, extras)
            
            return True, "Pedido creado exitosamente"
        except Exception as ex:
            return False, str(ex)
        
    @classmethod
    def get_pedido(cls):
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido"
            datos = connection.execute(sql).fetchall()
            pedidos = []
            for dato in datos:
                pedido = {
                    'id' : dato[0],
                    'total' : dato[1],
                    'fecha_hora' : dato[2]
                }
                pedidos.append(pedido)
            return pedidos
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def get_pedido_by_id(cls, id):
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido WHERE pedido_id = ?"
            dato = connection.execute(sql, ( id, )).fetchone()
            pedido = {}
            if dato:
                pedido = {
                    'id' : dato[0],
                    'total' : dato[1],
                    'fecha_hora' : dato[2]
                }
            return pedido
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()
    
    @classmethod
    def update_pedido(cls, pedido):
        try:
            connection = get_connection()
            sql = "UPDATE Pedido SET total = ? WHERE pedido_id = ?"
            connection.execute(sql, (
                edido.total,
                pedido.id,
            ))
            connection.commit()
            return True, "Pedido Actualizado"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def get_total_dia(cls):
        try:
            connection = get_connection()
            sql = """
                SELECT DATE(fecha_hora) AS fecha, SUM(total) AS total_ventas
                FROM Pedido
                WHERE fecha_hora >= datetime('now', '-7 day')
                GROUP BY DATE(fecha_hora);
            """
            datos = connection.execute(sql).fetchall()

            datos_dict = {fecha: valor for fecha, valor in datos}
            fechas = [datetime.now() - timedelta(days=i) for i in range(7)]
            datos_dias = [{'time': fecha.strftime('%Y-%m-%d'), 'value': datos_dict.get(fecha.strftime('%Y-%m-%d'), 0)} for fecha in fechas]
            datos_dias_ordenados = sorted(datos_dias, key=lambda x: x['time'])
            
            return datos_dias_ordenados
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def get_total_semana(cls):
        try:
            connection = get_connection()
            sql = """
                SELECT strftime('%Y-%W', fecha_hora) AS semana, SUM(total) AS total_ventas
                FROM Pedido
                GROUP BY strftime('%Y-%W', fecha_hora);
            """
            datos = connection.execute(sql).fetchall()
            datos_semanas = []
            for dato in datos:
                fecha_str = str(dato[0])
                ano = int(fecha_str[:4])
                semana = int(fecha_str[5:])
                fecha_semana = datetime.strptime(f"{ano}-W{semana}-1", "%Y-W%W-%w")
                fecha = fecha_semana.strftime("%Y-%m-%d")
                dato_semana = {
                    'time' : fecha,
                    'value' : dato[1],
                }
                datos_semanas.append(dato_semana)
            datos_semsnas_ordenados = sorted(datos_semanas, key=lambda x: x['time'])
            return datos_semsnas_ordenados
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def get_total_mes(cls):
        try:
            connection = get_connection()
            sql = """
                SELECT strftime('%Y-%m', fecha_hora) AS mes, SUM(total) AS total_ventas
                FROM Pedido
                GROUP BY strftime('%Y-%m', fecha_hora);
            """
            datos = connection.execute(sql).fetchall()
            datos_meses = []
            for dato in datos:
                fecha = f"{dato[0]}-01"
                dato_mes = {
                    'time' : fecha,
                    'value' : dato[1],
                }
                datos_meses.append(dato_mes)
            
            datos_meses_ordenados = sorted(datos_meses, key=lambda x: x['time'])

            return datos_meses_ordenados
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def get_total_ano(cls):
        try:
            connection = get_connection()
            sql = """
                SELECT strftime('%Y', fecha_hora) AS año, SUM(total) AS total_ventas
                FROM Pedido
                GROUP BY strftime('%Y', fecha_hora);
            """
            datos = connection.execute(sql).fetchall()
            datos_anos = []
            for dato in datos:
                fecha = (f"{dato[0]}-01-01")
                dato_ano = {
                    'time' : fecha,
                    'value' : dato[1],
                }
                datos_anos.append(dato_ano)

            datos_anos_ordenados = sorted(datos_anos, key=lambda x: x['time'])
            return datos_anos_ordenados
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()
