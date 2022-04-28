class Mascota():
    def __init__(self, idmascota, iusuario, tipo, nombre="") -> None:
        self.idmascota = idmascota
        self.idusuario = iusuario
        self.tipo = tipo
        self.nombre = nombre
        
class Servicio():
    def __init__(self, idservicio, servicio, precio) -> None:
        self.idservicio = idservicio
        self.servicio = servicio
        self.servicio = servicio
        self.precio = precio