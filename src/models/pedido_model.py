class Pedido():

    def __init__(self, cliente_id, total, fecha_hora,  id = None) -> None:
        self.id = id
        self.cliente_id = cliente_id
        self.total = total
        self.fecha_hora = fecha_hora

    def to_json(self):
        return {
            'id' : self.id,
            'cliente_id' : self.cliente_id,
            'total' : self.total,
            'fecha hora' : self.fecha_hora
        }