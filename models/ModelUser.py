from flask_login import current_user
from .entities.User import User

class ModelUser():
    
    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idusuario, username, password FROM usuarios 
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],User.check_password(row[2],user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idusuario, username, nombre, email, tipo FROM usuarios WHERE idusuario = {}".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                logged_user=User(row[0],row[1],None,row[2],row[3],row[4])
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def checkuser(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idusuario, username FROM usuarios WHERE username = '{}'".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            matchuser = False
            if row == None:
                matchuser = True
                return matchuser
            else:
                return matchuser
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def checkemail(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT idusuario, email FROM usuarios WHERE email = '{}'".format(user.email)
            cursor.execute(sql)
            row=cursor.fetchone()
            matchuser = False
            if row == None:
                matchuser = True
                return matchuser
            else:
                return matchuser
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def checknewpasswords(self,new,confirm):
        try:
            bandera = False
            if new == confirm:
                bandera = True
                return bandera
            else:
                return bandera
        except Exception as ex:
            raise Exception(ex)