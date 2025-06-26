DROP TABLE if EXISTS Notificacion;
DROP TABLE if EXISTS Pedido_Extra;
DROP TABLE if EXISTS Pedido_Producto;
DROP TABLE if EXISTS Extra;
DROP TABLE if EXISTS Pedido;
DROP TABLE if EXISTS Producto;
DROP TABLE if EXISTS Categoria;
DROP TABLE if EXISTS Admin;
DROP TABLE if EXISTS Usuario;

CREATE TABLE Admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE Usuario (
    usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE Categoria (
    categoria_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE Producto (
    producto_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria_id INTEGER,
    precio REAL NOT NULL,
    descripcion TEXT,
    imagen_url TEXT,
    FOREIGN KEY (categoria_id) REFERENCES Categoria(categoria_id)
);

CREATE TABLE Extra (
    extra_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    imagen_url TEXT
);

CREATE TABLE Pedido (
    pedido_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    total REAL,
    fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado TEXT DEFAULT 'Pendiente',
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id)
);

CREATE TABLE Pedido_Producto (
    pedido_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    sub_total REAL,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id),
    FOREIGN KEY (producto_id) REFERENCES Producto(producto_id)
);

CREATE TABLE Pedido_Extra (
    pedido_id INTEGER,
    extra_id INTEGER,
    cantidad INTEGER,
    sub_total REAL,
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id),
    FOREIGN KEY (extra_id) REFERENCES Extra(extra_id)
);

CREATE TABLE Notificacion (
    notificacion_id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    pedido_id INTEGER,
    mensaje TEXT NOT NULL,
    tipo TEXT DEFAULT 'info',
    leida BOOLEAN DEFAULT FALSE,
    fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(usuario_id),
    FOREIGN KEY (pedido_id) REFERENCES Pedido(pedido_id)
);
