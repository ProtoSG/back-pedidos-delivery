from datetime import datetime

class Pedido():

    def __init__(self, total, fecha_hora, usuario_id=None, estado='Pendiente', id=None) -> None:
        self.id = id
        self.usuario_id = int(usuario_id) if usuario_id is not None else None
        # Asegurar que el total siempre sea float
        self.total = float(total) if total else 0.0

        # Manejar la fecha_hora correctamente
        if isinstance(fecha_hora, str):
            try:
                self.fecha_hora = fecha_hora
            except:
                self.fecha_hora = datetime.now().isoformat()
        else:
            self.fecha_hora = datetime.now().isoformat() if fecha_hora is None else str(fecha_hora)

        self.estado = str(estado) if estado else 'Pendiente'

    def to_json(self):
        return {
            'pedido_id': int(self.id) if self.id else None,  # Usar el mismo nombre que en la base de datos
            'usuario_id': int(self.usuario_id) if self.usuario_id else None,
            'total': float(self.total),
            'fecha_hora': str(self.fecha_hora),
            'estado': self.estado
        }
