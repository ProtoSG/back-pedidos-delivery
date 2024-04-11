class Extra():

    def __init__(self, nombre, precio, imagen_url, id = None) -> None:
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.imagen_url = imagen_url

    def to_json(self):
        return {
            'id' : self.id,
            'nombre' : self.nombre,
            'precio' : self.precio,
            'imagen_url' : self.imagen_url
        }