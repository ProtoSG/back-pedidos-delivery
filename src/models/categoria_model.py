class Categoria():
    """
    Modelo que representa una categoría en el sistema.
    """

    def __init__(self, nombre, id=None) -> None:
        """
        Inicializa una nueva categoría.
        Args:
            nombre (str): Nombre de la categoría.
            id (int, opcional): ID de la categoría (para categorías existentes).
        """
        self.id = id
        self.nombre = nombre

    def to_json(self):
        """
        Convierte la categoría a un diccionario JSON serializable.
        Returns:
            dict: Representación JSON de la categoría.
        """
        return {
            'id': self.id,
            'nombre': self.nombre
        }