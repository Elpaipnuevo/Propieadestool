
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Propiedades", layout="wide")

st.markdown("## 🔍 Buscador de Propiedades - Portafolio Diversificado")

archivo_path = "Ficha_Propiedad_Limpia v.xlsx"

@st.cache_data
def cargar_datos():
    return pd.read_excel(archivo_path)

def mostrar_resultados(df):
    st.markdown(f"### Resultados: {len(df)} propiedades encontradas")
    for _, fila in df.iterrows():
        with st.container():
            st.markdown("---")
            st.markdown(f"#### 📍 {fila['Dirección completa']}")
            st.markdown(f"- **Zona / Vecindario:** {fila['Zona / Vecindario']}")
            st.markdown(f"- **Tipo de propiedad:** {fila['Tipo de propiedad']}")
            st.markdown(f"- **Año de construcción:** {fila['Año de construcción']}")
            st.markdown(f"- **Metros cuadrados / pies cuadrados:** {fila['Metros cuadrados / pies cuadrados']}")
            st.markdown(f"- **Estado general del inmueble:** {fila['Estado general del inmueble']}")
            st.markdown(f"- **Tiempo en el mercado (Days on Zillow):** {fila['Tiempo en el mercado (Days on Zillow)']}")
            st.markdown(f"- **ZIP Code:** {fila['ZIP Code']}")

try:
    df = cargar_datos()
    mostrar_resultados(df)
except Exception as e:
    st.error(f"Error al leer el archivo: {e}")
