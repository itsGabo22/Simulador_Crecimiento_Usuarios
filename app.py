# app.py

import streamlit as st
from simulation_models import run_simulations
from plotting import create_plots # type: ignore
from analysis import generate_analysis_text
from pdf_generator import create_pdf_report
from datetime import datetime

# --- Configuración inicial de la Página ---
st.set_page_config(
    page_title="Simulador de Crecimiento de Usuarios",
    page_icon="🚀",
    layout="wide"
)

# --- Título y Créditos ---
st.title("Simulador de Crecimiento de Usuarios")
st.write("""
Esta aplicación simula y compara dos modelos de crecimiento de usuarios basados en ecuaciones diferenciales. 
Utiliza los controles en la barra lateral para ajustar los parámetros y observar su impacto en tiempo real. (Made by: Gabriel Paz)
""")

# --- Barra Lateral con Controles (Sliders) ---
st.sidebar.header("Parámetros de Simulación")

r = st.sidebar.slider(
    'Tasa de Crecimiento (r)', 
    min_value=0.01, max_value=1.0, value=0.2, step=0.01,
    help="Representa la tasa intrínseca de crecimiento. Un valor más alto simula un marketing más agresivo."
)
K = st.sidebar.slider(
    'Capacidad Máxima (K)', 
    min_value=1000, max_value=50000, value=10000, step=1000,
    help="El número máximo de usuarios que la plataforma puede soportar de manera sostenible."
)
U0 = st.sidebar.slider(
    'Usuarios Iniciales (U0)', 
    min_value=1, max_value=5000, value=100, step=50,
    help="El número de usuarios al inicio de la simulación (t=0)."
)
a = st.sidebar.slider(
    'Fricción Social (a)', 
    min_value=0.0, max_value=1.0, value=0.1, step=0.05,
    help="Coeficiente de amortiguación en el modelo de 2do orden. Modela la 'resistencia' al crecimiento viral."
)
t_max = st.sidebar.slider(
    'Tiempo de Simulación (días)', 
    min_value=20, max_value=500, value=100, step=10,
    help="Días estimados de las simulación."
)

# --- Ejecución y Visualización ---
st.header("Resultados de la Simulación")

# 1. Ejecutar la simulación con los parámetros actuales
simulation_results = run_simulations(r, K, U0, a, t_max)

# 2. Generar las gráficas a partir de los resultados
fig = create_plots(simulation_results, r, K, a)

# 3. Mostrar la figura en la aplicación de Streamlit
st.pyplot(fig)

# --- Análisis e Interpretación Profesional ---
st.header("Análisis e Interpretación de los Modelos")

# 4. Generar y mostrar el análisis dinámico
analysis_text = generate_analysis_text(simulation_results, r, K, U0, a, t_max)
st.markdown(analysis_text, unsafe_allow_html=True)

# --- Funcionalidad de Descarga de PDF ---
st.sidebar.markdown("---")
st.sidebar.header("Descargar Reporte")

# 1. Recolectar parámetros en un diccionario
params = {
    "Tasa de Crecimiento (r)": r,
    "Capacidad Máxima (K)": K,
    "Usuarios Iniciales (U0)": U0,
    "Fricción Social (a)": a,
    "Tiempo de Simulación (días)": t_max
}

# 2. Generar el PDF en memoria
pdf_bytes = create_pdf_report(params, fig, analysis_text)

# 3. Crear el botón de descarga
st.sidebar.download_button(
    label="Descargar Reporte en PDF",
    data=pdf_bytes,
    file_name=f"reporte_simulacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    mime="application/pdf"
)
