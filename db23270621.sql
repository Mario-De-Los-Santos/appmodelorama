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
(1, 'Mario', 'Ruiz', 9612659586, 'Cajero');

-- Tabla Categoría
CREATE TABLE IF NOT EXISTS Categoria (
  idCategoria INT PRIMARY KEY,
  nombre_categoria VARCHAR(45),
  descripcion_categoria VARCHAR(45)
) ENGINE=InnoDB;

INSERT INTO Categoria (idCategoria, nombre_categoria, descripcion_categoria)
VALUES
(1, 'Refrescos', 'Refrescos embotellados');

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
(7, 'Caja');

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

INSERT INTO Producto (codigo, nombre_producto, precio_producto, stock, idCategoria, idUnidad) VALUES
('7501055310227', 'Coca Cola Retornable', 45.0, 22, 1, 1),
('7501055377022', 'Senzao Guaraná', 32.0, 15, 1, 1);

-- Tabla Cliente
CREATE TABLE IF NOT EXISTS Cliente (
  telefono CHAR(10) PRIMARY KEY,
  nombre_cliente VARCHAR(45),
  RFC CHAR(13)
) ENGINE=InnoDB;

INSERT INTO Cliente (telefono, nombre_cliente, RFC)
VALUES
(9612659585, 'Mario De Los Santos', 'F2438689D341W'),
(9611234567, 'Dorian Marroquín', 'DOA12127Y4JS2');

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
  idVenta INT PRIMARY KEY,
  fecha_venta DATETIME,
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
  direccion_proveedor VARCHAR(45),
  telefono_proveedor VARCHAR(45)
) ENGINE=InnoDB;

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
  total DECIMAL(10,2),
  PRIMARY KEY (idVenta, codigo),
  FOREIGN KEY (idVenta) REFERENCES Venta(idVenta),
  FOREIGN KEY (codigo) REFERENCES Producto(codigo)
) ENGINE=InnoDB;
