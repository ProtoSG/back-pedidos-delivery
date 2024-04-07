class Pedido_Extra():

    def __init__(self, pedido_id, extra_id, cantidad, sub_total) -> None:
        self.pedido_id = pedido_id
        self.extra_id = extra_id
        self.cantidad = cantidad
        self.sub_total = sub_total

    def to_json(self):
        return {
            'pedido_id' : self.pedido_id,
            'extra_id' : self.extra_id,
            'cantidad' : self.cantidad,
            'sub_total' : self.sub_total
        }