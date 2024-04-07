class Categoria():

    def __init__(self, nombre, id = None) -> None:
        self.id = id
        self.nombre = nombre

    def to_json(self):
        return {
            'id' : self.id,
            'nombre' : self.nombre
        }