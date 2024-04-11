class Producto():

    def __init__(self, nombre, categoria_id, precio, descripcion, imagen_url, id = None) -> None:
        self.id = id
        self.nombre = nombre
        self.categoria_id = categoria_id
        self.precio = precio
        self.descripcion = descripcion
        self.imagen_url = imagen_url

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria_id,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'imagen_url': self.imagen_url
        }
