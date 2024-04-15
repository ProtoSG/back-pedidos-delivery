from src.database.db_mysql import get_connection

class Pedido_Service():
    @classmethod
    def post_pedido(cls, pedido):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO Pedido (total, fecha_hora) VALUES (%s, %s)"
            cursor.execute(sql, (pedido.total, pedido.fecha_hora))
            connection.commit()
            return True, 'Pedido registrado'
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()
        
    @classmethod
    def get_pedido(cls):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Pedido"
            cursor.execute(sql)
            datos = cursor.fetchall()
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
            cursor.close()
            connection.close()
    
    @classmethod
    def get_pedido_by_id(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Pedido WHERE pedido_id = %s"
            cursor.execute(sql, (id))
            dato = cursor.fetchone()
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
            cursor.close()
            connection.close()
    
    @classmethod
    def update_pedido(cls, pedido):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "UPDATE Pedido SET total = %s WHERE pedido_id = %s"
            cursor.execute(sql, (pedido.total, pedido.id))
            connection.commit()
            return True, "Pedido Actualizado"
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()
            
        

