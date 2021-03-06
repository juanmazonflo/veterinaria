DROP DATABASE IF EXISTS veterinaria;
CREATE DATABASE veterinaria;
USE veterinaria;
CREATE TABLE atencion(
	idatencion int auto_increment NOT NULL,
	idcita int NOT NULL,
	idreceta int NULL,
	atendido bit NULL,
	descripcion varchar(50) NULL,
	subtotal decimal(10, 2) NULL,
 CONSTRAINT PK_atencion PRIMARY KEY CLUSTERED 
(
	idatencion ASC
)
);

CREATE TABLE citas(
	idcita int auto_increment NOT NULL,
	idmascota int NOT NULL,
	idservicio int NOT NULL,
	fecha date NOT NULL,
	hora time(6) NOT NULL,
 CONSTRAINT PK_citas PRIMARY KEY CLUSTERED 
(
	idcita ASC
)
);

CREATE TABLE mascotas(
	idmascota int auto_increment NOT NULL,
	idusuario int NOT NULL,
	tipo varchar(30) NOT NULL,
	nombre varchar(40) NULL,
 CONSTRAINT PK_mascotas PRIMARY KEY CLUSTERED 
(
	idmascota ASC
)
);

CREATE TABLE medicinas(
	idmedicina int auto_increment NOT NULL,
	descripcion varchar(100) NOT NULL,
	presentacion varchar(10) NOT NULL,
	medida varchar(10) NOT NULL,
	precio decimal(10, 2) NOT NULL,
 CONSTRAINT PK_medicinas PRIMARY KEY CLUSTERED 
(
	idmedicina ASC
)
);

CREATE TABLE recetas(
	idreceta int auto_increment NOT NULL,
	idmascota int NOT NULL,
	fecha date NOT NULL,
	descripcion varchar(200) NOT NULL,
 CONSTRAINT PK_recetas PRIMARY KEY CLUSTERED 
(
	idreceta ASC
)
);

CREATE TABLE recetasmedicinas(
	idrecetamedicina int auto_increment NOT NULL,
	idreceta int NOT NULL,
	idmedicina int NOT NULL,
	cantidad int NOT NULL,
 CONSTRAINT PK_recetasmedicinas PRIMARY KEY CLUSTERED 
(
	idrecetamedicina ASC
)
);

CREATE TABLE servicios(
	idservicio int auto_increment NOT NULL,
	servicio varchar(30) NOT NULL,
	precio decimal(10, 2) NOT NULL,
 CONSTRAINT PK_servicios PRIMARY KEY CLUSTERED 
(
	idservicio ASC
)
);

CREATE TABLE usuarios(
	idusuario int auto_increment NOT NULL,
	username varchar(20) NOT NULL,
	password char(102) NOT NULL,
	nombre varchar(50) NOT NULL,
	email varchar(30) NOT NULL,
	tipo varchar(15) NOT NULL,
 CONSTRAINT PK_usuarios PRIMARY KEY CLUSTERED 
(
	idusuario ASC
)
);

ALTER TABLE atencion ADD CONSTRAINT FK_atencion_citas FOREIGN KEY(idcita)
REFERENCES citas (idcita);

ALTER TABLE atencion ADD CONSTRAINT FK_atencion_recetas FOREIGN KEY(idreceta)
REFERENCES recetas (idreceta);

ALTER TABLE citas ADD CONSTRAINT FK_citas_mascotas FOREIGN KEY(idmascota)
REFERENCES mascotas (idmascota);

ALTER TABLE citas ADD CONSTRAINT FK_citas_servicios FOREIGN KEY(idservicio)
REFERENCES servicios (idservicio);

ALTER TABLE mascotas ADD CONSTRAINT FK_mascotas_usuarios FOREIGN KEY(idusuario)
REFERENCES usuarios (idusuario);

ALTER TABLE recetas ADD CONSTRAINT FK_recetas_mascotas FOREIGN KEY(idmascota)
REFERENCES mascotas (idmascota);

ALTER TABLE recetasmedicinas ADD CONSTRAINT FK_recetasmedicinas_medicinas FOREIGN KEY(idmedicina)
REFERENCES medicinas (idmedicina);

ALTER TABLE recetasmedicinas ADD CONSTRAINT FK_recetasmedicinas_recetas FOREIGN KEY(idreceta)
REFERENCES recetas (idreceta);

INSERT INTO usuarios VALUES (1,'admin','pbkdf2:sha256:150000$zz9A88lq$d39fe9808e418220448325d31402bb5ff4149272c28f380cfecb0888d285b8c2','Hiram Flores','hiram@hiram.com','admin');