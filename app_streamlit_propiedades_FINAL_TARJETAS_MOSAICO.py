
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Buscador de Propiedades", layout="wide")

st.title("🔍 Buscador de Propiedades - Portafolio Diversificado")

# Subida del archivo
archivo_excel = st.file_uploader("Carga el archivo Excel de propiedades", type=["xlsx"])

if archivo_excel:
    df = pd.read_excel(archivo_excel)

    # Filtros
    st.sidebar.header("🎲 Filtros")
    zonas = [""] + sorted(df["Zona / Vecindario"].dropna().unique().tolist())
    tipos = [""] + sorted(df["Tipo de propiedad"].dropna().unique().tolist())
    habitaciones = [""] + sorted(df["Número de habitaciones"].dropna().unique().astype(str).tolist())

    zona_sel = st.sidebar.selectbox("Zona / Vecindario", zonas)
    tipo_sel = st.sidebar.selectbox("Tipo de propiedad", tipos)
    hab_sel = st.sidebar.selectbox("Número de habitaciones", habitaciones)
    precio_max = st.sidebar.number_input("Precio máximo de renta mensual ($)", min_value=0, value=2000)

    df_filtrado = df.copy()
    if zona_sel:
        df_filtrado = df_filtrado[df_filtrado["Zona / Vecindario"] == zona_sel]
    if tipo_sel:
        df_filtrado = df_filtrado[df_filtrado["Tipo de propiedad"] == tipo_sel]
    if hab_sel:
        df_filtrado = df_filtrado[df_filtrado["Número de habitaciones"].astype(str) == hab_sel]
    if "Precio de renta mensual ($)" in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado["Precio de renta mensual ($)"] <= precio_max]

    st.subheader(f"📋 Resultados: {len(df_filtrado)} propiedades encontradas")

    # Mostrar resultados en forma de tarjetas
    for i, row in df_filtrado.iterrows():
        with st.container():
            st.markdown("---")
            st.markdown(f"### 🏠 {row['Dirección completa']}")
            st.markdown(
                f"- **Zona / Vecindario:** {row['Zona / Vecindario']}\n"
                f"- **Tipo de propiedad:** {row['Tipo de propiedad']}\n"
                f"- **Tipo de zona:** {row['Tipo de zona']}\n"
                f"- **Piso (si aplica):** {row['Piso (si aplica)']}\n"
                f"- **Año de construcción:** {row['Año de construcción']}\n"
                f"- **Metros cuadrados / pies cuadrados:** {row['Metros cuadrados / pies cuadrados']}\n"
                f"- **Tiempo en el mercado (Days on Zillow):** {row['Tiempo en el mercado (Days on Zillow)']}\n"
                f"- **Estado general del inmueble:** {row['Estado general del inmueble']}\n"
                f"- **Número de habitaciones:** {row['Número de habitaciones']}\n"
                f"- **Precio de renta mensual ($):** {row.get('Precio de renta mensual ($)', 'N/A')}"
            )
