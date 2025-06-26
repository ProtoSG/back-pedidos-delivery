from src.database.db_mysql import get_connection
from src.models.notificacion_model import Notificacion
from src.services.usuario_service import UsuarioService
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import traceback
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class NotificacionService():

    @staticmethod
    def crear_notificacion(usuario_id, pedido_id=None, mensaje="", tipo="info"):
        try:
            connection = get_connection()
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Log de datos recibidos
            print(f"INFO: Creando notificación - usuario_id: {usuario_id}, pedido_id: {pedido_id}, tipo: {tipo}")

            # Verificar que la tabla existe
            tables = connection.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Notificacion'").fetchall()
            if not tables:
                print("ERROR: La tabla Notificacion no existe")
                return False, "La tabla Notificacion no existe", None

            # Insertar notificación
            sql = """
                INSERT INTO Notificacion (usuario_id, pedido_id, mensaje, tipo, leida, fecha_envio)
                VALUES (?, ?, ?, ?, 0, ?)
            """
            cursor = connection.execute(sql, (usuario_id, pedido_id, mensaje, tipo, fecha_actual))
            connection.commit()

            # Obtener el ID de la notificación insertada
            notificacion_id = cursor.lastrowid

            # Verificar que la inserción fue exitosa
            verify_sql = "SELECT id, usuario_id FROM Notificacion WHERE id = ?"
            verify_result = connection.execute(verify_sql, (notificacion_id,)).fetchone()

            if verify_result:
                print(f"INFO: Notificación creada exitosamente - ID: {notificacion_id}")
                return True, "Notificación creada exitosamente", notificacion_id
            else:
                print(f"ERROR: No se pudo verificar la notificación creada")
                return False, "Error al crear la notificación", None

        except Exception as ex:
            print(f"ERROR en crear_notificacion: {str(ex)}")
            return False, f"Error interno del servidor: {str(ex)}", None
        finally:
            connection.close()

    @classmethod
    def get_notificaciones_usuario(cls, usuario_id, solo_no_leidas=False):
        try:
            connection = get_connection()

            # Obtener información de la estructura de la tabla
            table_info = connection.execute("PRAGMA table_info(Notificacion)").fetchall()

            # Construir la consulta base
            sql = """
                SELECT notificacion_id, usuario_id, pedido_id, mensaje, tipo, leida, fecha_envio
                FROM Notificacion
                WHERE usuario_id = ?
            """

            # Agregar filtro para solo no leídas si se solicita
            if solo_no_leidas:
                sql += " AND leida = 0"

            sql += " ORDER BY fecha_envio DESC"

            # Ejecutar la consulta
            cursor = connection.execute(sql, (usuario_id,))
            notificaciones = cursor.fetchall()

            # Convertir a lista de diccionarios
            resultado = []
            for notif in notificaciones:
                resultado.append({
                    'id': notif[0],
                    'usuario_id': notif[1],
                    'pedido_id': notif[2],
                    'mensaje': notif[3],
                    'tipo': notif[4],
                    'leida': bool(notif[5]),
                    'fecha_envio': notif[6]
                })

            print(f"INFO: Recuperadas {len(resultado)} notificaciones para usuario {usuario_id}")
            return resultado

        except Exception as ex:
            print(f"ERROR en get_notificaciones_usuario: {str(ex)}")
            return []
        finally:
            connection.close()

    @classmethod
    def marcar_como_leida(cls, notificacion_id):
        try:
            connection = get_connection()

            # Verificar que la notificación existe
            check_sql = "SELECT notificacion_id FROM Notificacion WHERE notificacion_id = ?"
            check_result = connection.execute(check_sql, (notificacion_id,)).fetchone()

            if not check_result:
                return False, "Notificación no encontrada"

            # Actualizar estado a leída
            sql = "UPDATE Notificacion SET leida = 1 WHERE notificacion_id = ?"
            connection.execute(sql, (notificacion_id,))
            connection.commit()

            print(f"INFO: Notificación #{notificacion_id} marcada como leída")
            return True, "Notificación marcada como leída exitosamente"

        except Exception as ex:
            print(f"ERROR en marcar_como_leida: {str(ex)}")
            return False, f"Error interno del servidor: {str(ex)}"
        finally:
            connection.close()

    @classmethod
    def marcar_todas_como_leidas(cls, usuario_id):
        try:
            connection = get_connection()
            sql = "UPDATE Notificacion SET leida = 1 WHERE usuario_id = ?"
            connection.execute(sql, (usuario_id,))
            connection.commit()
            return True, 'Todas las notificaciones marcadas como leídas'

        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def notificar_pedido_enviado(cls, pedido_id, usuario_id):
        """
        Crea una notificación de pedido enviado y envía un email.
        Esta función es utilizada como parte de una transacción más grande
        cuando se actualiza el estado de un pedido a 'Enviado'.

        Args:
            pedido_id: ID del pedido enviado
            usuario_id: ID del usuario destinatario

        Returns:
            tuple: (bool, str) con éxito y mensaje
        """
        try:
            # Validar parámetros
            if not pedido_id or not usuario_id:
                print("ERROR: Faltan parámetros requeridos")
                return False, "Se requieren IDs de pedido y usuario"

            # Sanitizar y validar tipos
            try:
                pedido_id = int(pedido_id) if pedido_id else None
                usuario_id = int(usuario_id) if usuario_id else None
            except (ValueError, TypeError) as e:
                print(f"ERROR: Conversión de tipos fallida - {e}")
                return False, f"Error en tipos de datos: {str(e)}"

            print(f"INFO: Notificando envío del pedido {pedido_id} al usuario {usuario_id}")

            # Crear mensaje de notificación
            mensaje = f"¡Tu pedido #{pedido_id} ha sido enviado! Pronto estará en camino."

            # Crear notificación en la base de datos
            print(f"DEBUG: Llamando a crear_notificacion con usuario_id={usuario_id}, pedido_id={pedido_id}")
            success, message, notificacion_id = cls.crear_notificacion(usuario_id, pedido_id, mensaje, 'envio')

            if not success:
                print(f"ERROR: No se pudo crear la notificación - {message}")
                return False, f"Error al crear notificación: {message}"

            # Enviar notificación por email (opcional, no afecta el resultado de la función)
            try:
                usuario = UsuarioService.get_usuario_by_id(usuario_id)
                if usuario and usuario.get('email'):
                    cls._enviar_email_pedido_enviado(usuario['email'], usuario['nombre'], pedido_id)
                    print(f"INFO: Email de notificación enviado a {usuario.get('email')}")
                else:
                    print(f"ADVERTENCIA: No se encontró email para el usuario_id={usuario_id}")
            except Exception as email_error:
                print(f"ADVERTENCIA: No se pudo enviar email: {str(email_error)}")

            print(f"INFO: Notificación de pedido enviado creada exitosamente con ID {notificacion_id}")
            return True, 'Notificación de envío creada exitosamente'

        except Exception as ex:
            print(f"ERROR en notificar_pedido_enviado: {str(ex)}")
            traceback.print_exc()
            return False, str(ex)

    @classmethod
    def _enviar_email_pedido_enviado(cls, email_destino, nombre_usuario, pedido_id):
        try:
            # Configuración del servidor SMTP (opcional, requiere configuración)
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = os.getenv('SMTP_PORT', 587)
            smtp_username = os.getenv('SMTP_USERNAME')
            smtp_password = os.getenv('SMTP_PASSWORD')

            if not all([smtp_server, smtp_username, smtp_password]):
                print("Configuración SMTP no completa, saltando envío de email")
                return False

            # Crear mensaje
            msg = MIMEMultipart()
            msg['From'] = smtp_username
            msg['To'] = email_destino
            msg['Subject'] = f"Tu pedido #{pedido_id} ha sido enviado"

            # Cuerpo del mensaje
            body = f"""
            Hola {nombre_usuario},

            ¡Buenas noticias! Tu pedido #{pedido_id} ha sido enviado y está en camino.

            Gracias por elegirnos.

            Saludos,
            Equipo de Delivery
            """

            msg.attach(MIMEText(body, 'plain'))

            # Enviar email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.quit()

            return True

        except Exception as ex:
            print(f"Error al enviar email: {str(ex)}")
            return False

    @classmethod
    def get_resumen_notificaciones(cls, usuario_id):
        try:
            connection = get_connection()

            # Obtener total de notificaciones
            total_sql = "SELECT COUNT(*) FROM Notificacion WHERE usuario_id = ?"
            total = connection.execute(total_sql, (usuario_id,)).fetchone()[0]

            # Obtener notificaciones no leídas
            no_leidas_sql = "SELECT COUNT(*) FROM Notificacion WHERE usuario_id = ? AND leida = 0"
            no_leidas = connection.execute(no_leidas_sql, (usuario_id,)).fetchone()[0]

            print(f"INFO: Resumen notificaciones - total: {total}, no_leidas: {no_leidas}")

            return {
                'total': total,
                'no_leidas': no_leidas,
                'leidas': total - no_leidas
            }

        except Exception as ex:
            print(f"ERROR en get_resumen_notificaciones: {str(ex)}")
            return {'total': 0, 'no_leidas': 0, 'leidas': 0}
        finally:
            connection.close()

    @classmethod
    def eliminar_notificacion(cls, notificacion_id, usuario_id):
        try:
            connection = get_connection()
            sql = "DELETE FROM Notificacion WHERE notificacion_id = ? AND usuario_id = ?"
            connection.execute(sql, (notificacion_id, usuario_id))
            connection.commit()
            return True, 'Notificación eliminada'

        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def crear_notificacion_envio(cls, usuario_id, pedido_id):
        try:
            mensaje = f"Tu pedido #{pedido_id} ha sido enviado y está en camino."
            print(f"INFO: Creando notificación de envío para pedido #{pedido_id}")
            return cls.crear_notificacion(usuario_id, pedido_id, mensaje, "envio")
        except Exception as ex:
            print(f"ERROR en crear_notificacion_envio: {str(ex)}")
            return False, f"Error al crear notificación de envío: {str(ex)}", None
