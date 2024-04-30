from src.database.db_mysql import get_connection
from src.models.producto_model import Producto
from src.services.categoria_service import Categoria_Service
from sqlalchemy import text
from sqlalchemy import select
from src.models.producto_model import Producto
from sqlalchemy.orm import Session

class Producto_Service():    
    @classmethod
    def post_producto(cls, producto):
        try:
            connection = get_connection()
            sql = text("""
                INSERT INTO Producto (nombre, categoria_id, precio, descripcion, imagen_url)
                VALUES (:nombre, :categoria_id, :precio, :descripcion, :imagen_url)
            """)
            connection.execute(sql, {
                'nombre': producto.nombre,
                'categoria_id': producto.categoria_id,
                'precio': producto.precio,
                'descripcion': producto.descripcion,
                'imagen_url': producto.imagen_url
            })
            connection.commit()
            return True, 'Producto registrado'
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def get_producto(cls):
        try:
            connection = get_connection()
            if connection is not None:
                sql = text("""
                    SELECT p.producto_id, p.nombre, p.precio, p.descripcion, p.imagen_url, c.categoria_id, c.nombre AS nombre_categoria
                    FROM Producto p
                    JOIN Categoria c ON p.categoria_id = c.categoria_id;
                """)
                
                datos = connection.execute(sql)
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
            sql = text("""
                SELECT p.producto_id, p.nombre, p.precio, p.descripcion, p.imagen_url, c.categoria_id, c.nombre AS nombre_categoria
                FROM Producto p
                JOIN Categoria c ON p.categoria_id = c.categoria_id
                WHERE p.producto_id = :id;
            """)
            dato = connection.execute(sql, {'id': id}).fetchone()
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
            sql = text("UPDATE Producto SET nombre = :nombre, precio = :precio, categoria_id = :categoria_id, descripcion = :descripcion, imagen_url = :imagen_url WHERE producto_id = :id;")
            connection.execute(sql, {
                "nombre" : producto.nombre,
                "precio" : producto.precio,
                "categoria_id" : producto.categoria_id, "descripcion" : producto.descripcion,
                "imagen_url" : producto.imagen_url,
                 "id" : producto.id,
            })
            connection.commit()
            return True, "Producto actualizado exitosamente"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()
        
    @classmethod
    def delete_producto(cls, id):
        try:
            connection = get_connection()
            sql = text("DELETE FROM Producto WHERE producto_id = :id")
            connection.execute(sql, {"id" : id})
            connection.commit()
            return True, "Producto eliminado"
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()