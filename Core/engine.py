# =====================================
# IREF Core Engine
# =====================================

from core.detector import detectar_tipo

from parsers import parser_creditos_estudiantiles

from core.constants import TIPO_CREDITOS_ESTUDIANTILES

class IREFCore:

    def procesar(self, texto):

        tipo = detectar_tipo(texto)

        if tipo == TIPO_CREDITOS_ESTUDIANTILES:
            return parser_creditos_estudiantiles.procesar(texto)

        raise ValueError(
            f"Tipo de resolución no soportado: {tipo}"
        )