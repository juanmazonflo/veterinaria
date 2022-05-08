from flask_login import current_user

from models.entities.User import User
from models.entities.Clases import * 

class Usuarios():      
    
    @classmethod
    def extraerlistausuarios(self,db):
        try:
            listausuarios = []
            cursor = db.connection.cursor()
            sql = "SELECT * FROM usuarios"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevouser=User(row[0],row[1],row[2],row[3],row[4],row[5])
                    listausuarios.append(nuevouser)
                    row=cursor.fetchone()
            return listausuarios
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregarUsuario(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("INSERT INTO usuarios (username, password, nombre, email, tipo) VALUES (%s,%s,%s,%s,%s)", (valores[0],valores[1],valores[2],valores[3],valores[4]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerUsuario(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM usuarios WHERE idusuario = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def actualizarUsuario(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE usuarios SET username=%s, password=%s, nombre=%s, email=%s, tipo=%s  WHERE idusuario = %s", (valores[0],valores[1],valores[2],valores[3],valores[4],valores[5]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def eliminarUsuario(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM usuarios WHERE idusuario = {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)