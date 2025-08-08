import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Predicción de Delitos", layout="centered")

# --- CSS RESPONSIVO AL TEMA DEL SISTEMA ---
st.markdown("""
    <style>
    /* Modo Claro */
    @media (prefers-color-scheme: light) {
        html, body, .main {
            background-color: #fff6e5;
            color: #000000;
            font-family: 'Segoe UI', sans-serif;
        }
        .titulo { color: #000000; }
        .sub { color: #00569e; }
        .dato { color: #f3c623; }
    }

    /* Modo Oscuro */
    @media (prefers-color-scheme: dark) {
        html, body, .main {
            background-color: #121212;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        .titulo { color: #f3c623; }
        .sub { color: #7ed957; }
        .dato { color: #38b6ff; }
    }

    header, footer {visibility: hidden;}
    .titulo {
        font-size: 36px;
        font-weight: bold;
    }
    .sub {
        font-size: 20px;
        font-weight: bold;
        margin-top: 1rem;
    }
    .dato {
        font-size: 24px;
        font-weight: bold;
    }
    .center { text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- CARGAR DATOS ---
df_pred = pd.read_csv("predicciones_patrimonio.csv")
df_hist = pd.read_csv("historico_patrimonio.csv")

# --- TÍTULO ---
st.markdown("<div class='titulo center'>🔎 Predicción de denuncias por <span style='color:#f3c623'>Delito Contra el Patrimonio</span></div>", unsafe_allow_html=True)
st.markdown("---")

# --- SELECTOR ---
departamento = st.selectbox("📍 Selecciona un departamento:", sorted(df_pred["departamento"].unique()))

# --- FILTRAR ---
df_hist_dpto = df_hist[df_hist["departamento"] == departamento]
df_pred_dpto = df_pred[df_pred["departamento"] == departamento]

# --- MOSTRAR PREDICCIONES ---
st.markdown(f"<div class='sub'>📈 Predicciones para {departamento}</div>", unsafe_allow_html=True)

if not df_pred_dpto.empty:
    col1, col2 = st.columns(2)
    col1.markdown(f"<div class='dato'>🔮 2024: {int(df_pred_dpto['2024'])}</div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='dato'>🔮 2025: {int(df_pred_dpto['2025'])}</div>", unsafe_allow_html=True)
else:
    st.warning("No hay predicciones disponibles para este departamento.")

# --- GRAFICO ---
if not df_hist_dpto.empty and not df_pred_dpto.empty:
    df_viz = df_hist_dpto.rename(columns={"anio": "Año", "cantidad": "Denuncias"})
    pred_df = pd.DataFrame({
        "Año": [2024, 2025],
        "Denuncias": [int(df_pred_dpto["2024"]), int(df_pred_dpto["2025"])]
    })
    df_viz = pd.concat([df_viz[["Año", "Denuncias"]], pred_df], ignore_index=True)

    st.markdown("<div class='sub'>📊 Histórico + Predicción</div>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.lineplot(data=df_viz, x="Año", y="Denuncias", marker="o", linewidth=2.5, color="#00569e")
    ax.set_title(f"Denuncias por año - {departamento}", fontsize=14)
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("No hay datos históricos suficientes para mostrar el gráfico.")
