class Producto():
    """
    Modelo que representa un producto en el sistema.
    """

    def __init__(self, nombre, categoria_id, precio, descripcion, imagen_url, id = None) -> None:
        """
        Inicializa un nuevo producto.
        Args:
            nombre (str): Nombre del producto.
            categoria_id (int): ID de la categoría.
            precio (float): Precio del producto.
            descripcion (str): Descripción del producto.
            imagen_url (str): URL de la imagen del producto.
            id (int, opcional): ID del producto (para productos existentes).
        """
        self.id = id
        self.nombre = nombre
        self.categoria_id = categoria_id
        self.precio = precio
        self.descripcion = descripcion
        self.imagen_url = imagen_url

    def to_json(self):
        """
        Convierte el producto a un diccionario JSON serializable.
        Returns:
            dict: Representación JSON del producto.
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': self.categoria_id,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'imagen_url': self.imagen_url
        }
