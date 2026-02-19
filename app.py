import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

# ------------------------
# CONFIG
# ------------------------
st.set_page_config(layout="wide")

# ------------------------
# ESTADO INICIAL
# ------------------------
if "frame" not in st.session_state:
    st.session_state.frame = 0

if "escenario" not in st.session_state:
    st.session_state.escenario = "Baseline"

if "ia_activa" not in st.session_state:
    st.session_state.ia_activa = False

# ------------------------
# LOGO
# ------------------------
import os

col1, col2 = st.columns([6,1])

with col2:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120)
    else:
        st.write("")  # no rompe la app si no existe

# ------------------------
# TITULO
# ------------------------
st.title("Gemelo Digital - Terminal APM Barcelona")

# ------------------------
# SELECTOR
# ------------------------
escenario = st.radio(
    "Selecciona escenario:",
    ["Baseline", "Productivo", "Energético", "Ambiental"]
)

st.session_state.escenario = escenario

# ------------------------
# BOTON IA
# ------------------------
if st.button("Optimizar con IA"):
    st.session_state.ia_activa = True

# ------------------------
# PARAMETROS
# ------------------------
params = {
    "Baseline": (30, 35, 12000),
    "Productivo": (46, 46, 15700),
    "Energético": (30, 28, 9300),
    "Ambiental": (30, 35, 10172),
    "IA": (40, 30, 9500)
}

# Selección final
if st.session_state.ia_activa:
    gmph, energia, co2 = params["IA"]
    escenario_final = "Optimizado IA"
else:
    gmph, energia, co2 = params[escenario]
    escenario_final = escenario

# ------------------------
# ANIMACION
# ------------------------
fig, ax = plt.subplots(figsize=(12,5))

# Puerto base
ax.add_patch(plt.Rectangle((0,0), 100, 50))  # agua
ax.add_patch(plt.Rectangle((0,50), 100, 50)) # tierra

# Buque
container_progress = (st.session_state.frame * gmph * 0.1) % 100

ax.add_patch(plt.Rectangle((10,20), 30,10))  # barco

# Contenedores en barco
for i in range(int(container_progress/5)):
    ax.add_patch(plt.Rectangle((10+i, 30), 1, 2))

# Grúas
for x in [20,40,60,80]:
    ax.add_patch(plt.Rectangle((x,60), 2,15))
    ax.add_patch(plt.Rectangle((x,75), 10,2))
    
    # contenedor moviéndose (verde)
    y_move = 60 + abs(np.sin(st.session_state.frame/5))*15
    ax.add_patch(plt.Rectangle((x+4, y_move), 2,2))

ax.set_xlim(0,100)
ax.set_ylim(0,100)
ax.axis('off')

st.pyplot(fig)

# ------------------------
# KPIs
# ------------------------
st.subheader("KPIs del escenario")

col1, col2, col3 = st.columns(3)
col1.metric("GMPH", gmph)
col2.metric("Energía (GWh)", energia)
col3.metric("CO2 (t)", co2)

# ------------------------
# IA EXPLICACION
# ------------------------
if st.session_state.ia_activa:

    st.subheader("Optimización mediante Inteligencia Artificial")

    st.markdown("""
La solución propuesta por la Inteligencia Artificial se basa en el análisis de los tres benchmarks desarrollados en este estudio: productivo, energético y ambiental.

En primer lugar, el benchmark productivo demuestra que es posible aumentar significativamente la eficiencia operativa de la terminal, alcanzando 45,85 GMPH y reduciendo el tiempo de estancia de los buques en un 25,2%. Sin embargo, esta mejora implica un incremento del 31% tanto en el consumo energético como en las emisiones de CO2, lo que lo convierte en un escenario poco sostenible.

Por otro lado, el benchmark energético reduce el consumo en un 16,9% (de 33,90 GWh a 28,16 GWh), lo que conlleva una disminución proporcional de emisiones hasta 9.310 toneladas de CO2. No obstante, este escenario no mejora la productividad operativa.

Finalmente, el benchmark ambiental consigue reducir las emisiones en un 9,2% (hasta 10.172 toneladas de CO2) sin afectar a la productividad ni al consumo energético, mediante estrategias de descarbonización y tecnologías limpias.

Ante estos resultados, la IA propone un escenario híbrido que equilibra los tres enfoques:

• Mantiene una productividad eficiente para evitar congestión portuaria  
• Reduce el consumo energético respecto al escenario productivo  
• Minimiza las emisiones de CO2 sin comprometer la operativa  

Este enfoque permite maximizar la eficiencia global de la terminal APM de Barcelona, evitando los trade-offs extremos observados en los benchmarks individuales.
""")

# ------------------------
# LOOP DE ANIMACION
# ------------------------
st.session_state.frame += 1
time.sleep(0.05)
st.rerun()



















