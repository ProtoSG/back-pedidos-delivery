class Usuario():
    """
    Modelo que representa un usuario en el sistema.
    """

    def __init__(self, nombre, email, password, id=None, fecha_registro=None, activo=True):
        """
        Inicializa un nuevo usuario.
        Args:
            nombre (str): Nombre del usuario.
            email (str): Email del usuario.
            password (str): Contraseña del usuario.
            id (int, opcional): ID del usuario (para usuarios existentes).
            fecha_registro (str, opcional): Fecha de registro.
            activo (bool, opcional): Estado de actividad del usuario.
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.fecha_registro = fecha_registro
        self.activo = activo

    def to_json(self):
        """
        Convierte el usuario a un diccionario JSON serializable.
        Returns:
            dict: Representación JSON del usuario.
        """
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
