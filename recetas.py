from flask_login import current_user

from models.entities.User import User
from models.entities.Clases import * 

class Recetas():   
    @classmethod
    def extraerlistaRecetas(self,db):
        try:
            listarecetas = []
            cursor = db.connection.cursor()
            sql = "SELECT r.idreceta, m.nombre,r.fecha,r.descripcion FROM recetas r INNER JOIN mascotas m ON m.idmascota = r.idmascota"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevoreceta=Receta(row[0],row[1],row[2],row[3])
                    listarecetas.append(nuevoreceta)
                    row=cursor.fetchone()
            return listarecetas
        except Exception as ex:
            raise Exception(ex)      
        
    @classmethod
    def agregarReceta(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO recetas (idmascota,fecha,descripcion) VALUES (%s,%s,%s)", (valores[0],valores[1],valores[2]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerReceta(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM recetas WHERE idreceta = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarReceta(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE recetas SET idmascota=%s,fecha=%s,descripcion=%s  WHERE idreceta = %s", (valores[0], valores[1],valores[2],valores[3]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def eliminarReceta(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM recetas WHERE idreceta= {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)   