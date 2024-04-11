from src.database.db_mysql import get_connection
from src.models.producto_model import Producto
from src.services.categoria_service import Categoria_Service

class Producto_Service():
        
    @classmethod
    def post_producto(cls, producto):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = """INSERT INTO Producto (nombre, categoria_id, precio, descripcion, imagen_url)
                     VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql, (producto.nombre, producto.categoria_id, producto.precio, producto.descripcion, producto.imagen_url))
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
                categoria = Categoria_Service.get_categoria_by_id(fila[2])
                producto = {
                    'id': fila[0],
                    'nombre': fila[1],
                    'precio': fila[3],
                    'descripcion': fila[4],
                    'imagen_url': fila[5],
                    'categoria': categoria
                }
                productos.append(producto)
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
                categoria = Categoria_Service.get_categoria_by_id(dato[2])
                _producto = {
                    'id': dato[0],
                    'nombre': dato[1],
                    'precio': dato[3],
                    'descripcion': dato[4],
                    'imagen_url': dato[5],
                    'categoria': categoria
                }
                return _producto
            else:
                return None
        except Exception as ex:
            return str(ex)
    
    @classmethod
    def update_prodcuto(cls, producto):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "UPDATE Producto SET nombre = %s, precio = %s, categoria_id = %s, descripcion = %s, imagen_url = %s WHERE producto_id = %s;"
            cursor.execute(sql, (producto.nombre, producto.precio, producto.categoria_id, producto.descripcion, producto.imagen_url, producto.id,))
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