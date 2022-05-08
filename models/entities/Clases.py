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

class Cita():
    def __init__(self, idcita, idmascota, idservicio,fecha,hora) -> None:
        self.idcita=idcita
        self.idmascota =idmascota
        self.idservicio=idservicio
        self.fecha =fecha
        self.hora =hora

class Medicinas():
    def __init__(self, idmedicina, descripcion,medida,presentacion, precio) -> None:
        self.idmedicina=idmedicina
        self.descripcion =descripcion
        self.medida=medida
        self.presentacion=presentacion
        self.precio =precio

class Receta():
    def __init__(self, idreceta, idmascota,fecha,descripcion) -> None:
        self.idreceta=idreceta
        self.idmascota =idmascota
        self.fecha=fecha
        self.descripcion=descripcion

class Atencion():
    def __init__(self,idatencion,idcita,idreceta,atendido,descripcion,subtotal)-> None:
        self.idcita=idatencion
        self.idcita=idcita
        self.idreceta=idreceta
        self.atendido=atendido
        self.descripcion=descripcion
        self.subtotal=subtotal
 