import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import random

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sabor Nacional Optimizer", layout="wide")

# --- DISEÑO MULTIMEDIA Y ANIMACIONES (CSS) ---
st.markdown("""
    <style>
    /* Fondo con granos de café */
    .stApp {
        background: linear-gradient(rgba(253, 250, 245, 0.92), rgba(253, 250, 245, 0.92)),
                    url('https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=2000');
        background-attachment: fixed;
        background-size: cover;
    }

    /* Animación de granos de café cayendo */
    @keyframes fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }
    .bean {
        position: fixed;
        top: -5%;
        font-size: 2rem;
        user-select: none;
        z-index: 9999;
        animation: fall 3s linear forwards;
    }

    /* Logo interactivo */
    .logo-container { display: flex; justify-content: center; padding: 20px; }
    .logo-img { width: 350px; transition: transform 0.5s; }
    .logo-img:hover { transform: rotate(-2deg) scale(1.1); }

    /* Galería Hero */
    .hero-gallery { display: flex; gap: 20px; overflow: hidden; padding: 30px 0; justify-content: center; }
    .hero-img { width: 280px; height: 180px; object-fit: cover; border-radius: 20px; box-shadow: 0 12px 20px rgba(0,0,0,0.15); animation: slide 8s infinite alternate ease-in-out; }
    @keyframes slide { from { transform: translateY(10px); } to { transform: translateY(-10px); } }

    /* Botón Gigante */
    div.stButton > button {
        background: linear-gradient(45deg, #4b2c20, #8b5a2b) !important;
        color: white !important;
        border-radius: 50px !important;
        height: 4.5em !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(75, 44, 32, 0.3) !important;
    }
    div.stButton > button:hover {
        transform: scale(1.15) !important;
        background: linear-gradient(45deg, #6f4e37, #a67c52) !important;
    }

    /* Estilo de Tabla */
    .stDataFrame { background: white; border-radius: 15px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN PARA GRANOS CAYENDO ---
def animar_granos():
    # Creamos 20 "granos" (emojis de café) en posiciones aleatorias
    for i in range(25):
        left = random.randint(0, 100)
        delay = random.uniform(0, 2)
        st.markdown(f'<div class="bean" style="left:{left}%; animation-delay:{delay}s;">☕</div>', unsafe_allow_html=True)

# --- HEADER: LOGO ---
logo_url = "https://raw.githubusercontent.com/nikolb17/optimizador_de_tueste_y_merma/37e620726061dd64a35fc51a4d53253a712fb8a6/logo%20vectorizado%20sabor%20nacional.png"
st.markdown(f'<div class="logo-container"><img src="{logo_url}" class="logo-img"></div>', unsafe_allow_html=True)

# Galería Hero
st.markdown("""
    <div class="hero-gallery">
        <img src="https://images.unsplash.com/photo-1511537190424-bbbab87ac5eb?q=80&w=500" class="hero-img">
        <img src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=500" class="hero-img">
        <img src="https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=500" class="hero-img">
    </div>
    """, unsafe_allow_html=True)

# --- LÓGICA DE CÁLCULO ---
def calcular_metricas(pv, pt, tf, fc):
    try:
        m_f, s_f = map(int, tf.split(':'))
        m_c, s_c = map(int, fc.split(':'))
        sec_total = m_f * 60 + s_f
        sec_fc = m_c * 60 + s_c
        merma = ((pv - pt) / pv) * 100
        dtr = ((sec_total - sec_fc) / sec_total) * 100
        return merma, dtr
    except: return None, None

# --- FORMULARIO ---
_, col_form, _ = st.columns([1, 2, 1])

with col_form:
    st.markdown("<div style='background: white; padding: 40px; border-radius: 25px; box-shadow: 0 15px 40px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
    lote = st.text_input("💎 Nombre del Lote", placeholder="Ej: Santa Marta")
    c1, c2 = st.columns(2)
    peso_v = c1.number_input("Entrada Verde (kg)", value=10.0)
    peso_t = c2.number_input("Salida Tostado (kg)", value=8.5)
    c3, c4 = st.columns(2)
    t_fc = c3.text_input("⏱️ First Crack (M:S)", value="13:50")
    t_fin = c4.text_input("⏱️ Tiempo Saque (M:S)", value="15:30")
    
    if st.button("PROCESAR Y GUARDAR LOTE"):
        m, d = calcular_metricas(peso_v, peso_t, t_fin, t_fc)
        if m is not None:
            animar_granos() # <--- EFECTO DE GRANOS CAYENDO
            st.success(f"¡Lote '{lote}' registrado!")
            
            m1, m2 = st.columns(2)
            m1.metric("MERMA FINAL", f"{m:.2f}%")
            m2.metric("DESARROLLO (DTR)", f"{d:.2f}%")
            
            # Guardar
            archivo = 'historial_tuestes_sabor_nacional.csv'
            nuevo = {'Fecha': datetime.now().strftime("%Y-%m-%d"), 'Lote': lote, 'Merma': round(m, 2), 'DTR': round(d, 2)}
            pd.DataFrame([nuevo]).to_csv(archivo, mode='a', header=not os.path.exists(archivo), index=False)
        else:
            st.error("Formato de tiempo incorrecto.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- VISUALIZACIÓN ---
st.write("---")
archivo_csv = 'historial_tuestes_sabor_nacional.csv'

if os.path.exists(archivo_csv):
    df_h = pd.read_csv(archivo_csv)
    
    # Gráfica
    st.subheader("📈 Tendencias de Calidad")
    fig = px.line(df_h, x='Lote', y=['Merma', 'DTR'], markers=True, 
                  color_discrete_sequence=['#4b2c20', '#a67c52'])
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    # NUEVA TABLA AL FINAL
    st.write("---")
    st.subheader("📋 Base de Datos de Tueste")
    st.write("Aquí puedes ver todos tus registros históricos ordenados por fecha:")
    st.dataframe(df_h.sort_values(by='Fecha', ascending=False), use_container_width=True)
    
    # Botón para descargar el archivo por si lo necesitas en Excel
    csv = df_h.to_csv(index=False).encode('utf-8')
    st.download_button("Descargar historial para Excel", data=csv, file_name='historial_sabor_nacional.csv', mime='text/csv')
else:
    st.info("El historial aparecerá aquí al guardar tu primer tueste.")
