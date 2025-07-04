class Extra():
    """
    Modelo que representa un extra en el sistema.
    """

    def __init__(self, nombre, precio, imagen_url, id=None) -> None:
        """
        Inicializa un nuevo extra.
        Args:
            nombre (str): Nombre del extra.
            precio (float): Precio del extra.
            imagen_url (str): URL de la imagen del extra.
            id (int, opcional): ID del extra (para extras existentes).
        """
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.imagen_url = imagen_url

    def to_json(self):
        """
        Convierte el extra a un diccionario JSON serializable.
        Returns:
            dict: Representación JSON del extra.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'imagen_url': self.imagen_url
        }