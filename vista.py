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

    with col2:
        cant_num = st.number_input("Cantidad", min_value=1, value=5, step=1)
        unid = st.text_input("Unidad de Medida", "pza")
        p_unit_num = st.number_input("Precio Unitario ($)", min_value=0.0, value=600.00, step=0.01, format="%.2f")
        
        total_calculado = cant_num * p_unit_num
        cant = str(cant_num)
        p_unit = f"{p_unit_num:.2f}"
        p_total = f"{total_calculado:.2f}"
        
        st.text_input("Precio Total ($) [Calculado Automáticamente]", p_total, disabled=True)

    descripcion = st.text_area("Descripción detallada", "Grating frp de vidrio 1 X 4", height=100)
    st.markdown("---")

    datos_nuevos = {
        "nro_cotizacion": nro_cotizacion,
        "fecha": fecha,
        "cliente": cliente,
        "contacto": contacto,
        "cant": cant,
        "unid": unid,
        "descripcion": descripcion,
        "p_unit": p_unit,
        "p_total": p_total,
        "atentamente": atentamente, 
    }

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        btn_generar = st.button("⚡ Generar Cotización PDF", type="primary", use_container_width=True)

    if btn_generar:
        # Apagamos la alerta previa antes de intentar compilar el nuevo
        st.session_state["mostrar_alerta_exito"] = False
        try:
            with st.spinner("Procesando cotización..."):
                pdf_bytes = svc.generar_documento_cotizacion(datos_nuevos, num_actual)
            
            st.session_state["pdf_listo"] = pdf_bytes
            st.session_state["archivo_nombre"] = f"Cotizacion_{nro_cotizacion.replace('/', '-')}.pdf"
            # Activamos la alerta
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