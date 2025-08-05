import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="Dashboard por Sucursal", layout="wide")
st.title("📊 Dashboard de KPIs por Sucursal")

uploaded_file = st.file_uploader("Sube el archivo Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    sucursales = [s for s in xls.sheet_names if not s.startswith("RM") and not s.startswith("TD")]

    sucursal = st.selectbox("Selecciona una sucursal", sucursales)

    df = pd.read_excel(uploaded_file, sheet_name=sucursal, header=None)
    kpis = {}

    i = 0
    while i < len(df):
        row = df.iloc[i]
        if isinstance(row[1], str) and row[1].startswith("KPI"):
            kpi_name = row[1].replace("KPI: ", "")
            headers = df.iloc[i + 1, 2:].tolist()
            months = df.iloc[i + 2:i + 14, 1].tolist()
            values = df.iloc[i + 2:i + 14, 2:i + 2 + len(headers)]
            values.columns = headers
            values.insert(0, "Mes", months)
            kpis[kpi_name] = values
            i += 14
        else:
            i += 1

    if kpis:
        for kpi, data in kpis.items():
            st.subheader(f"📈 {kpi}")
            years = list(data.columns[1:])
            selected_years = st.multiselect(f"Filtra años para {kpi}", years, default=years, key=kpi)

            fig, ax = plt.subplots()
            for year in selected_years:
                ax.plot(data["Mes"], data[year], label=year)
            ax.set_title(kpi)
            ax.set_xlabel("Mes")
            ax.set_ylabel("Valor")
            ax.legend()
            st.pyplot(fig)
    else:
        st.warning("No se encontraron KPIs en la hoja seleccionada.")

st.markdown("---")
st.caption("Creado con ❤️ y Streamlit | Más herramientas en https://gptonline.ai/")