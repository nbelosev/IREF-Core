# =====================================
# IREF Core Engine
# =====================================

from core.constants import TIPO_CREDITOS_ESTUDIANTILES
from core.detector import detectar_tipo
from parsers.parser_creditos_estudiantiles import ParserCreditosEstudiantiles


class IREFCore:
    """
    Orquestador general: detecta el tipo de resolución
    y delega en el parser correspondiente (todos cumplen
    el contrato de ParserBase: procesar(texto) -> list[dict]).
    """

    def __init__(self):
        self._parsers = {
            TIPO_CREDITOS_ESTUDIANTILES:ParserCreditosEstudiantiles(),
            # TIPO_BECAS_INVESTIGACION: ParserBecasInvestigacion(),
            # ...futuros parsers se agregan acá, sin tocar procesar()
        }

    def procesar(self, texto):
        tipo = detectar_tipo(texto)

        parser = self._parsers.get(tipo)

        if parser is None:
            raise ValueError(
                f"Tipo de resolución no soportado: {tipo}"
            )

        return parser.procesar(texto)

