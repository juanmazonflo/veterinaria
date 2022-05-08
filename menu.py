from flask_login import current_user

from models.entities.User import User
from models.entities.Clases import *

class Menu():   
   
    @classmethod
    def extraermenu(self,tipo):
        try:
            if tipo == "admin":
                usermenu = {"Home":"/home","Agendar cita":"/citas", "Historiales":"/historial","Atencion":"/atencion","Agregar receta":"/recetas/agregar","Agendar atencion":"/atencion/agregar","Usuarios":"/usuarios","Medicinas":"/medicinas","Servicios":"/servicios","Informes ventas":"/informes","Mascotas":"/mascotas"}
            else:
                if tipo == "usuario":
                    usermenu = {"Home":"/home","Agendar una cita":"/citas", "Historiales":"/historial","Atencion":"/atencion","Agregar receta":"/recetas/agregar","Agendar una atencion":"/atencion/agregar","Mascotas":"/mascotas"}
                else:
                    if tipo == "cliente":
                        usermenu = {"Home":"/home","Agendar una cita":"/citas", "Historiales":"/historial","Mascotas":"/mascotas"},
            return usermenu
        except Exception as ex:
            raise Exception(ex)