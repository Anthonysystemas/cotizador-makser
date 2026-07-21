# vista.py
from datetime import datetime
import streamlit as st

# Importamos nuestros módulos locales
import database as db
import pdf_service as svc

def renderizar_interfaz():
    # --- INICIALIZACIÓN DEL ESTADO ---
    if "pdf_listo" not in st.session_state:
        st.session_state["pdf_listo"] = None
    if "archivo_nombre" not in st.session_state:
        st.session_state["archivo_nombre"] = ""
    if "mostrar_alerta_exito" not in st.session_state:
        st.session_state["mostrar_alerta_exito"] = False    

    st.set_page_config(page_title="Makser Perú - Cotizaciones", page_icon="📋", layout="wide")
    st.title("🚀 Sistema de Cotizaciones - Makser Perú S.A.C.")
    st.write("Llena los campos de las columnas. Al finalizar, presiona el botón para compilar.")

    # Carga inicial delegada al modelo
    try:
        codigo_cotizacion, num_actual, anio_actual = db.obtener_siguiente_codigo()
    except Exception as e:
        st.error(str(e))
        codigo_cotizacion, num_actual, anio_actual = "000/00", 0, 0

    with st.container(border=True):
        col1, col2 = st.columns(2)

    with col1:
        nro_cotizacion = st.text_input("Número de Cotización", codigo_cotizacion, disabled=True)
        fecha_usuario = st.date_input("Selecciona la Fecha de Emisión", value=datetime.today())
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        fecha = f"Lima, {fecha_usuario.day} de {meses[fecha_usuario.month - 1]} de {fecha_usuario.year}"
        cliente = st.text_input("Cliente / Empresa", "MAKSER PERU S.A.C.")
        contacto = st.text_input("Contacto / Atención", "Ing. ANTHONY JESUS")
        atentamente = st.text_input("Emitido por (Atte.)", "ING. ELIO CORONEL GABRIEL")

    # --- ESTADO PARA LA LISTA DE PRODUCTOS ---
    if "lista_productos" not in st.session_state:
        st.session_state["lista_productos"] = []

    st.markdown("### 🧾 Agregar Productos")
    with st.form("form_agregar_producto", clear_on_submit=True, border=True):
        col_p1, col_p2, col_p3, col_p4 = st.columns([1, 1, 3, 1.2])
        with col_p1:
            cant_num = st.number_input("Cantidad", min_value=1, value=1, step=1)
        with col_p2:
            unid = st.text_input("Unidad", "pza")
        with col_p3:
            descripcion = st.text_input("Descripción", "")
        with col_p4:
            p_unit_num = st.number_input("P. Unitario ($)", min_value=0.0, value=0.0, step=0.01, format="%.2f")

        agregar = st.form_submit_button("➕ Agregar producto", use_container_width=True)

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
                    "p_total": f"{p_total_item:.2f}"
                })
                st.rerun()

    # --- TABLA DE PRODUCTOS AGREGADOS ---
    total_general = 0.0
    if st.session_state["lista_productos"]:
        st.write("**Productos agregados:**")
        for i, prod in enumerate(st.session_state["lista_productos"]):
            col_a, col_b, col_c, col_d, col_e, col_f = st.columns([0.6, 0.8, 3, 1, 1, 0.6])
            col_a.write(prod["cant"])
            col_b.write(prod["unid"])
            col_c.write(prod["descripcion"])
            col_d.write(f'$ {prod["p_unit"]}')
            col_e.write(f'$ {prod["p_total"]}')
            if col_f.button("🗑️", key=f"del_{i}"):
                st.session_state["lista_productos"].pop(i)
                st.rerun()
        total_general = sum(float(p["p_total"]) for p in st.session_state["lista_productos"])
        st.markdown(f"### 💰 Total: $ {total_general:,.2f}")

    st.markdown("---")

    datos_nuevos = {
        "nro_cotizacion": nro_cotizacion,
        "fecha": fecha,
        "cliente": cliente,
        "contacto": contacto,
        "atentamente": atentamente,
        "p_total_general": f"{total_general:.2f}",
        "productos": st.session_state["lista_productos"]
    }

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        btn_generar = st.button("⚡ Generar Cotización PDF", type="primary", use_container_width=True)

    if btn_generar:
        if not st.session_state["lista_productos"]:
            st.error("Agrega al menos un producto antes de generar la cotización.")
        else:
            st.session_state["mostrar_alerta_exito"] = False
            try:
                with st.spinner("Procesando cotización..."):
                    pdf_bytes = svc.generar_documento_cotizacion(datos_nuevos, num_actual)
                st.session_state["pdf_listo"] = pdf_bytes
                st.session_state["archivo_nombre"] = f"Cotizacion_{nro_cotizacion.replace('/', '-')}.pdf"
                st.session_state["mostrar_alerta_exito"] = True
                st.rerun()
            except Exception as e:
                st.error(f"Error en el proceso: {e}")
    # --- RENDERIZADO PERSISTENTE ---
    # Colocamos la alerta dentro del bloque de control del PDF para que salgan juntos
    if st.session_state["pdf_listo"] is not None:
        if st.session_state["mostrar_alerta_exito"]:
            st.success("¡PDF generado con éxito de manera interna!")

        st.markdown("### 📄 Tu documento está listo")
        st.download_button(
            label="📥 Descargar Archivo PDF",
            data=st.session_state["pdf_listo"],
            file_name=st.session_state["archivo_nombre"],
            mime="application/pdf",
            use_container_width=True
        )