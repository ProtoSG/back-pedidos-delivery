from src.database.db_mysql import get_connection
from src.models.usuario_model import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UsuarioService():

    @classmethod
    def registrar_usuario(cls, usuario):
        try:
            connection = get_connection()

            # Verificar si el email ya existe
            sql_check = "SELECT email FROM Usuario WHERE email = ?"
            existing_user = connection.execute(sql_check, (usuario.email,)).fetchone()

            if existing_user:
                return False, 'El email ya está registrado'

            # Encriptar la contraseña
            hashed_password = bcrypt.generate_password_hash(usuario.password).decode('utf-8')

            # Insertar nuevo usuario
            sql = "INSERT INTO Usuario (nombre, email, password) VALUES (?, ?, ?)"
            connection.execute(sql, (usuario.nombre, usuario.email, hashed_password))
            connection.commit()
            return True, 'Usuario registrado exitosamente'

        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def login_usuario(cls, email, password):
        try:
            # Validar que el email y password no estén vacíos
            if not email or not password:
                return False, "Email y password son requeridos"

            # Buscar usuario por email
            query = "SELECT usuario_id, nombre, email, password, activo FROM Usuario WHERE email = ?"
            cursor = get_connection().cursor()
            cursor.execute(query, (email,))
            dato = cursor.fetchone()

            if not dato:
                return False, "Usuario no encontrado"

            # Verificar si el usuario está activo
            if not dato[4]:  # dato[4] es el campo 'activo'
                return False, "Usuario inactivo"

            # Verificar password
            if bcrypt.check_password_hash(dato[3], password):  # dato[3] es el password
                return True, {
                    'id': dato[0],
                    'nombre': dato[1],
                    'email': dato[2]
                }
            else:
                return False, "Password incorrecto"

        except Exception as ex:
            print(f"ERROR en login_usuario: {str(ex)}")
            return False, f"Error interno del servidor: {str(ex)}"

    @classmethod
    def get_usuario_by_id(cls, usuario_id):
        try:
            connection = get_connection()
            sql = "SELECT * FROM Usuario WHERE usuario_id = ?"
            dato = connection.execute(sql, (usuario_id,)).fetchone()

            if dato:
                usuario = Usuario(dato[1], dato[2], dato[3], dato[0], dato[4], dato[5])
                return usuario.to_json()
            else:
                return None

        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def get_usuario_by_email(cls, email):
        try:
            query = "SELECT usuario_id, nombre, email, password, activo FROM Usuario WHERE email = ?"
            cursor = get_connection().cursor()
            cursor.execute(query, (email,))
            dato = cursor.fetchone()

            if dato:
                return {
                    'id': dato[0],
                    'nombre': dato[1],
                    'email': dato[2],
                    'password': dato[3],
                    'activo': dato[4]
                }
            return None

        except Exception as ex:
            print(f"ERROR en get_usuario_by_email: {str(ex)}")
            return None

    @classmethod
    def actualizar_usuario(cls, usuario):
        try:
            connection = get_connection()
            sql = "UPDATE Usuario SET nombre = ?, email = ? WHERE usuario_id = ?"
            connection.execute(sql, (usuario.nombre, usuario.email, usuario.id))
            connection.commit()
            return True, "Usuario actualizado exitosamente"

        except Exception as e:
            return False, str(e)
        finally:
            connection.close()

    @classmethod
    def cambiar_password(cls, usuario_id, nueva_password):
        try:
            connection = get_connection()
            hashed_password = bcrypt.generate_password_hash(nueva_password).decode('utf-8')
            sql = "UPDATE Usuario SET password = ? WHERE usuario_id = ?"
            connection.execute(sql, (hashed_password, usuario_id))
            connection.commit()
            return True, "Contraseña actualizada exitosamente"

        except Exception as e:
            return False, str(e)
        finally:
            connection.close()

    @classmethod
    def desactivar_usuario(cls, usuario_id):
        try:
            connection = get_connection()
            sql = "UPDATE Usuario SET activo = 0 WHERE usuario_id = ?"
            connection.execute(sql, (usuario_id,))
            connection.commit()
            return True, "Usuario desactivado"

        except Exception as e:
            return False, str(e)
        finally:
            connection.close()
