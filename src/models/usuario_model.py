class Usuario():
    def __init__(self, nombre, email, password, usuario_id=None, fecha_registro=None, activo=True) -> None:
        self.id = usuario_id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.fecha_registro = fecha_registro
        self.activo = activo

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'fecha_registro': self.fecha_registro,
            'activo': self.activo
        }

    def to_json_with_password(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'password': self.password,
            'fecha_registro': self.fecha_registro,
            'activo': self.activo
        }
