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
                     VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, (producto.nombre, producto.categoria_id, producto.precio, producto.descripcion, producto.imagen_url))
            connection.commit()
            return True, 'Producto registrado'
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.sync()

    @classmethod
    def get_producto(cls):
        connection = None
        cursor = None
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = """
                SELECT p.producto_id, p.nombre, p.precio, p.descripcion, p.imagen_url, c.categoria_id, c.nombre AS nombre_categoria
                FROM Producto p
                JOIN Categoria c ON p.categoria_id = c.categoria_id;
            """
            cursor.execute(sql)
            datos = cursor.fetchall()
            productos = []
            for fila in datos:
                producto = {
                    'id': fila[0],
                    'nombre': fila[1],
                    'precio': fila[2],
                    'descripcion': fila[3],
                    'imagen_url': fila[4],
                    'categoria': {
                        'id' : fila[5],
                        'nombre' : fila[6]
                    }
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
            sql = """
                SELECT p.producto_id, p.nombre, p.precio, p.descripcion, p.imagen_url, c.categoria_id, c.nombre AS nombre_categoria
                FROM Producto p
                JOIN Categoria c ON p.categoria_id = c.categoria_id
                WHERE p.producto_id = ?;
            """
            cursor.execute(sql, (id))
            dato = cursor.fetchone()
            print(dato)
            if dato:
                _producto = {
                    'id': dato[0],
                    'nombre': dato[1],
                    'precio': dato[2],
                    'descripcion': dato[3],
                    'imagen_url': dato[4],
                    'categoria': {
                        'id' : dato[5],
                        'nombre' : dato[6],
                    }
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
            sql = "UPDATE Producto SET nombre = ?, precio = ?, categoria_id = ?, descripcion = ?, imagen_url = ? WHERE producto_id = ?;"
            cursor.execute(sql, (producto.nombre, producto.precio, producto.categoria_id, producto.descripcion, producto.imagen_url, producto.id,))
            connection.commit()
            return True, "Producto actualizado exitosamente"
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.sync()
        
    @classmethod
    def delete_producto(cls, id):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "DELETE FROM Producto WHERE producto_id = ?"
            cursor.execute(sql, (id))
            connection.commit()
            return True, "Producto eliminado"
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.sync()