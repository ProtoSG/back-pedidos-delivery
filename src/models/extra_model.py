class Extra():

    def __init__(self, nombre, precio, id = None) -> None:
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def to_json(self):
        return {
            'id' : self.id,
            'nombre' : self.nombre,
            'precio' : self.precio
        }