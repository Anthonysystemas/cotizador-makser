import streamlit as st

import database as db
from vista_cotizacion import renderizar_cotizacion
from vista_ficha_tecnica import renderizar_ficha_tecnica
from vista_condiciones import renderizar_condiciones


def renderizar_interfaz():
  if "pdf_listo" not in st.session_state:
    st.session_state["pdf_listo"] = None
  if "archivo_nombre" not in st.session_state:
    st.session_state["archivo_nombre"] = ""
  if "mostrar_alerta_exito" not in st.session_state:
    st.session_state["mostrar_alerta_exito"] = False

  st.set_page_config(
      page_title="Makser Perú - Sistema Integrado", page_icon="📋", layout="wide"
  )
  st.title("🚀 Sistema Integrado de Cotizaciones y Fichas Técnicas")

  try:
    codigo_cotizacion, num_actual, anio_actual = db.obtener_siguiente_codigo()
  except Exception as e:
    st.error(f"Error al obtener correlativo: {e}")
    codigo_cotizacion, num_actual, anio_actual = "000/00", 0, 0

  tab_cotizacion, tab_ficha, tab_condiciones = st.tabs([
      "1. 📄 Cotización",
      "2. 📋 Ficha Técnica",
      "3. 📜 Condiciones Generales y Generación",
  ])

  with tab_cotizacion:
    renderizar_cotizacion(codigo_cotizacion)

  with tab_ficha:
    renderizar_ficha_tecnica()

  with tab_condiciones:
    renderizar_condiciones(codigo_cotizacion, num_actual)

  if st.session_state["pdf_listo"] is not None:
    st.markdown("---")
    if st.session_state["mostrar_alerta_exito"]:
      st.success(
          "¡Documento completo (Cotización + Ficha Técnica + Condiciones)"
          " guardado y generado con éxito! El formulario ya se limpió para"
          " una nueva cotización."
      )
      st.session_state["mostrar_alerta_exito"] = False

    st.download_button(
        label="📥 Descargar Documento Final PDF",
        data=st.session_state["pdf_listo"],
        file_name=st.session_state["archivo_nombre"],
        mime="application/pdf",
        use_container_width=True,
    )


if __name__ == "__main__":
  renderizar_interfaz()