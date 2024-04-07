USE delivery;

DROP TABLE if EXISTS Resumen_Pedido;
DROP TABLE if EXISTS Resumen;
DROP TABLE if EXISTS Pedido_Producto;
DROP TABLE if EXISTS Pedido;
DROP TABLE if EXISTS Producto;
DROP TABLE if EXISTS Categoria;
DROP TABLE if EXISTS Cliente;

CREATE TABLE Cliente(
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    apellido VARCHAR(40) NOT NULL,
    direccion VARCHAR(120) NOT NULL
);

CREATE TABLE Categoria(
    categoria_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40)
);

CREATE TABLE Producto(
    producto_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    categoria_id INT NOT NULL,
    precio FLOAT NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES Categoria(categoria_id)
);

CREATE TABLE Extra(
    extra_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    precio FLOAT NOT NULL
);

CREATE TABLE Pedido(
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    total FLOAT,
    fecha_hora DATETIME,
    FOREIGN KEY (cliente_id) REFERENCES Cliente(cliente_id)
);

CREATE TABLE Pedido_Producto(
    pedido_id INT,
    producto_id INT,
    cantidad INT,
    sub_total FLOAT,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Producto(producto_id)
);

CREATE TABLE Pedido_Extra(
    pedido_id INT,
    extra_id INT,
    cantidad INT,
    sub_total FLOAT,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id),
    FOREIGN KEY (extra_id) REFERENCES Extra(extra_id)
);