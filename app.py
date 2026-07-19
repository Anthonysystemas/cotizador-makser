import streamlit as st
import typst
from datetime import datetime

# 1. Configuración del título de la pestaña web
st.set_page_config(page_title="Makser Perú - Cotizaciones", page_icon="📋", layout="wide")

# 2. Logotipo de la Empresa en la Cabecera
try:
    st.image("logo_makser.png", width=250)
except Exception:
    st.caption("💡 *Nota: Coloca un archivo llamado 'logo_makser.png' en tu repositorio para mostrar el logo aquí.*")

st.title("🚀 Sistema de Cotizaciones - Makser Perú S.A.C.")
st.write("Llena los campos de las columnas. Al finalizar, presiona el botón para compilar.")

st.markdown(" ")

# Contenedor visual con borde
with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        nro_cotizacion = st.text_input("Número de Cotización", "300/26")
        
        # Calendario Interactivo para la Fecha
        fecha_usuario = st.date_input("Selecciona la Fecha de Emisión", value=datetime.today())
        
        # Diccionario de meses en español para armar el formato exacto de texto
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        fecha = f"Lima, {fecha_usuario.day} de {meses[fecha_usuario.month - 1]} de {fecha_usuario.year}"
        
        st.caption(f"📅 Formato enviado: *{fecha}*")
        
        cliente = st.text_input("Cliente / Empresa", "MASKEL PERU S.A.C.")
        contacto = st.text_input("Contacto / Atención", "Ing. ANTHONY JESUS")

    with col2:
        # Cálculos Automáticos en Tiempo Real
        cant_num = st.number_input("Cantidad", min_value=1, value=5, step=1)
        unid = st.text_input("Unidad de Medida", "pza")
        p_unit_num = st.number_input("Precio Unitario ($)", min_value=0.0, value=600.00, step=0.01, format="%.2f")
        
        # El total se calcula multiplicando en tiempo real
        total_calculado = cant_num * p_unit_num
        
        # Convertimos a texto manteniendo tus mismos formatos para Typst
        cant = str(cant_num)
        p_unit = f"{p_unit_num:.2f}"
        p_total = f"{total_calculado:.2f}"
        
        # Caja de texto informativa del total calculado (bloqueada para edición manual)
        st.text_input("Precio Total ($) [Calculado Automáticamente]", p_total, disabled=True)
        
        # TOTALMENTE LIBRE: Volvemos a text_input para que escribas CUALQUIER nombre
        atentamente = st.text_input("Emitido por (Atte.)", "ING. ELIO CORONEL GABRIEL")

    # Caja de descripción original
    descripcion = st.text_area("Descripción detallada", "Grating frp de vidrio 1 X 4", height=100)

st.markdown("---")

# 3. Tu diccionario original intacto con las variables procesadas
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

# 4. Botón de acción
col_btn, _ = st.columns([1, 3])
with col_btn:
    btn_generar = st.button("⚡ Generar Cotización PDF", type="primary", use_container_width=True)

if btn_generar:
    try:
        with st.spinner("Compilando cotización con Typst..."):
            pdf_bytes = typst.compile("plantilla.typ", sys_inputs=datos_nuevos)
        
        st.success("¡PDF generado con éxito de manera interna!")
        
        st.download_button(
            label="📥 Descargar Archivo PDF",
            data=pdf_bytes,
            file_name=f"Cotizacion_{nro_cotizacion.replace('/', '-')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"Error al compilar el documento: {e}")