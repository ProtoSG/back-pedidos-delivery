from src.database.db_mysql import get_connection
from src.models.producto_model import Producto

class Producto_Service():
        
    @classmethod
    def post_producto(cls, producto):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = """INSERT INTO Producto (nombre, categoria_id, precio)
                     VALUES (%s, %s, %s)"""
            cursor.execute(sql, (producto.nombre, producto.categoria_id, producto.precio))
            connection.commit()  # Confirma la acción de inserción.
            return True, 'Producto registrado'
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_producto(cls):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Producto"
            cursor.execute(sql)
            datos = cursor.fetchall()
            productos = []
            for fila in datos:
                producto = Producto(fila[1], fila[2], fila[3], fila[0])
                productos.append(producto.to_json())
            return productos
        except Exception as ex:
            return str(ex)
    
    @classmethod
    def get_producto_by_id(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Producto WHERE producto_id = %s"
            cursor.execute(sql, (id))
            dato = cursor.fetchone()
            if dato:
                _producto = Producto(dato[1], dato[2], dato[3], dato[0])
                return _producto.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
    
    @classmethod
    def update_prodcuto(cls, producto):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "UPDATE Producto SET nombre = %s, precio = %s WHERE producto_id = %s;"
            cursor.execute(sql, (producto.nombre, producto.precio, producto.id))
            connection.commit()
            return True, "Producto actualizado exitosamente"
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()
        
    @classmethod
    def delete_producto(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM Producto WHERE producto_id = %s"
            cursor.execute(sql, (id))
            connection.commit()
            return True, "Producto eliminado"
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.close()