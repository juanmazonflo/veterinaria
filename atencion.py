from flask_login import current_user

from models.entities.User import User
from models.entities.Clases import * 

class Atenciones():  
    @classmethod
    def extraerlistaAtencion(self,db):
        try:
            listaatencion = []
            cursor = db.connection.cursor()
            sql = "SELECT * FROM atencion"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevoatencion=Atencion(row[0],row[1],row[2],row[3],row[4],row[5])
                    listaatencion.append(nuevoatencion)
                    row=cursor.fetchone()
            return listaatencion
        except Exception as ex:
            raise Exception(ex)      
        
    @classmethod
    def agregarAtencion(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO atencion (idcita,idreceta,atendido,descripcion,subtotal) VALUES (%s,%s,%s,%s,%s)", (valores[0],valores[1],valores[2],valores[3],valores[4]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerAtencion(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM atencion WHERE idatencion = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarAtencion(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE recetas SET idcita=%s,idreceta=%s,atendido=%s,descripcion=%s,subtotal=%s  WHERE idreceta = %s", (valores[0], valores[1],valores[2],valores[3],valores[4]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def eliminarAtencion(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM atencion WHERE idatencion= {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)