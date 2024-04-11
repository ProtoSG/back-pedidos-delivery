USE delivery;

DROP TABLE if EXISTS Pedido_Extra;
DROP TABLE if EXISTS Pedido_Producto;
DROP TABLE if EXISTS Extra;
DROP TABLE if EXISTS Pedido;
DROP TABLE if EXISTS Producto;
DROP TABLE if EXISTS Categoria;
DROP TABLE if EXISTS Admin;

CREATE TABLE Admin(
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    admin_username VARCHAR(40) NOT NULL,
    admin_password VARCHAR(60) NOT NULL
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
    descripcion VARCHAR(400),
    imagen_url VARCHAR(400),
    FOREIGN KEY (categoria_id) REFERENCES Categoria(categoria_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Extra(
    extra_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40) NOT NULL,
    precio FLOAT NOT NULL,
    imagen_url VARCHAR(400)
);

CREATE TABLE Pedido(
    pedido_id INT AUTO_INCREMENT PRIMARY KEY,
    total FLOAT,
    fecha_hora DATETIME
);

CREATE TABLE Pedido_Producto(
    pedido_id INT,
    producto_id INT,
    cantidad INT,
    sub_total FLOAT,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES Producto(producto_id)
);

CREATE TABLE Pedido_Extra(
    pedido_id INT,
    extra_id INT,
    cantidad INT,
    sub_total FLOAT,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (extra_id) REFERENCES Extra(extra_id) ON DELETE CASCADE ON UPDATE CASCADE
);