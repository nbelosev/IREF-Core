import streamlit as st
import pdfplumber
import pandas as pd

from core.engine import IREFCore

st.set_page_config(page_title="IREF")

st.title("🎓 Interpretación de Resoluciones Institucionales")

archivos = st.file_uploader(
    "Seleccioná uno o varios PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if archivos:

    if st.button("🚀 Procesar Resoluciones"):

        resultados = []

        for archivo in archivos:

            texto_completo = ""

            with pdfplumber.open(archivo) as pdf:

                for pagina in pdf.pages:

                    texto_completo += (
                        pagina.extract_text() or ""
                    ) + "\n"

            motor = IREFCore()

            datos = motor.procesar(texto)

            for fila in datos:

                resultados.append({
                    "archivo": archivo.name,
                    "alumno": fila["alumno"],
                    "padron": fila["padron"],
                    "actividad": fila["actividad"],
                    "creditos": fila["creditos"]
                })

        df = pd.DataFrame(resultados)

        if not df.empty:
            df = df.sort_values(
                by=["archivo", "alumno"]
            )

        st.subheader("Vista previa")

        st.dataframe(df)

        df.to_excel(
            "reporte.xlsx",
            index=False
        )

        with open(
            "reporte.xlsx",
            "rb"
        ) as f:

            st.download_button(
                "📥 Descargar Excel",
                f,
                file_name="IREF_Indice_Resoluciones.xlsx"
            )
