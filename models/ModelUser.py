from .entities.User import User

class ModelUser():
    
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, nombre, email, telefono, usuario, contraseña, tipo FROM usuarios 
                    WHERE usuario = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[4],User.check_password(row[5],user.password),row[1])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, nombre, usuario FROM usuarios WHERE id = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                logged_user=User(row[0],row[1],None,row[2])
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)