from flask_login import current_user

from models.entities.User import User
from models.entities.Clases import * 

class Citas():  
    @classmethod
    def extraerCitas(self,db):
        try:
            listacitas = []
            cursor = db.connection.cursor()
            sql = "SELECT c.idcita, m.nombre, s.servicio, fecha, hora FROM citas c INNER JOIN mascotas m ON m.idmascota = c.idmascota INNER JOIN servicios s ON s.idservicio = c.idservicio"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevacita=Cita(row[0],row[1],row[2],row[3],row[4])
                    listacitas.append(nuevacita)
                    row=cursor.fetchone()
            return listacitas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregarCita(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO citas (idmascota,idservicio, fecha, hora) VALUES (%s,%s,%s,%s)", (valores[0],valores[1],valores[2],valores[3]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerCita(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM citas WHERE idcita = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarCita(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE citas SET idmascota=%s, idservicio=%s, fecha=%s, hora=%s  WHERE idcita = %s", (valores[0], valores[1], valores[2],valores[3],valores[4]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminarCita(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM citas WHERE idcita= {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)