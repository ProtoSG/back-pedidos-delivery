class Notificacion():
    """
    Modelo que representa una notificación en el sistema.
    """

    def __init__(self, usuario_id, pedido_id, mensaje, tipo, leida=False, id=None) -> None:
        """
        Inicializa una nueva notificación.
        Args:
            usuario_id (int): ID del usuario.
            pedido_id (int): ID del pedido relacionado.
            mensaje (str): Mensaje de la notificación.
            tipo (str): Tipo de notificación.
            leida (bool, opcional): Estado de lectura.
            id (int, opcional): ID de la notificación (para notificaciones existentes).
        """
        self.id = id
        self.usuario_id = usuario_id
        self.pedido_id = pedido_id
        self.mensaje = mensaje
        self.tipo = tipo
        self.leida = leida

    def to_json(self):
        """
        Convierte la notificación a un diccionario JSON serializable.
        Returns:
            dict: Representación JSON de la notificación.
        """
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'pedido_id': self.pedido_id,
            'mensaje': self.mensaje,
            'tipo': self.tipo,
            'leida': self.leida
        }
