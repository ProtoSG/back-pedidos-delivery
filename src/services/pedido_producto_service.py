from src.database.db_mysql import get_connection
from src.models.pedido_producto_model import PedidoProducto

class PedidoProductoService():
    @staticmethod
    def insertar_productos_pedido(pedido_id, productos):
        """
        Inserta los productos asociados a un pedido en la base de datos.

        Args:
            pedido_id: ID del pedido al que pertenecen los productos
            productos: Lista de diccionarios con información de productos
                       Cada producto debe tener: producto_id, cantidad, sub_total

        Returns:
            bool: True si la inserción fue exitosa, False en caso contrario
        """
        connection = None
        try:
            if not pedido_id:
                print("ERROR: ID de pedido inválido o no proporcionado")
                return False

            if not productos or not isinstance(productos, list):
                print("ERROR: Productos inválidos o vacíos")
                return False

            connection = get_connection()
            print(f"INFO: Insertando {len(productos)} productos para pedido #{pedido_id}")

            for i, producto in enumerate(productos):
                try:
                    # Extraer datos del producto
                    producto_id = producto.get('producto_id')
                    cantidad = producto.get('cantidad')
                    sub_total = producto.get('sub_total')

                    # Validar datos requeridos
                    if not all([producto_id, cantidad is not None, sub_total is not None]):
                        missing_fields = []
                        if not producto_id: missing_fields.append('producto_id')
                        if cantidad is None: missing_fields.append('cantidad')
                        if sub_total is None: missing_fields.append('sub_total')

                        print(f"ERROR: Datos incompletos en producto #{i+1}: faltan {', '.join(missing_fields)}")
                        continue

                    # Insertar en la base de datos
                    sql = "INSERT INTO Pedido_Producto (pedido_id, producto_id, cantidad, sub_total) VALUES (?, ?, ?, ?)"
                    connection.execute(sql, (
                        pedido_id,
                        producto_id,
                        cantidad,
                        sub_total
                    ))
                    print(f"INFO: Producto #{producto_id} agregado al pedido #{pedido_id}")

                except Exception as e:
                    print(f"ERROR: No se pudo insertar producto #{i+1}: {str(e)}")
                    connection.rollback()
                    return False

            # Confirmar todos los cambios
            connection.commit()
            print(f"INFO: {len(productos)} productos insertados exitosamente para pedido #{pedido_id}")
            return True

        except Exception as e:
            print(f"ERROR al insertar productos: {str(e)}")
            if connection:
                connection.rollback()
            return False

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_pedido_producto(cls, id):
        """
        Recupera todos los productos asociados a un pedido.

        Args:
            id: ID del pedido

        Returns:
            list: Lista de productos asociados al pedido
        """
        connection = None
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido_Producto WHERE pedido_id = ?"
            datos = connection.execute(sql, (id, )).fetchall()

            pedidos_productos = []
            for dato in datos:
                # dato: (pedido_id, producto_id, cantidad, sub_total)
                _pedido_producto = PedidoProducto(dato[0], dato[1], dato[2], dato[3])
                pedidos_productos.append(_pedido_producto.to_json())

            return pedidos_productos

        except Exception as ex:
            print(f"ERROR al recuperar productos del pedido: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_rank_producto(cls, date):
        """
        Obtiene un ranking de productos vendidos en un período de tiempo.

        Args:
            date: Período de tiempo ('dia', 'semana', 'mes', 'año')

        Returns:
            list: Lista de productos ordenados por ventas
        """
        connection = None
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
                datos = connection.execute(sql, (date_interval, )).fetchall()

            productos = []
            for dato in datos:
                producto = {
                    "producto_id": dato[0],
                    "nombre": dato[1],
                    "cantidad": dato[2],
                    "total": dato[3]
                }
                productos.append(producto)

            return productos

        except Exception as ex:
            print(f"ERROR al obtener ranking de productos: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()
