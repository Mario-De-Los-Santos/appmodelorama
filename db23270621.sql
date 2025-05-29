-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS modelorama DEFAULT CHARACTER SET utf8;
USE modelorama;

-- Tabla Empleado
CREATE TABLE IF NOT EXISTS Empleado (
  idEmpleado INT AUTO_INCREMENT PRIMARY KEY,
  nombre_empleado VARCHAR(45),
  apellido_empleado VARCHAR(45),
  numero_empleado CHAR(10),
  puesto VARCHAR(35)
) ENGINE=InnoDB;

INSERT INTO Empleado (idEmpleado, nombre_empleado, apellido_empleado, numero_empleado, puesto)
VALUES
(1, 'Mario', 'Ruiz', '9612659586', 'Cajero'),
(2, 'Angel Fernando', 'Tovar Hernandez', '9612345678', 'Cajero');

-- Tabla Categoría
CREATE TABLE IF NOT EXISTS categoria (
  idCategoria INT PRIMARY KEY,
  nombre_categoria VARCHAR(45),
  descripcion_categoria VARCHAR(45)
) ENGINE=InnoDB;


-- Insertar registros en Categoria
INSERT INTO categoria (idCategoria, nombre_categoria, descripcion_categoria) VALUES
(1, 'Refrescos', 'Refrescos embotellados'),
(2, 'Cerveza', 'Cervezas claras y oscuras'),
(3, 'Licores', 'Licores de todo tipo'),
(4, 'Sabritas y snacks', 'Sabritas y snacks de todo tipo'),
(5, 'Salsas', 'Salsas picantes para botanas');

-- Tabla Unidad
CREATE TABLE IF NOT EXISTS Unidad (
  idUnidad INT PRIMARY KEY,
  tipo_unidad VARCHAR(45)
) ENGINE=InnoDB;

-- Insertar registros en Unidad
INSERT INTO Unidad (idUnidad, tipo_unidad) VALUES 
(1, 'Litro'),
(2, 'Mililitro'),
(3, 'Gramo'),
(4, 'Kilogramo'),
(5, 'Botella'),
(6, 'Lata'),
(7, 'Caja'),
(8, 'Bolsa');

-- Tabla Producto
CREATE TABLE IF NOT EXISTS Producto (
  codigo CHAR(13) PRIMARY KEY,
  nombre_producto VARCHAR(45),
  precio_producto FLOAT,
  stock INT,
  idCategoria INT NOT NULL,
  idUnidad INT NOT NULL,
  FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria),
  FOREIGN KEY (idUnidad) REFERENCES Unidad(idUnidad)
) ENGINE=InnoDB;

-- Insertar registros en Producto
INSERT INTO Producto (codigo, nombre_producto, precio_producto, stock, idCategoria, idUnidad) VALUES
('7501055310227', 'Coca Cola Retornable', 45.0, 22, 1, 1),
('7501055377022', 'Senzao Guarana', 32.0, 15, 1, 1),
('7501064103100', 'Corona Extra', 22.0, 12, 2, 5),
('7501049928742', 'Superior', 21.0, 23, 2, 6),
('7501049967062', 'Sol Clamato', 25.0, 15, 2, 6),
('7501061696988', 'Indio', 23.0, 19, 2, 6),
('7501064196935', 'Modelo Oscura', 25.0, 32, 2, 6),
('7501035103124', 'Tequila 1800 Reposado', 690, 15, 3, 5),
('7500810024546', 'Chips Fuego', 21, 26, 4, 8),
('7500478044214', 'Cheetos Bolita', 16.0, 18, 4, 8),
('7501011143586', 'Cheetos Torciditos', 16.0, 29, 4, 8),
('5410316950527', 'Vodka Smirnoff X1 Tamarindo', 355.0, 30, 3, 5),
('7501035042322', 'Tequila José Cuervo Silver 750 ml', 199.0, 15, 3, 5),
('7501145214138', 'Tequila Antiguo Herradura 700 ml', 359.0, 22, 3, 5),
('0097339000054', 'Salsa Valentina Picante 370 ml', 24.00, 40, 5, 5),
('0097339000061', 'Salsa Valentina Negra 370 ml', 24.00, 30, 5, 5),
('7501064190124', 'Corona Light 355 ml', 22.0, 23, 2, 6),
('7501011101456', 'Papas Sabritas Sal 45 g', 25.00, 15, 4, 8),
('7501011133921', 'Papas Sabritas Adobadas 170 g', 55.70, 12, 4, 8),
('7501064190414', 'Pacífico Clara 355 ml', 22.0, 23, 2, 6),
('7501064195310', 'Victoria Lata 355 ml', 21.0, 33, 2, 6);


