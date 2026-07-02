import re


class ParserBase:
    """
    Clase base para todos los parsers de IREF Core.

    Contiene utilidades comunes reutilizables por cualquier parser.
    """

    def procesar(self, texto: str):
        """
        Método que debe implementar cada parser concreto.
        """
        raise NotImplementedError

    # ---------------------------------------------------------
    # Utilidades comunes
    # ---------------------------------------------------------

    @staticmethod
    def limpiar_texto(texto: str) -> str:
        """
        Elimina espacios duplicados y limpia el texto.
        """
        return re.sub(r"\s+", " ", texto).strip()

    @staticmethod
    def normalizar_padron(padron: str) -> str:
        """
        Elimina puntos y espacios de un padrón.
        """
        return padron.replace(".", "").strip()

    @staticmethod
    def crear_registro(**kwargs) -> dict:
        """
        Construye un registro estándar de IREF Core.
        """
        return kwargs