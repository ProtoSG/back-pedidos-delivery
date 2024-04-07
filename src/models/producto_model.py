class Producto():

    def __init__(self, nombre, categoria_id, precio, id = None) -> None:
        self.id = id
        self.nombre = nombre
        self.categoria_id = categoria_id
        self.precio = precio

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria_id,
            'precio': self.precio
        }
