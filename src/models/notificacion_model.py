class Notificacion():
    def __init__(self, usuario_id, pedido_id, mensaje, tipo='info', notificacion_id=None, leida=False, fecha_envio=None) -> None:
        self.id = notificacion_id
        self.usuario_id = usuario_id
        self.pedido_id = pedido_id
        self.mensaje = mensaje
        self.tipo = tipo
        self.leida = leida
        self.fecha_envio = fecha_envio

    def to_json(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'pedido_id': self.pedido_id,
            'mensaje': self.mensaje,
            'tipo': self.tipo,
            'leida': self.leida,
            'fecha_envio': self.fecha_envio
        }
