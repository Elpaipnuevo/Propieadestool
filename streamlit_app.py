
import streamlit as st
import pandas as pd

# Configurar página
st.set_page_config(page_title="Buscador de Propiedades", layout="wide")
st.title("🔍 Buscador de Propiedades - Portafolio Diversificado")

# Cargar el archivo Excel automáticamente desde el archivo incluido en el repo
@st.cache_data
def cargar_datos():
    return pd.read_excel("Ficha_Propiedad_Limpia v.xlsx", engine="openpyxl")

try:
    df = cargar_datos()

    # Filtros en la barra lateral
    st.sidebar.header("🔽 Filtros")

    zonas = ["Todas"] + sorted(df["Zona / Vecindario"].dropna().unique().tolist())
    tipos = ["Todos"] + sorted(df["Tipo de propiedad"].dropna().unique().tolist())
    habitaciones = ["Todas"] + sorted(df["Número de habitaciones"].dropna().astype(str).unique().tolist())

    zona_sel = st.sidebar.selectbox("Zona / Vecindario", zonas)
    tipo_sel = st.sidebar.selectbox("Tipo de propiedad", tipos)
    hab_sel = st.sidebar.selectbox("Número de habitaciones", habitaciones)
    precio_max = st.sidebar.number_input("Precio máximo de renta mensual ($)", min_value=0, value=2000)

    # Filtrar los datos
    df_filtrado = df.copy()

    if zona_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Zona / Vecindario"] == zona_sel]

    if tipo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo de propiedad"] == tipo_sel]

    if hab_sel != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Número de habitaciones"].astype(str) == hab_sel]

    df_filtrado = df_filtrado[df_filtrado["Precio de renta mensual ($)"] <= precio_max]

    st.subheader(f"Resultados: {len(df_filtrado)} propiedades encontradas")

    # Mostrar propiedades como tarjetas
    for i, row in df_filtrado.iterrows():
        with st.container():
            st.markdown("---")
            st.markdown(f"📍 **{row['Dirección completa']}**")
            st.markdown(f"""
            - **Zona / Vecindario:** {row['Zona / Vecindario']}
            - **Tipo de propiedad:** {row['Tipo de propiedad']}
            - **Año de construcción:** {row['Año de construcción']}
            - **Metros cuadrados / pies cuadrados:** {row['Metros cuadrados / pies cuadrados']}
            - **Estado general del inmueble:** {row['Estado general del inmueble']}
            - **Tiempo en el mercado (Days on Zillow):** {row['Tiempo en el mercado (Days on Zillow)']}
            - **ZIP Code:** {row['ZIP Code']}
            """)
except Exception as e:
    st.error(f"Error al cargar los datos: {e}")
