from datetime import datetime

class Pedido():
    """
    Modelo que representa un pedido en el sistema.
    """

    def __init__(self, total, fecha_hora, usuario_id, estado='Pendiente', id=None) -> None:
        """
        Inicializa un nuevo pedido.
        Args:
            total (float): Total del pedido.
            fecha_hora (str): Fecha y hora del pedido.
            usuario_id (int): ID del usuario que realiza el pedido.
            estado (str, opcional): Estado del pedido.
            id (int, opcional): ID del pedido (para pedidos existentes).
        """
        self.id = id
        self.total = total
        self.fecha_hora = fecha_hora
        self.usuario_id = usuario_id
        self.estado = estado

    def to_json(self):
        """
        Convierte el pedido a un diccionario JSON serializable.
        Returns:
            dict: Representación JSON del pedido.
        """
        return {
            'id': self.id,
            'total': self.total,
            'fecha_hora': self.fecha_hora,
            'usuario_id': self.usuario_id,
            'estado': self.estado
        }
