import streamlit as st
import pdfplumber
import pandas as pd

from core.engine import IREFCore

st.set_page_config(page_title="IREF")

st.title("🎓 Interpretación de Resoluciones Institucionales")


# Modificación de estilos CSS precisa y compatible
st.markdown(
    """
    <style>
        /* 1. Selecciona el contenedor de texto exacto del botón y esconde la palabra "Upload" */
        [data-testid="stFileUploaderDropzone"] button div[data-testid="stMarkdownContainer"] p {
            font-size: 0px !important;
            line-height: 0 !important;
        }

        /* 2. Inyecta el texto en español justo después del ícono de la flecha */
        [data-testid="stFileUploaderDropzone"] button div[data-testid="stMarkdownContainer"] p::after {
            content: "Examinar archivos" !important;
            font-size: 14px !important; /* Devuelve el tamaño normal a la letra */
            line-height: normal !important;
            display: inline-block;
        }
        
        /* 3. Ajusta el ancho mínimo del botón para que no corte la palabra nueva */
        [data-testid="stFileUploaderDropzone"] button {
            min-width: 170px !important;
        }
	/* Traducción y personalización del File Uploader */
        [data-testid="stFileUploaderDropzoneInstructions"] > div > span,
        [data-testid="stFileUploaderDropzoneInstructions"] button span {
            display: none !important;
        }
	[data-testid="stFileUploaderDropzoneInstructions"] > div::before {
            content: "Cargar archivos 200 Mb por Pdf" !important;
        }
        [data-testid="stFileUploaderDropzoneInstructions"] button::after {
            content: "Examinar" !important;
        }


    </style>
    """,
    unsafe_allow_html=True
)

# El componente original nativo que funciona perfectamente al hacer clic
archivos = st.file_uploader(
    "Seleccioná uno o varios PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if archivos:

    if st.button("🚀 Procesar Resoluciones"):

        resultados = []
        motor = IREFCore()

        for archivo in archivos:

            texto_completo = ""

            with pdfplumber.open(archivo) as pdf:

                for pagina in pdf.pages:

                    texto_completo += (
                        pagina.extract_text() or ""
                    ) + "\n"


            datos = motor.procesar(texto_completo )

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
