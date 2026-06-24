from dataclasses import dataclass

@dataclass
class Registro:

    alumno: str

    padron: str

    actividad: str

    creditos: str

    archivo: str = ""