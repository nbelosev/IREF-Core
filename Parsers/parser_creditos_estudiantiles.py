import re

from parsers.parser_base import ParserBase


class ParserCreditosEstudiantiles(ParserBase):
    """
    Parser de resoluciones de créditos estudiantiles (FIUBA).
    Extrae, por cada artículo con créditos, el/los alumno(s),
    padrón(es), actividad y cantidad de créditos.
    """

    # ------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------

    def limpiar_texto(self, texto):
        return " ".join(
            texto.replace("\n", " ").split()
        )

    # ------------------------------------------------------------
    # Extracción de campos individuales
    # ------------------------------------------------------------

    def extraer_creditos(self, articulo):

        match = re.search(
            r"\((\d+)\)\s*crédit",
            articulo,
            re.IGNORECASE
        )

        if match:
            return match.group(1)

        return ""

    def extraer_padron(self, articulo):

        match = re.search(
            r"Leg\.\s*N[º°]\s*(\d{2,3}\.\d{3})",
            articulo,
            re.IGNORECASE
        )

        if match:
            return match.group(1).replace(".", "")

        return ""

    def extraer_alumno(self, articulo):

        match = re.search(
            r",\s+a\s+(.+?),\s+Leg",
            articulo,
            re.IGNORECASE | re.DOTALL
        )

        if match:
            return self.limpiar_texto(
                match.group(1)
            )

        return ""

    # ------------------------------------------------------------
    # NUEVO: soporte para resoluciones GRUPALES (varios alumnos)
    # ------------------------------------------------------------

    def extraer_alumnos_grupal(self, articulo):
        """
        Devuelve una lista de dicts {"alumno": ..., "padron": ...}
        cuando el artículo contiene un listado de varios estudiantes.

        Soporta dos formatos vistos en las resoluciones de FIUBA:

        Formato A (listado simple, con "Leg. Nº"):
            DIAZ COLINA Sergio Ignacio Leg. Nº 98.841 Plan 2023
            MOCNIK Andrés Leg. Nº 108.875 Plan 2023

        Formato B (tabla numerada, sin "Leg."):
            1 BONILLA IBARRA Morgana Emilia 112.588 2023
            2 CLAUDIO TRUJILLO Mario Vinicio 105.847 2023
        """

        alumnos = []

        # --- Formato A: "NOMBRE Leg. Nº XX.XXX [Plan AAAA]" ---
        for match in re.finditer(
            r"([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ\.\s]*?)\s+"
            r"Leg\.\s*N[º°]\s*(\d{2,3}\.\d{3})"
            r"(?:\s*Plan\s*\d{4})?",
            articulo
        ):
            nombre = self.limpiar_texto(match.group(1))
            padron = match.group(2).replace(".", "")

            alumnos.append({
                "alumno": nombre,
                "padron": padron
            })

        if alumnos:
            return alumnos

        # --- Formato B y C: procesamiento línea por línea para tablas ---
        for linea in articulo.split("\n"):

            # Limpiamos comillas y comas, ruido común de tablas extraídas como texto
            linea_limpia = linea.replace('"', "").replace(",", " ").strip()

            # Omitir encabezados de la tabla si aparecen en el artículo
            if "Apellido y Nombre" in linea_limpia or "Legajo" in linea_limpia:
                continue

            # Regex flexible: el número de orden puede estar antes del nombre,
            # pegado después del nombre (extracción desalineada), o ausente.
            match = re.search(
                r"(?:\d+\s+)?"
                r"([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ\s]+?)"
                r"(?:\s+\d+)?\s+"
                r"(\d{2,3}\.\d{3})\s+"
                r"(?:\d{4}|\d{4}\s*[A-Z])",
                linea_limpia
            )

            if match:
                nombre = self.limpiar_texto(match.group(1))
                padron = match.group(2).replace(".", "")

                alumnos.append({
                    "alumno": nombre,
                    "padron": padron
                })

        return alumnos

    def extraer_actividad(self, articulo):

        patrones = [

            # Aprobar la asignatura (Ferreiro, etc.)
            r'aprobar\s+la\s+asignatura\s+(.+?),\s+a\s',

            # Curso de Posgrado
            r'Curso\s+de\s+Posgrado\s+[“"]?\s*(.+?)[”"]\s*,?\s+a\s',

            # Curso de Complementación
            r'Curso de Complementación\s+[“"]?\s*(.+?)[”"]\s*,?\s+a\s',

            # Actividad extracurricular (resoluciones grupales)
            r'actividad\s+extracurricular\s+[“"]?\s*(.+?)[”"]\s*,?\s+a\s',

            # Curso realizado de "..." (ARFITEC y similares)
            r'curso\s+realizado\s+de\s+[“"]?\s*(.+?)[”"]\s*,?\s+a\s',

            # Pasantía
            r'crédito[s]?\s+por\s+la\s+(.+?),\s+a\s',

            # Actividad genérica
            r'crédito[s]?\s+por\s+el\s+(.+?),\s+a\s',

            # Curso simple (Green Belt)
            r'crédito[s]?\s+por\s+aprobar\s+el\s+Curso\s+de\s+([^,]+),\s+a\s',

            # Curso entre comillas
            r'crédito[s]?\s+por\s+aprobar\s+el\s+Curso\s+de\s+[“"]\s*(.+?)\s*[”"]\s*,?\s+a\s',

            # Genérico: "por aprobar el X, a" (sin la palabra "Curso de")
            r'crédito[s]?\s+por\s+aprobar\s+el\s+(.+?),\s+a\s',

            # Actividad mencionada DESPUÉS del alumno:
            # "..., a NOMBRE, Leg. Nº ..., estudiante de la Carrera de X, por la/el ACTIVIDAD."
            r'estudiante\s+de\s+la\s+Carrera\s+de\s+[^,\.]+,?\s+por\s+(?:la|el)\s+(.+?)\.',
        ]

        for patron in patrones:

            match = re.search(
                patron,
                articulo,
                re.IGNORECASE | re.DOTALL
            )

            if match:

                actividad = self.limpiar_texto(
                    match.group(1)
                )

                actividad = actividad.strip(
                    ' "“”'
                )

                # Quita comillas sueltas que hayan quedado
                # en medio del texto (no solo en los bordes)
                actividad = actividad.replace(
                    '"', ''
                ).replace(
                    '“', ''
                ).replace(
                    '”', ''
                ).strip()

                return actividad

        return ""

    def extraer_actividades_visto(self, texto):

        actividades = []

        match_visto = re.search(
            r'V\s*I\s*S\s*T\s*O:(.*?)(?=CONSIDERANDO:)',
            texto,
            re.IGNORECASE | re.DOTALL
        )

        if not match_visto:
            return actividades

        visto = match_visto.group(1)

        # --- Formato A: listado con viñetas "•" ---
        actividades = re.findall(
            r'•\s*(.+)',
            visto
        )

        if actividades:
            return [
                self.limpiar_texto(a)
                for a in actividades
            ]

        # --- Formato B: redactado en prosa ---
        # "...créditos por las actividades realizadas en X
        #  y en Y, y" (sin viñetas)
        match_prosa = re.search(
            r'actividades\s+(?:realizadas|llevadas\s+a\s+cabo|desarrolladas)\s+'
            r'en\s+(.+?),?\s+y\s*$',
            visto,
            re.IGNORECASE | re.DOTALL
        )

        if match_prosa:

            bloque = match_prosa.group(1)

            partes = re.split(
                r'\s+y\s+en\s+',
                bloque,
                flags=re.IGNORECASE
            )

            for parte in partes:

                parte = self.limpiar_texto(parte)

                # Quita artículo inicial ("el ", "la ", etc.)
                parte = re.sub(
                    r'^(el|la|los|las)\s+',
                    '',
                    parte,
                    flags=re.IGNORECASE
                )

                actividades.append(parte)

        return actividades

    # ------------------------------------------------------------
    # Construcción del registro de salida
    # ------------------------------------------------------------

    def crear_registro(
        self,
        alumno: str,
        padron: str,
        actividad: str,
        creditos: str
    ) -> dict:
        """
        Crea un registro estándar de créditos estudiantiles.
        Todas las salidas del parser deben construirse desde aquí.
        """
        return {
            "alumno": alumno,
            "padron": padron,
            "actividad": actividad,
            "creditos": creditos
        }

    # ------------------------------------------------------------
    # Procesamiento por tipo de artículo
    # ------------------------------------------------------------

    def procesar_articulo_grupal(
        self,
        alumnos_grupal,
        articulo,
        actividad,
        creditos,
        actividades_visto
    ):
        """
        Construye los registros de un artículo grupal (varios alumnos).
        Devuelve siempre una lista de registros vía crear_registro().
        """

        registros = []

        # Tipo C grupal: "actividades detalladas en el VISTO"
        if (
            not actividad
            and "detalladas en el visto" in articulo.lower()
            and actividades_visto
        ):

            actividad_combinada = "; ".join(
                actividades_visto
            )

            for alumno in alumnos_grupal:

                registros.append(
                    self.crear_registro(
                        alumno["alumno"],
                        alumno["padron"],
                        actividad_combinada,
                        creditos
                    )
                )

            return registros

        for alumno in alumnos_grupal:

            registros.append(
                self.crear_registro(
                    alumno["alumno"],
                    alumno["padron"],
                    actividad,
                    creditos
                )
            )

        return registros

    def procesar_articulo_individual(
        self,
        articulo,
        actividad,
        creditos,
        actividades_visto
    ):
        """
        Construye el registro de un artículo individual (un solo alumno).
        Devuelve siempre una lista de un único registro vía crear_registro().
        """

        alumno = self.extraer_alumno(
            articulo
        )

        padron = self.extraer_padron(
            articulo
        )

        # Tipo C individual: "actividades detalladas en el VISTO"
        if (
            not actividad
            and "detalladas en el visto" in articulo.lower()
            and actividades_visto
        ):

            actividad_combinada = "; ".join(
                actividades_visto
            )

            return [
                self.crear_registro(
                    alumno,
                    padron,
                    actividad_combinada,
                    creditos
                )
            ]

        return [
            self.crear_registro(
                alumno,
                padron,
                actividad,
                creditos
            )
        ]

    # ------------------------------------------------------------
    # Punto de entrada
    # ------------------------------------------------------------

    def procesar(self, texto):

        resultados = []

        actividades_visto = self.extraer_actividades_visto(
            texto
        )

        articulos = re.findall(
            r'(Art[ií]culo\s+\d+[º°].*?)(?=Art[ií]culo\s+\d+[º°]|$)',
            texto,
            re.IGNORECASE | re.DOTALL
        )

        for articulo in articulos:

            creditos = self.extraer_creditos(
                articulo
            )

            if not creditos:
                continue

            actividad = self.extraer_actividad(
                articulo
            )

            # ¿El artículo tiene varios alumnos (caso grupal)?
            alumnos_grupal = self.extraer_alumnos_grupal(
                articulo
            )

            if len(alumnos_grupal) > 1:

                resultados.extend(
                    self.procesar_articulo_grupal(
                        alumnos_grupal,
                        articulo,
                        actividad,
                        creditos,
                        actividades_visto
                    )
                )

                continue

            # --- Caso individual (un solo alumno) ---

            resultados.extend(
                self.procesar_articulo_individual(
                    articulo,
                    actividad,
                    creditos,
                    actividades_visto
                )
            )

        return resultados
