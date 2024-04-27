from src.database.db_mysql import get_connection
from src.models.admin_model import Admin

class Admin_Service():

    @classmethod
    def post_admin(cls, admin):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "INSERT INTO Admin (username, password) VALUES (?, ?)"
            cursor.execute(sql, (admin.username, admin.password))
            connection.commit()
            return True, 'Admin registrado'
        except Exception as ex:
            return False, str(ex)
        finally:
            cursor.close()
            connection.sync()

    @classmethod
    def get_admin_by_id(cls, id):
        try:
            conneciton = get_connection()
            cursor = conneciton.cursor()
            sql = "SELECT * FROM Admin WHERE admin_id = ?"
            cursor.execute(sql, (id,))
            dato = cursor.fetchone()
            if dato:
                admin = Admin(dato[1], dato[0])
                return admin.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
    
    @classmethod
    def get_admin_by_username(cls, username):
        try:
            connection = get_connection()
            cursor = connection.cursor()
            sql = "SELECT * FROM Admin WHERE username = ?"
            cursor.execute(sql, (username,))
            dato = cursor.fetchone()
            if dato:
                admin = Admin(dato[1], dato[2])
                return admin.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)