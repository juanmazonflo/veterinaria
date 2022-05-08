from flask_login import current_user

from models.entities.User import User
from models.entities.Clases import * 

class Mascotas():
    
    @classmethod
    def extraerlistamascotas(self,db):
        try:
            listamascotas = []
            cursor = db.connection.cursor()
            sql = "SELECT m.idmascota, u.nombre, m.tipo, m.nombre FROM mascotas m INNER JOIN usuarios u ON m.idusuario = u.idusuario"
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevamascota=Mascota(row[0],row[1],row[2],row[3])
                    listamascotas.append(nuevamascota)
                    row=cursor.fetchone()
            return listamascotas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerlistamascotasCliente(self,db,id):
        try:
            listamascotas = []
            cursor = db.connection.cursor()
            sql = ("SELECT m.idmascota, u.nombre, m.tipo, m.nombre FROM mascotas m INNER JOIN usuarios u ON m.idusuario = u.idusuario INNER JOIN usuarios o ON m.idusuario={0}".format(id))
            cursor.execute(sql)
            row=cursor.fetchone()
            while row != None:
                    nuevamascota=Mascota(row[0],row[1],row[2],row[3])
                    listamascotas.append(nuevamascota)
                    row=cursor.fetchone()
            return listamascotas
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def agregarMascota(self,db,valores):
        try:
            cursor = db.connection.cursor()
            cursor.execute("INSERT INTO mascotas (idusuario, tipo, nombre) VALUES (%s,%s,%s)", (valores[0],valores[1],valores[2]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def extraerMascota(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('SELECT * FROM mascotas WHERE idmascota = %s', (id))
            data = cur.fetchall()
            cur.close()
            return data
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def actualizarMascota(self,db,valores):
        try:
            cur = db.connection.cursor()
            cur.execute("UPDATE mascotas SET idusuario=%s, tipo=%s, nombre=%s  WHERE idmascota = %s", (valores[0], valores[1], valores[2],valores[3]))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def eliminarMascota(self,db,id):
        try:
            cur = db.connection.cursor()
            cur.execute('DELETE FROM mascotas WHERE idmascota = {0}'.format(id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

