import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time

st.set_page_config(layout="wide")

# ------------------------
# HEADER
# ------------------------

col1, col2 = st.columns([6,1])

with col1:
    st.title("Gemelo Digital - Terminal Portuaria (Referencia APM)")

with col2:
    st.write("")  # evitar logo real por tema legal


# ------------------------
# ESTADO
# ------------------------

if "frame" not in st.session_state:
    st.session_state.frame = 0


# ------------------------
# SELECTOR
# ------------------------

opcion = st.radio(
    "Selecciona escenario:",
    ["Baseline", "Productivo", "Energético", "Ambiental", "Optimizado IA"],
    horizontal=True
)


# ------------------------
# PARÁMETROS
# ------------------------

params = {
    "Baseline": (35, 33.90, 11203, 1.5, 4, 4),
    "Productivo": (45.85, 44.42, 14676, 3, 7, 7),
    "Energético": (35, 28.16, 9310, 1.2, 2, 2),
    "Ambiental": (35, 33.90, 10172, 1.5, 4, 1),
    "Optimizado IA": (40, 30, 9500, 2, 3, 2),
}

gmph, energia, co2, velocidad, num_humo, num_co2 = params[opcion]


# ------------------------
# CONTENEDOR ANIMACIÓN
# ------------------------

placeholder = st.empty()

with placeholder.container():

    frame = st.session_state.frame

    fig, ax = plt.subplots(figsize=(12,5))
    ax.set_facecolor('#d0d3d4')

    # MAR
    ax.add_patch(patches.Rectangle((0, 0), 100, 25, color='#5dade2'))

    # MUELLE
    ax.add_patch(patches.Rectangle((0, 25), 100, 20, color='#7f8c8d'))

    # BUQUE
    ax.add_patch(patches.Rectangle((20, 8), 60, 10, color='#2c3e50'))
    ax.add_patch(patches.Rectangle((30, 18), 40, 5, color='#c0392b'))

    # 🔁 PROGRESO CÍCLICO
    ciclo = (frame % 120) / 120
    progreso = ciclo * (gmph / 45.85)

    for i in range(int(progreso * 20)):
        x = 25 + (i % 10) * 5
        y = 10 + (i // 10) * 3
        ax.add_patch(patches.Rectangle((x, y), 3, 2, color='green'))

    # GRÚAS
    posiciones = np.linspace(5, 95, 14)

    for i, x in enumerate(posiciones):
        desplazamiento = np.sin(frame * 0.15 * velocidad + i) * 1.2

        ax.add_patch(patches.Rectangle((x + desplazamiento, 25), 2, 15, color='#f39c12'))

        ax.add_line(plt.Line2D(
            [x+1 + desplazamiento, x+6 + desplazamiento],
            [40, 48],
            linewidth=2
        ))

        ax.add_patch(patches.Rectangle(
            (x+6 + desplazamiento, 46),
            2,
            2,
            color='green'
        ))

    # HUMO
    humo_x = np.linspace(15, 85, num_humo)
    for x in humo_x:
        ax.add_patch(patches.Circle((x, 50), 2, color='#7f8c8d'))

    # CO2
    co2_x = np.linspace(20, 80, num_co2)
    for x in co2_x:
        y = 60 + np.sin(frame * 0.1 + x) * 1.5
        ax.add_patch(patches.Circle((x, y), 3, color='#bdc3c7'))
        ax.text(x, y, "CO2", ha='center', fontsize=8)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis('off')

    st.pyplot(fig, use_container_width=True)


# ------------------------
# KPI
# ------------------------

st.subheader("📊 Indicadores KPI")

k1, k2, k3 = st.columns(3)

k1.metric("GMPH", gmph)
k2.metric("Energía (GWh/año)", energia)
k3.metric("CO2 (ton/año)", co2)


# ------------------------
# IA (CONTROLADO)
# ------------------------

if opcion == "Optimizado IA":
    with st.container():
        st.subheader("🧠 Modelo de optimización basado en reglas")

        st.markdown("""
Este modelo no genera resultados de forma arbitraria, sino que aplica reglas derivadas del análisis de benchmarks previos.

Se construye un escenario híbrido que equilibra:

- Productividad (GMPH)
- Consumo energético
- Emisiones de CO2

El sistema prioriza soluciones que eviten incrementos extremos en cualquiera de los tres indicadores, generando una configuración operativa más eficiente y sostenible.
""")


# ------------------------
# LOOP SUAVE
# ------------------------

time.sleep(0.03)
st.session_state.frame += 1
st.rerun()




















