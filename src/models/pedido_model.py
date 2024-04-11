class Pedido():

    def __init__(self, total, fecha_hora,  id = None) -> None:
        self.id = id
        self.total = total
        self.fecha_hora = fecha_hora

    def to_json(self):
        return {
            'id' : self.id,
            'total' : self.total,
            'fecha hora' : self.fecha_hora
        }