from src.database.db_mysql import get_connection
from src.services.pedido_producto_service import PedidoProductoService
from src.services.pedido_extra_service import PedidoExtraService
from src.services.notificacion_service import NotificacionService
from src.models.pedido_model import Pedido
from datetime import datetime, timedelta
import traceback

class PedidoService():
    """
    Servicio para operaciones relacionadas con pedidos.
    """

    @classmethod
    def post_pedido(cls, pedido, productos, extras):
        """
        Crea un pedido completo con sus productos y extras utilizando una transacción.
        Asegura que todas las operaciones de inserción se realizan como una unidad atómica.
        Si cualquier parte falla, toda la transacción se revierte.
        Args:
            pedido (Pedido): Objeto con los datos del pedido
            productos (list): Lista de productos a agregar
            extras (list): Lista de extras a agregar
        Returns:
            tuple: (bool, str, int) con éxito, mensaje y ID del pedido
        """
        connection = None
        try:
            # Validaciones básicas
            if pedido is None:
                return False, "El objeto pedido es inválido", None

            if not hasattr(pedido, 'usuario_id') or not pedido.usuario_id:
                return False, "Se requiere un usuario para el pedido", None

            if not productos or not isinstance(productos, list):
                return False, "Se requiere al menos un producto", None

            print(f"INFO: Iniciando transacción para crear pedido - Usuario: {pedido.usuario_id}, Total: {pedido.total}")

            # Obtener conexión e iniciar transacción
            connection = get_connection()

            # En SQLite, las transacciones se inician automáticamente con BEGIN
            # y se confirman con COMMIT o se revierten con ROLLBACK

            # Insertar el pedido principal
            sql = "INSERT INTO Pedido (usuario_id, total, fecha_hora, estado) VALUES (?, ?, ?, ?)"

            # Convertir los valores a tipos apropiados para SQLite
            usuario_id = int(pedido.usuario_id) if pedido.usuario_id else None
            total = float(pedido.total) if pedido.total else 0.0
            fecha_hora = str(pedido.fecha_hora) if pedido.fecha_hora else str(datetime.now())
            estado = str(pedido.estado) if pedido.estado else 'Pendiente'

            cursor = connection.execute(sql, (
                usuario_id,
                total,
                fecha_hora,
                estado
            ))

            # Obtener el ID del pedido insertado
            pedido_id = cursor.lastrowid

            # Si no se obtuvo ID, intentar recuperarlo manualmente
            if not pedido_id:
                cursor = connection.execute("SELECT last_insert_rowid()")
                row = cursor.fetchone()
                if row:
                    pedido_id = row[0]

            if not pedido_id:
                connection.rollback()
                print("ERROR: No se pudo obtener ID del pedido")
                return False, "No se pudo crear el pedido", None

            print(f"INFO: Pedido base creado con ID: {pedido_id}")

            # Insertar productos del pedido
            print(f"INFO: Agregando {len(productos)} productos al pedido {pedido_id}")
            for producto in productos:
                try:
                    producto_id = producto.get('producto_id')
                    cantidad = producto.get('cantidad')
                    sub_total = producto.get('sub_total')

                    if not all([producto_id, cantidad is not None, sub_total is not None]):
                        connection.rollback()
                        return False, "Producto con datos incompletos", None

                    sql_producto = "INSERT INTO Pedido_Producto (pedido_id, producto_id, cantidad, sub_total) VALUES (?, ?, ?, ?)"
                    connection.execute(sql_producto, (
                        int(pedido_id),
                        int(producto_id),
                        int(cantidad),
                        float(sub_total)
                    ))
                except Exception as e:
                    connection.rollback()
                    print(f"ERROR: Al insertar producto: {str(e)}")
                    return False, f"Error al insertar producto: {str(e)}", None

            # Insertar extras (si hay)
            if extras and len(extras) > 0:
                print(f"INFO: Agregando {len(extras)} extras al pedido {pedido_id}")
                for extra in extras:
                    try:
                        extra_id = extra.get('extra_id')
                        cantidad = extra.get('cantidad')
                        sub_total = extra.get('sub_total')

                        if not all([extra_id, cantidad is not None, sub_total is not None]):
                            connection.rollback()
                            return False, "Extra con datos incompletos", None

                        sql_extra = "INSERT INTO Pedido_Extra (pedido_id, extra_id, cantidad, sub_total) VALUES (?, ?, ?, ?)"
                        connection.execute(sql_extra, (
                            int(pedido_id),
                            int(extra_id),
                            int(cantidad),
                            float(sub_total)
                        ))
                    except Exception as e:
                        connection.rollback()
                        print(f"ERROR: Al insertar extra: {str(e)}")
                        return False, f"Error al insertar extra: {str(e)}", None

            # Si llegamos hasta aquí, todo está bien, confirmar transacción
            connection.commit()
            print(f"INFO: Transacción completada. Pedido {pedido_id} creado con {len(productos)} productos y {len(extras)} extras")

            # Crear notificación para informar al usuario sobre el pedido creado
            try:
                print(f"INFO: Creando notificación para el nuevo pedido {pedido_id}, usuario {pedido.usuario_id}")
                mensaje = f"Tu pedido #{pedido_id} ha sido creado con éxito. Te notificaremos cuando sea enviado."
                exito_notif, mensaje_notif, notif_id = NotificacionService.crear_notificacion(
                    usuario_id=pedido.usuario_id,
                    pedido_id=pedido_id,
                    mensaje=mensaje,
                    tipo='nuevo_pedido'
                )
                if exito_notif:
                    print(f"INFO: Notificación de nuevo pedido creada exitosamente con ID {notif_id}")
                else:
                    print(f"ADVERTENCIA: No se pudo crear la notificación: {mensaje_notif}")
            except Exception as notif_ex:
                print(f"ADVERTENCIA: No se pudo crear la notificación para el nuevo pedido: {str(notif_ex)}")
                traceback.print_exc()
                # Continuamos aunque falle la notificación, ya que el pedido se creó correctamente

            return True, "Pedido creado exitosamente", pedido_id

        except Exception as e:
            if connection:
                connection.rollback()
            print(f"ERROR en post_pedido: {str(e)}")
            traceback.print_exc()
            return False, f"Error inesperado: {str(e)}", None

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_pedido(cls):
        """
        Obtiene todos los pedidos en el sistema.
        Returns:
            list: Lista de pedidos.
        """
        connection = None
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido ORDER BY fecha_hora DESC"
            datos = connection.execute(sql).fetchall()

            pedidos = []
            for dato in datos:
                pedido = {
                    'id': dato[0],
                    'usuario_id': dato[1],
                    'total': dato[2],
                    'fecha_hora': dato[3],
                    'estado': dato[4]
                }
                pedidos.append(pedido)

            return pedidos

        except Exception as ex:
            print(f"ERROR al obtener pedidos: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_pedido_by_id(cls, id):
        """Obtiene un pedido específico por su ID"""
        connection = None
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido WHERE pedido_id = ?"
            dato = connection.execute(sql, (id,)).fetchone()

            if not dato:
                return {}

            pedido = {
                'id': dato[0],
                'usuario_id': dato[1],
                'total': dato[2],
                'fecha_hora': dato[3],
                'estado': dato[4]
            }

            return pedido

        except Exception as ex:
            print(f"ERROR al obtener pedido por ID: {str(ex)}")
            return {}

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_historial_usuario(cls, usuario_id):
        """Obtiene el historial completo de pedidos de un usuario"""
        connection = None
        try:
            connection = get_connection()
            sql = """
                SELECT p.pedido_id, p.total, p.fecha_hora, p.estado,
                       GROUP_CONCAT(pr.nombre || ' (x' || pp.cantidad || ')') as productos,
                       GROUP_CONCAT(e.nombre || ' (x' || pe.cantidad || ')') as extras
                FROM Pedido p
                LEFT JOIN Pedido_Producto pp ON p.pedido_id = pp.pedido_id
                LEFT JOIN Producto pr ON pp.producto_id = pr.producto_id
                LEFT JOIN Pedido_Extra pe ON p.pedido_id = pe.pedido_id
                LEFT JOIN Extra e ON pe.extra_id = e.extra_id
                WHERE p.usuario_id = ?
                GROUP BY p.pedido_id, p.total, p.fecha_hora, p.estado
                ORDER BY p.fecha_hora DESC
            """
            datos = connection.execute(sql, (usuario_id,)).fetchall()

            historial = []
            for dato in datos:
                pedido = {
                    'id': dato[0],
                    'total': dato[1],
                    'fecha_hora': dato[2],
                    'estado': dato[3],
                    'productos': dato[4].split(',') if dato[4] else [],
                    'extras': dato[5].split(',') if dato[5] else []
                }
                historial.append(pedido)

            print(f"INFO: Historial recuperado para usuario {usuario_id}: {len(historial)} pedidos")
            return historial

        except Exception as ex:
            print(f"ERROR al obtener historial: {str(ex)}")
            traceback.print_exc()
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def actualizar_estado_pedido(cls, pedido_id, nuevo_estado):
        """
        Actualiza el estado de un pedido y genera notificaciones si es necesario.
        Utiliza transacción para garantizar atomicidad.

        Args:
            pedido_id: ID del pedido a actualizar
            nuevo_estado: Estado al que se cambiará el pedido

        Returns:
            tuple: (bool, str) con éxito/fallo y mensaje
        """
        connection = None
        try:
            # Validar estados permitidos
            estados_validos = ['Pendiente', 'Preparando', 'Enviado', 'Entregado', 'Cancelado']
            if nuevo_estado not in estados_validos:
                return False, f"Estado inválido. Valores permitidos: {', '.join(estados_validos)}"

            print(f"INFO: Iniciando transacción para actualizar estado del pedido {pedido_id} a '{nuevo_estado}'")
            connection = get_connection()

            # Obtener información actual del pedido
            sql_get = "SELECT usuario_id, estado FROM Pedido WHERE pedido_id = ?"
            pedido_actual = connection.execute(sql_get, (pedido_id,)).fetchone()

            if not pedido_actual:
                return False, f"Pedido #{pedido_id} no encontrado"

            usuario_id = pedido_actual[0]
            estado_anterior = pedido_actual[1]

            # Si el estado es el mismo, no hacer nada
            if estado_anterior == nuevo_estado:
                return True, f"El pedido ya tiene estado {nuevo_estado}"

            # Actualizar el estado
            sql_update = "UPDATE Pedido SET estado = ? WHERE pedido_id = ?"
            connection.execute(sql_update, (str(nuevo_estado), int(pedido_id)))

            print(f"INFO: Estado del pedido {pedido_id} actualizado de '{estado_anterior}' a '{nuevo_estado}'")

            # Si el estado cambió a "Enviado", crear notificación dentro de la misma transacción
            if nuevo_estado == 'Enviado' and estado_anterior != 'Enviado' and usuario_id:
                print(f"INFO: Creando notificación para pedido {pedido_id} (usuario {usuario_id})")

                # Crear notificación directamente en esta transacción para garantizar atomicidad
                mensaje_notif = f"¡Tu pedido #{pedido_id} ha sido enviado! Pronto estará en camino."
                sql_notif = "INSERT INTO Notificacion (usuario_id, pedido_id, mensaje, tipo) VALUES (?, ?, ?, ?)"
                connection.execute(sql_notif, (int(usuario_id), int(pedido_id), str(mensaje_notif), 'envio'))

                print(f"INFO: Notificación creada dentro de la transacción")

                # Intentar enviar email (no afecta a la transacción si falla)
                try:
                    # from src.services.usuario_service import UsuarioService # This import is not in the original file,
                    # so it's commented out to avoid an error.
                    # usuario = UsuarioService.get_usuario_by_id(usuario_id)
                    # if usuario and usuario.get('email'):
                    #     NotificacionService._enviar_email_pedido_enviado(usuario['email'], usuario['nombre'], pedido_id)
                    pass # Placeholder for actual email sending logic
                except Exception as email_ex:
                    print(f"ADVERTENCIA: No se pudo enviar email: {str(email_ex)}")

            # Confirmar todos los cambios
            connection.commit()
            print(f"INFO: Transacción completada exitosamente")

            return True, f"Estado de pedido actualizado a {nuevo_estado}"

        except Exception as ex:
            if connection:
                connection.rollback()
            print(f"ERROR al actualizar estado: {str(ex)}")
            traceback.print_exc()
            return False, f"Error: {str(ex)}"

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_pedidos_usuario(cls, usuario_id):
        """
        Obtiene todos los pedidos de un usuario específico

        Args:
            usuario_id: ID del usuario

        Returns:
            list: Lista de pedidos del usuario
        """
        connection = None
        try:
            connection = get_connection()
            sql = "SELECT * FROM Pedido WHERE usuario_id = ? ORDER BY fecha_hora DESC"
            datos = connection.execute(sql, (usuario_id,)).fetchall()

            pedidos = []
            for dato in datos:
                pedido = {
                    'id': dato[0],
                    'usuario_id': dato[1],
                    'total': dato[2],
                    'fecha_hora': dato[3],
                    'estado': dato[4]
                }
                pedidos.append(pedido)

            print(f"INFO: {len(pedidos)} pedidos encontrados para el usuario {usuario_id}")
            return pedidos

        except Exception as ex:
            print(f"ERROR al obtener pedidos del usuario: {str(ex)}")
            traceback.print_exc()
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_total_dia(cls):
        """Obtiene las ventas totales por día"""
        connection = None
        try:
            connection = get_connection()
            sql = """
                SELECT DATE(fecha_hora) AS fecha, SUM(total) AS total_ventas
                FROM Pedido
                WHERE fecha_hora >= datetime('now', '-7 day')
                GROUP BY DATE(fecha_hora);
            """
            datos = connection.execute(sql).fetchall()

            # Crear diccionario con fechas y ventas
            datos_dict = {fecha: valor for fecha, valor in datos}

            # Generar datos para los últimos 7 días
            fechas = [datetime.now() - timedelta(days=i) for i in range(7)]
            datos_dias = [
                {'time': fecha.strftime('%Y-%m-%d'),
                 'value': datos_dict.get(fecha.strftime('%Y-%m-%d'), 0)}
                for fecha in fechas
            ]

            return sorted(datos_dias, key=lambda x: x['time'])

        except Exception as ex:
            print(f"ERROR al obtener total por día: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_total_semana(cls):
        """Obtiene las ventas totales por semana"""
        connection = None
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
                    'time': fecha,
                    'value': dato[1],
                }
                datos_semanas.append(dato_semana)

            return sorted(datos_semanas, key=lambda x: x['time'])

        except Exception as ex:
            print(f"ERROR al obtener total por semana: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_total_mes(cls):
        """Obtiene las ventas totales por mes"""
        connection = None
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
                    'time': fecha,
                    'value': dato[1],
                }
                datos_meses.append(dato_mes)

            return sorted(datos_meses, key=lambda x: x['time'])

        except Exception as ex:
            print(f"ERROR al obtener total por mes: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()

    @classmethod
    def get_total_ano(cls):
        """Obtiene las ventas totales por año"""
        connection = None
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
                    'time': fecha,
                    'value': dato[1],
                }
                datos_anos.append(dato_ano)

            return sorted(datos_anos, key=lambda x: x['time'])

        except Exception as ex:
            print(f"ERROR al obtener total por año: {str(ex)}")
            return []

        finally:
            if connection:
                connection.close()
