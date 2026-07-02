class ParserBase:
    """
    Contrato mínimo para cualquier parser de resoluciones.
    Cada parser concreto debe implementar procesar(texto) -> list[dict].
    """

    def procesar(self, texto: str):
        raise NotImplementedError
