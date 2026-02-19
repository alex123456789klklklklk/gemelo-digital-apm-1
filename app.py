import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import time


st.set_page_config(layout="wide")


# ------------------------
# HEADER CON LOGO
# ------------------------

col1, col2 = st.columns([6,1])

with col1:
    st.title("Gemelo Digital - Terminal APM Barcelona")

with col2:
    st.image("apm_logo.png", width=120)


# ------------------------
# ESTADO
# ------------------------

if "frame" not in st.session_state:
   st.session_state.frame = 0

if "escenario" not in st.session_state:
   st.session_state.escenario = "Baseline"


# ------------------------
# SELECTOR
# ------------------------

opcion = st.radio(
   "Selecciona escenario:",
   ["Baseline", "Productivo", "Energético", "Ambiental", "Optimizado IA"]
)

st.session_state.escenario = opcion


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
# REPRESENTACIÓN
# ------------------------

frame = st.session_state.frame

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
# EXPLICACIÓN IA
# ------------------------

if opcion == "Optimizado IA":

   st.subheader("🧠 Explicación del modelo de optimización")

   st.markdown("""
La solución propuesta por la Inteligencia Artificial se basa en el análisis de los tres benchmarks desarrollados en este estudio: productivo, energético y ambiental.

En primer lugar, el benchmark productivo demuestra que es posible aumentar significativamente la eficiencia operativa de la terminal, alcanzando 45,85 GMPH y reduciendo el tiempo de estancia de los buques en un 25,2%. Sin embargo, esta mejora implica un incremento del 31% tanto en el consumo energético como en las emisiones de CO2, lo que lo convierte en un escenario poco sostenible.

Por otro lado, el benchmark energético reduce el consumo en un 16,9%, lo que conlleva una disminución proporcional de emisiones. No obstante, este escenario no mejora la productividad operativa.

Finalmente, el benchmark ambiental consigue reducir las emisiones sin afectar a la productividad ni al consumo energético.

Ante estos resultados, la IA propone un escenario híbrido que equilibra los tres enfoques:

• Productividad eficiente (40 GMPH)  
• Menor consumo energético (30 GWh)  
• Reducción de emisiones (9.500 t CO2)  

Este enfoque maximiza la eficiencia global de la terminal, evitando trade-offs extremos.
""")


# ------------------------
# ANIMACIÓN
# ------------------------

st.session_state.frame += 1
time.sleep(0.05)
st.rerun()




















