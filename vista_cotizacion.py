from datetime import datetime

import streamlit as st


def renderizar_cotizacion(codigo_cotizacion):
  """Renderiza la Pestaña 1: datos de cabecera y productos de la cotización."""
  if "lista_productos" not in st.session_state:
    st.session_state["lista_productos"] = []

  st.subheader("Datos de la Cotización")
  with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
      st.session_state["nro_cotizacion"] = st.text_input(
          "Número de Cotización", codigo_cotizacion, disabled=True
      )
      fecha_usuario = st.date_input(
          "Selecciona la Fecha de Emisión", value=datetime.today()
      )
      meses = [
          "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
          "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
      ]
      st.session_state["fecha"] = (
          f"Lima, {fecha_usuario.day} de {meses[fecha_usuario.month - 1]} de"
          f" {fecha_usuario.year}"
      )
      st.session_state["cliente"] = st.text_input(
          "Cliente / Empresa", "MAKSER PERU S.A.C."
      )
    with col2:
      st.session_state["contacto"] = st.text_input(
          "Contacto / Atención", "Ing. ANTHONY JESUS"
      )
      st.session_state["atentamente"] = st.text_input(
          "Emitido por (Atte.)", "ING. ELIO CORONEL GABRIEL"
      )

  st.markdown("### 🧾 Agregar Productos a la Cotización")
  with st.form("form_agregar_producto", clear_on_submit=True, border=True):
    col_p1, col_p2, col_p3, col_p4 = st.columns([1, 1, 3, 1.2])
    with col_p1:
      cant_num = st.number_input("Cantidad", min_value=1, value=1, step=1)
    with col_p2:
      unid = st.text_input("Unidad", "pza")
    with col_p3:
      descripcion = st.text_input("Descripción", "")
    with col_p4:
      p_unit_num = st.number_input(
          "P. Unitario ($)", min_value=0.0, value=0.0, step=0.01, format="%.2f"
      )

    agregar = st.form_submit_button(
        "➕ Agregar producto", use_container_width=True
    )

    if agregar:
      if descripcion.strip() == "":
        st.warning("Escribe una descripción antes de agregar el producto.")
      else:
        p_total_item = cant_num * p_unit_num
        st.session_state["lista_productos"].append({
            "cant": str(cant_num),
            "unid": unid,
            "descripcion": descripcion,
            "p_unit": f"{p_unit_num:.2f}",
            "p_total": f"{p_total_item:.2f}",
        })
        st.rerun()

  total_general = 0.0
  if st.session_state["lista_productos"]:
    st.write("**Productos agregados:**")
    for i, prod in enumerate(st.session_state["lista_productos"]):
      col_a, col_b, col_c, col_d, col_e, col_f = st.columns(
          [0.6, 0.8, 3, 1, 1, 0.6]
      )
      col_a.write(prod["cant"])
      col_b.write(prod["unid"])
      col_c.write(prod["descripcion"])
      col_d.write(f'$ {prod["p_unit"]}')
      col_e.write(f'$ {prod["p_total"]}')
      if col_f.button("🗑️", key=f"del_{i}"):
        st.session_state["lista_productos"].pop(i)
        st.rerun()
    total_general = sum(
        float(p["p_total"]) for p in st.session_state["lista_productos"]
    )
    st.markdown(f"### 💰 Total: $ {total_general:,.2f}")

  st.session_state["p_total_general"] = f"{total_general:.2f}"