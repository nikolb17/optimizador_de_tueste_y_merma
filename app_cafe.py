import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Sabor Nacional Optimizer", layout="wide")

# --- DISEÑO MULTIMEDIA AVANZADO (CSS) ---
st.markdown("""
    <style>
    /* Fondo de granos de café con movimiento suave */
    .stApp {
        background: linear-gradient(rgba(253, 250, 245, 0.92), rgba(253, 250, 245, 0.92)),
                    url('https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?q=80&w=2000');
        background-attachment: fixed;
        background-size: cover;
    }

    /* Contenedor del Logo */
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 20px;
    }
    .logo-img {
        width: 350px;
        transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .logo-img:hover {
        transform: rotate(-2deg) scale(1.1);
    }

    /* Galería de imágenes de tueste con movimiento */
    .hero-gallery {
        display: flex;
        gap: 20px;
        overflow: hidden;
        padding: 30px 0;
        justify-content: center;
    }
    .hero-img {
        width: 280px;
        height: 180px;
        object-fit: cover;
        border-radius: 20px;
        box-shadow: 0 12px 20px rgba(0,0,0,0.15);
        animation: slide 8s infinite alternate ease-in-out;
    }
    @keyframes slide {
        from { transform: translateY(10px); }
        to { transform: translateY(-10px); }
    }

    /* Botones Gigantes e Interactivos */
    div.stButton > button {
        background: linear-gradient(45deg, #4b2c20, #8b5a2b) !important;
        color: white !important;
        border-radius: 50px !important;
        height: 4.5em !important;
        font-size: 1.3rem !important;
        font-weight: bold !important;
        letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        border: none !important;
        box-shadow: 0px 8px 15px rgba(75, 44, 32, 0.3) !important;
    }
    div.stButton > button:hover {
        transform: scale(1.12) !important;
        box-shadow: 0px 15px 30px rgba(75, 44, 32, 0.5) !important;
        background: linear-gradient(45deg, #6f4e37, #a67c52) !important;
    }

    /* Estilo de los contenedores de entrada */
    .stTextInput input, .stNumberInput input {
        border-radius: 12px !important;
        border: 2px solid #e0d5c1 !important;
        padding: 10px !important;
    }
    
    h1, h2, h3 {
        color: #4b2c20 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER: LOGO INCORPORADO ---
# Usamos el enlace RAW para que GitHub permita la visualización directa
logo_url = "https://raw.githubusercontent.com/nikolb17/optimizador_de_tueste_y_merma/37e620726061dd64a35fc51a4d53253a712fb8a6/logo%20vectorizado%20sabor%20nacional.png"

st.markdown(f"""
    <div class="logo-container">
        <img src="{logo_url}" class="logo-img" alt="Sabor Nacional Logo">
    </div>
    """, unsafe_allow_html=True)

# Galería animada (Contexto Multimedia)
st.markdown("""
    <div class="hero-gallery">
        <img src="https://images.unsplash.com/photo-1511537190424-bbbab87ac5eb?q=80&w=500" class="hero-img">
        <img src="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=500" class="hero-img">
        <img src="https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=500" class="hero-img">
    </div>
    """, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>REGISTRO TÉCNICO DE CAFÉ ESPECIAL</h2>", unsafe_allow_html=True)

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

# --- FORMULARIO DE REGISTRO ---
_, col_form, _ = st.columns([1, 2, 1])

with col_form:
    st.markdown("<div style='background: white; padding: 40px; border-radius: 25px; box-shadow: 0 15px 40px rgba(0,0,0,0.08);'>", unsafe_allow_html=True)
    
    nombre_lote = st.text_input("💎 Nombre del Lote / Variedad", placeholder="Ej: Santa Marta Geisha")
    
    c1, c2 = st.columns(2)
    pv_input = c1.number_input("Entrada Verde (kg)", value=10.0, step=0.1)
    pt_input = c2.number_input("Salida Tostado (kg)", value=8.5, step=0.1)
    
    c3, c4 = st.columns(2)
    fc_input = c3.text_input("⏱️ Tiempo First Crack (M:S)", value="13:50")
    saque_input = c4.text_input("⏱️ Tiempo Saque (M:S)", value="15:30")
    
    if st.button("PROCESAR Y GUARDAR LOTE"):
        m, d = calcular_metricas(pv_input, pt_input, saque_input, fc_input)
        if m is not None:
            st.balloons()
            st.success(f"¡Lote '{nombre_lote}' procesado con éxito!")
            
            m1, m2 = st.columns(2)
            m1.metric("MERMA FINAL", f"{m:.2f}%", delta=f"{m-15:.1f}%")
            m2.metric("DESARROLLO (DTR)", f"{d:.2f}%", delta=f"{d-20:.1f}%")
            
            # Persistencia de datos
            archivo = 'historial_tuestes_sabor_nacional.csv'
            nuevo_registro = {
                'Fecha': datetime.now().strftime("%Y-%m-%d"),
                'Lote': nombre_lote,
                'Merma': round(m, 2),
                'DTR': round(d, 2)
            }
            df_nuevo = pd.DataFrame([nuevo_registro])
            df_nuevo.to_csv(archivo, mode='a', header=not os.path.exists(archivo), index=False)
        else:
            st.error("Error: Verifica que los tiempos tengan el formato Minutos:Segundos")
    st.markdown("</div>", unsafe_allow_html=True)

# --- VISUALIZACIÓN DE TENDENCIAS ---
st.write("---")
if os.path.exists('historial_tuestes_sabor_nacional.csv'):
    st.subheader("📈 Consistencia Histórica")
    df_h = pd.read_csv('historial_tuestes_sabor_nacional.csv')
    
    fig = px.area(df_h, x='Lote', y=['Merma', 'DTR'], 
                  title="Evolución de Perfiles - Sabor Nacional",
                  color_discrete_sequence=['#4b2c20', '#a67c52'],
                  markers=True)
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#4b2c20")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("El historial aparecerá aquí cuando registres tu primer lote.")