-- Tabla Cliente
CREATE TABLE IF NOT EXISTS Cliente (
  telefono CHAR(10) PRIMARY KEY,
  nombre_cliente VARCHAR(45),
  RFC CHAR(13)
) ENGINE=InnoDB;

-- Insertar Registros en Cliente
INSERT INTO Cliente (telefono, nombre_cliente, RFC)
VALUES
('9612659585', 'Mario De Los Santos', 'F2438689D341W'),
('9611234567', 'Dorian Marroquin', 'DOA12127Y4JS2');

-- Tabla Método de Pago
CREATE TABLE IF NOT EXISTS Metodo_Pago (
  idMetodo_pago INT PRIMARY KEY,
  nombre_del_pago VARCHAR(45)
) ENGINE=InnoDB;

INSERT INTO Metodo_Pago (idMetodo_pago, nombre_del_pago)
VALUES
(1, 'Efectivo'),
(2, 'Tarjeta');

-- Tabla Venta
CREATE TABLE IF NOT EXISTS Venta (
  idVenta INT AUTO_INCREMENT PRIMARY KEY,
  fecha_venta DATE,
  total DECIMAL(10,2),
  idEmpleado INT NOT NULL,
  telefono_cliente CHAR(10) NOT NULL,
  idMetodo_pago INT NOT NULL,
  FOREIGN KEY (idEmpleado) REFERENCES Empleado(idEmpleado),
  FOREIGN KEY (telefono_cliente) REFERENCES Cliente(telefono),
  FOREIGN KEY (idMetodo_pago) REFERENCES Metodo_Pago(idMetodo_pago)
) ENGINE=InnoDB;

-- Tabla Proveedor
CREATE TABLE IF NOT EXISTS Proveedor (
  idProveedor INT PRIMARY KEY,
  nombre_proveedor VARCHAR(45),
  direccion_proveedor VARCHAR(100),
  telefono_proveedor CHAR(10)
) ENGINE=InnoDB;

-- Insertar Registros en Proveedor
INSERT INTO Proveedor (idProveedor, nombre_proveedor, direccion_proveedor, telefono_proveedor)
VALUES
(1, 'Grupo modelo', '5 Avenida Norte Poniente 2730, 29000, Tuxtla Gutierrez, Chiapas', '9616021829'),
(2, 'Distribuidora Coca-Cola FEMSA','Libramiento Norte Pte 3435, 29020 Tuxtla Gtz, Chiapas', '5515195000'),
(3, 'Grupo Bimbo', 'Libramiento Norte Pte esquina, C. Torreon No 1229, 29020 Teran, Chiapas', '9626995068');

-- Tabla Pedido
CREATE TABLE IF NOT EXISTS Pedido (
  idPedido VARCHAR(45),
  codigo CHAR(13),
  idProveedor INT,
  cantidad INT,
  PRIMARY KEY (idPedido, codigo, idProveedor),
  FOREIGN KEY (codigo) REFERENCES Producto(codigo),
  FOREIGN KEY (idProveedor) REFERENCES Proveedor(idProveedor)
) ENGINE=InnoDB;

-- Tabla Detalles de Venta
CREATE TABLE IF NOT EXISTS Detalles_Venta (
  idVenta INT,
  codigo CHAR(13),
  cantidad INT,
  PRIMARY KEY (idVenta, codigo),
  FOREIGN KEY (idVenta) REFERENCES Venta(idVenta),
  FOREIGN KEY (codigo) REFERENCES Producto(codigo)
) ENGINE=InnoDB;
