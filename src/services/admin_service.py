from sqlalchemy.engine import connection_memoize
from src.database.db_mysql import get_connection
from src.models.admin_model import Admin
from sqlalchemy import text

class Admin_Service():

    @classmethod
    def post_admin(cls, admin):
        try:
            connection = get_connection()
            sql = text("INSERT INTO Admin (username, password) VALUES (:username, :password)")
            connection.execute(sql, {
                "username" : admin.username, 
                "password" : admin.password
            })
            connection.commit()
            return True, 'Admin registrado'
        except Exception as ex:
            return False, str(ex)
        finally:
            connection.close()

    @classmethod
    def get_admin_by_id(cls, id):
        try:
            connection = get_connection()
            sql = text("SELECT * FROM Admin WHERE admin_id = :id")
            dato = connection.execute(sql, {"id" : id}).fetchone()
            if dato:
                admin = Admin(dato[1], dato[2], dato[0])
                return admin.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
    
    @classmethod
    def get_admin_by_username(cls, username):
        try:
            connection = get_connection()
            sql = text("SELECT * FROM Admin WHERE username = :username")
            dato = connection.execute(sql, {
                "username" : username
            }).fetchone()
            if dato:
                admin = Admin(dato[1], dato[2], dato[0])
                return admin.to_json()
            else:
                return None
        except Exception as ex:
            return str(ex)
        finally:
            connection.close()

    @classmethod
    def update_admin(cls, admin):
        try:
            connection = get_connection()
            print(admin.username, admin.password, admin.id)
            sql = text("UPDATE Admin SET username :username, password :password WHERE admin_id = :admin_id;")
            connection.execute(sql, {
                "username" : admin.username,
                "password" : admin.password,
                "admin_id" : admin.id
            })
            connection.commit()
            return True, "Admin Actualizado"
        except Exception as e:
            return False, str(e)
        finally:
            connection.close()
