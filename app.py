import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CBA • Costo-Beneficio", layout="wide")
st.title("9️⃣ CBA • Costo-Beneficio")

def descarga_csv(df: pd.DataFrame, nombre: str):
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Descargar CSV", csv, file_name=f"{nombre}.csv", mime="text/csv")

st.header("9️⃣ Costo-Beneficio (CBA)")

st.caption("Beneficios ya expresados en términos monetarios.")
df0 = pd.DataFrame({
    "Alternativa": ["A", "B", "C"],
    "Costo (US$)": [10000.0, 15000.0, 22000.0],
    "Beneficio (US$)": [13000.0, 21000.0, 26000.0]
})
df = st.data_editor(df0, num_rows="dynamic", key="cba_tbl")

if not df.empty:
    if (df["Costo (US$)"] < 0).any() or (df["Beneficio (US$)"] < 0).any():
        st.error("Costos/beneficios no pueden ser negativos.")
    else:
        out = df.copy()
        out["Beneficio Neto (US$)"] = out["Beneficio (US$)"] - out["Costo (US$)"]
        out["B/C"] = out.apply(
            lambda r: (r["Beneficio (US$)"] / r["Costo (US$)"]) if r["Costo (US$)"] > 0 else np.nan,
            axis=1
        )
        out = out.sort_values("Beneficio Neto (US$)", ascending=False).reset_index(drop=True)

        st.subheader("Resultados CBA")
        st.dataframe(out, hide_index=True, use_container_width=True)

        mejor = out.iloc[0]
        st.success(
            f"Mejor alternativa (por Beneficio Neto): {mejor['Alternativa']} "
            f"— Beneficio Neto US$ {mejor['Beneficio Neto (US$)']:,.2f} — "
            f"B/C = {mejor['B/C']:.2f}"
        )

        fig, ax = plt.subplots()
        ax.bar(out["Alternativa"], out["Beneficio Neto (US$)"])
        ax.set_xlabel("Alternativa")
        ax.set_ylabel("Beneficio Neto (US$)")
        ax.set_title("Costo-Beneficio: Beneficio Neto por alternativa")
        st.pyplot(fig)

        descarga_csv(out, "CBA_resultados")
else:
    st.info("Agrega al menos una alternativa.")
