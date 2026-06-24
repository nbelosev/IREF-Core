import re


def limpiar_texto(texto):
    return " ".join(
        texto.replace("\n", " ").split()
    )


def extraer_creditos(articulo):

    match = re.search(
        r"\((\d+)\)\s*crédit",
        articulo,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


def extraer_padron(articulo):

    match = re.search(
        r"Leg\.\s*N[º°]\s*(\d{2,3}\.\d{3})",
        articulo,
        re.IGNORECASE
    )

    if match:
        return match.group(1).replace(".", "")

    return ""


def extraer_alumno(articulo):

    match = re.search(
        r",\s+a\s+(.+?),\s+Leg",
        articulo,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return limpiar_texto(
            match.group(1)
        )

    return ""


# ----------------------------------------------------------------
# NUEVO: soporte para resoluciones GRUPALES (varios alumnos)
# ----------------------------------------------------------------

def extraer_alumnos_grupal(articulo):
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
        nombre = limpiar_texto(match.group(1))
        padron = match.group(2).replace(".", "")

        alumnos.append({
            "alumno": nombre,
            "padron": padron
        })

    if alumnos:
        return alumnos

    # --- Formato B: tabla numerada "N NOMBRE PADRON AÑO" ---
    for linea in articulo.split("\n"):

        match = re.match(
            r"\s*\d{1,2}\s+"
            r"([A-ZÁÉÍÓÚÑ][A-Za-zÁÉÍÓÚÑáéíóúñ\s]+?)\s+"
            r"(\d{2,3}\.\d{3})\s+"
            r"\d{4}(?:\s*[A-Za-z]+)?\s*$",
            linea
        )

        if match:
            nombre = limpiar_texto(match.group(1))
            padron = match.group(2).replace(".", "")

            alumnos.append({
                "alumno": nombre,
                "padron": padron
            })

    return alumnos


def extraer_actividad(articulo):

    patrones = [

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
        r'crédito[s]?\s+por\s+aprobar\s+el\s+Curso\s+de\s+[“"]\s*(.+?)\s*[”"]\s*,?\s+a\s'
    ]

    for patron in patrones:

        match = re.search(
            patron,
            articulo,
            re.IGNORECASE | re.DOTALL
        )

        if match:

            actividad = limpiar_texto(
                match.group(1)
            )

            actividad = actividad.strip(
                ' "“”'
            )

            return actividad

    return ""


def extraer_actividades_visto(texto):

    actividades = []

    match_visto = re.search(
        r'V\s*I\s*S\s*T\s*O:(.*?)(?=CONSIDERANDO:)',
        texto,
        re.IGNORECASE | re.DOTALL
    )

    if match_visto:

        visto = match_visto.group(1)

        actividades = re.findall(
            r'•\s*(.+)',
            visto
        )

        actividades = [
            limpiar_texto(a)
            for a in actividades
        ]

    return actividades


def procesar(texto):

    resultados = []

    actividades_visto = extraer_actividades_visto(
        texto
    )

    articulos = re.findall(
        r'(Art[ií]culo\s+\d+[º°].*?)(?=Art[ií]culo\s+\d+[º°]|$)',
        texto,
        re.IGNORECASE | re.DOTALL
    )

    for articulo in articulos:

        creditos = extraer_creditos(
            articulo
        )

        if not creditos:
            continue

        actividad = extraer_actividad(
            articulo
        )

        # ¿El artículo tiene varios alumnos (caso grupal)?
        alumnos_grupal = extraer_alumnos_grupal(
            articulo
        )

        if len(alumnos_grupal) > 1:

            # Tipo C grupal: "actividades detalladas en el VISTO"
            if (
                not actividad
                and "detalladas en el visto"
                in articulo.lower()
                and actividades_visto
            ):

                for alumno in alumnos_grupal:
                    for act in actividades_visto:

                        resultados.append({
                            "alumno": alumno["alumno"],
                            "padron": alumno["padron"],
                            "actividad": act,
                            "creditos": creditos
                        })

                continue

            for alumno in alumnos_grupal:

                resultados.append({
                    "alumno": alumno["alumno"],
                    "padron": alumno["padron"],
                    "actividad": actividad,
                    "creditos": creditos
                })

            continue

        # --- Caso individual (un solo alumno) ---

        alumno = extraer_alumno(
            articulo
        )

        padron = extraer_padron(
            articulo
        )

        # Tipo C individual:
        # "actividades detalladas en el VISTO"
        if (
            not actividad
            and "detalladas en el visto"
            in articulo.lower()
            and actividades_visto
        ):

            for act in actividades_visto:

                resultados.append({
                    "alumno": alumno,
                    "padron": padron,
                    "actividad": act,
                    "creditos": creditos
                })

            continue

        resultados.append({
            "alumno": alumno,
            "padron": padron,
            "actividad": actividad,
            "creditos": creditos
        })

    return resultados
