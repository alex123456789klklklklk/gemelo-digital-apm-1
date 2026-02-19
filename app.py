import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time
import os

st.set_page_config(layout="wide")

# ------------------------
# HEADER + LOGO
# ------------------------

col_logo, col_title = st.columns([1,5])

with col_logo:
    if os.path.exists("apm_logo.png"):
        st.image("apm_logo.png", width=120)

with col_title:
    st.title("Gemelo Digital - Terminal APM Barcelona")

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
    ["Baseline", "Productivo", "Energético", "Ambiental", "Optimizado IA"]
)

# ------------------------
# PARÁMETROS
# ------------------------

if opcion == "Baseline":
    gmph = 35
    energia = 33.90
    co2 = 11203
    velocidad = 1.5
    num_humo = 4
    num_co2 = 4

elif opcion == "Productivo":
    gmph = 45.85
    energia = 44.42
    co2 = 14676
    velocidad = 3
    num_humo = 7
    num_co2 = 7

elif opcion == "Energético":
    gmph = 35
    energia = 28.16
    co2 = 9310
    velocidad = 1.2
    num_humo = 2
    num_co2 = 2

elif opcion == "Ambiental":
    gmph = 35
    energia = 33.90
    co2 = 10172
    velocidad = 1.5
    num_humo = 4
    num_co2 = 1

elif opcion == "Optimizado IA":
    gmph = 40
    energia = 30
    co2 = 9500
    velocidad = 2
    num_humo = 3
    num_co2 = 2

# ------------------------
# ANIMACIÓN ESTABLE
# ------------------------

placeholder = st.empty()

frame = st.session_state.frame

with placeholder.container():

    fig, ax = plt.subplots(figsize=(14,6))
    ax.set_facecolor('#d0d3d4')

    # MAR
    ax.add_patch(patches.Rectangle((0, 0), 100, 25, color='#5dade2'))

    # MUELLE
    ax.add_patch(patches.Rectangle((0, 25), 100, 20, color='#7f8c8d'))

    # BUQUE
    ax.add_patch(patches.Rectangle((20, 8), 60, 10, color='#2c3e50'))
    ax.add_patch(patches.Rectangle((30, 18), 40, 5, color='#c0392b'))

    # CARGA SEGÚN GMPH
    progreso = min(1, (frame / 60) * (gmph / 45.85))

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

        # contenedor en grúa
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
        ax.text(x, y, "CO2", ha='center', fontsize=9)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 70)
    ax.axis('off')

    st.pyplot(fig)

# ------------------------
# KPI
# ------------------------

st.subheader("📊 Indicadores KPI")

col1, col2, col3 = st.columns(3)

col1.metric("GMPH", gmph)
col2.metric("Energía (GWh/año)", energia)
col3.metric("CO2 (ton/año)", co2)

# ------------------------
# IA EXPLICACIÓN
# ------------------------

if opcion == "Optimizado IA":

    st.subheader("🧠 Optimización mediante Inteligencia Artificial")

    st.markdown("""
La solución propuesta por la Inteligencia Artificial se basa en el análisis de los tres benchmarks desarrollados en este estudio: productivo, energético y ambiental.

El benchmark productivo demuestra que es posible aumentar significativamente la eficiencia operativa (45,85 GMPH), pero con un aumento del 31% en consumo energético y emisiones.

El benchmark energético reduce el consumo en un 16,9% (28,16 GWh) y las emisiones, aunque sin mejorar la productividad.

El benchmark ambiental reduce un 9,2% las emisiones sin afectar al rendimiento operativo.

Ante estos resultados, la IA propone un escenario híbrido:

• Productividad optimizada (40 GMPH)  
• Consumo energético reducido (30 GWh)  
• Emisiones minimizadas (9.500 t CO2)  

Este equilibrio evita los trade-offs extremos y maximiza la eficiencia global de la terminal.
""")

# ------------------------
# ACTUALIZAR FRAME (SIN BUG)
# ------------------------

st.session_state.frame += 1
time.sleep(0.05)




















