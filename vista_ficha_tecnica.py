import os
import time

import streamlit as st


def renderizar_ficha_tecnica():
  """Renderiza la Pestaña 2: cabecera de ficha técnica, imagen y características.
  No tiene botón de generación — eso vive en la Pestaña 3 (Condiciones Generales).
  El código de ficha es libre: puede repetirse sin problema.
  """
  st.subheader("1. Cabecera de Ficha Técnica")

  if "ft_codigo_ficha" not in st.session_state:
    st.session_state["ft_codigo_ficha"] = f"FT-2026-{str(int(time.time()))[-4:]}"

  with st.container(border=True):
    st.text_input("Código Ficha", key="ft_codigo_ficha")

    col_ft1, col_ft2 = st.columns(2)
    with col_ft1:
      st.text_input(
          "Título del Producto",
          value=st.session_state.get("ft_titulo_producto", "GRATING ELECTROSOLDADO 19W-4"),
          key="ft_titulo_producto",
      )
      st.text_input(
          "Norma de Fabricación",
          value=st.session_state.get("ft_norma", "FABRICACIÓN SEGÚN NORMA NAAMM MB 531"),
          key="ft_norma",
      )
    with col_ft2:
      st.text_input(
          "Etiqueta Material",
          value=st.session_state.get("ft_etiqueta_material", "Materiales Platinas y Barra:"),
          key="ft_etiqueta_material",
      )
      st.text_input(
          "Valor Material",
          value=st.session_state.get("ft_valor_material", "ASTM A36 DE ACEROS AREQUIPA."),
          key="ft_valor_material",
      )
      st.text_input(
          "Acabado",
          value=st.session_state.get("ft_acabado", "Con platinas dentadas y en negro natural."),
          key="ft_acabado",
      )

      imagen_subida = st.file_uploader(
          "Imagen del producto",
          type=["jpg", "jpeg", "png"],
          help="Si no subes una imagen, se usará la imagen por defecto.",
          key="ft_imagen_subida",
      )

      if imagen_subida is not None:
        os.makedirs("images/subidas", exist_ok=True)
        extension = imagen_subida.name.split(".")[-1].lower()
        codigo_ficha_actual = st.session_state["ft_codigo_ficha"]
        nombre_archivo = f"images/subidas/{codigo_ficha_actual}.{extension}"
        with open(nombre_archivo, "wb") as archivo_salida:
          archivo_salida.write(imagen_subida.getbuffer())
        st.session_state["ft_imagen_url"] = nombre_archivo
        st.image(imagen_subida, caption="Vista previa", width=150)
      elif "ft_imagen_url" not in st.session_state:
        st.session_state["ft_imagen_url"] = "images/GRATING.jpg"

  st.subheader("2. Características y Medidas del Producto")
  caracteristicas_defecto = [
      {"caracteristica": "Platina Portante (PP)", "medida": '3/16" x 1 1/2"'},
      {"caracteristica": "Separación entre platinas (SP)", "medida": "30mm"},
      {"caracteristica": "Barra cuadrilla torsional", "medida": '1/4"'},
      {"caracteristica": "Separación entre barras (SB)", "medida": "102mm"},
  ]

  st.number_input(
      "Número de características",
      min_value=1,
      max_value=15,
      value=st.session_state.get("ft_num_filas", len(caracteristicas_defecto)),
      key="ft_num_filas",
  )

  num_filas_ft = int(st.session_state["ft_num_filas"])

  for idx in range(num_filas_ft):
    c_caract, c_med = st.columns(2)
    def_caract = (
        caracteristicas_defecto[idx]["caracteristica"]
        if idx < len(caracteristicas_defecto)
        else ""
    )
    def_medida = (
        caracteristicas_defecto[idx]["medida"]
        if idx < len(caracteristicas_defecto)
        else ""
    )

    with c_caract:
      st.text_input(
          f"Característica #{idx+1}",
          value=st.session_state.get(f"ft_caract_{idx}", def_caract),
          key=f"ft_caract_{idx}",
      )
    with c_med:
      st.text_input(
          f"Medida / Valor #{idx+1}",
          value=st.session_state.get(f"ft_med_{idx}", def_medida),
          key=f"ft_med_{idx}",
      )