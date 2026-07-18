import streamlit as st
import typst

# 1. Configuración del título de la pestaña web
st.set_page_config(page_title="Makser Perú - Cotizaciones", page_icon="📋")

st.title("🚀 Sistema de Cotizaciones - Makser Perú S.A.C.")
st.write("Llena los campos de la izquierda y derecha. Al finalizar, presiona el botón para compilar.")

# 2. Creamos dos columnas visuales en la pantalla para que se vea ordenado
col1, col2 = st.columns(2)

with col1:
    # st.text_input crea una caja de texto. El segundo parámetro es el valor por defecto.
    nro_cotizacion = st.text_input("Número de Cotización", "300/26")
    fecha = st.text_input("Fecha de Emisión", "Lima, 18 de Julio de 2026")
    cliente = st.text_input("Cliente / Empresa", "MASKEL PERU S.A.C.")
    contacto = st.text_input("Contacto / Atención", "Ing. ANTHONY JESUS")

with col2:
    cant = st.text_input("Cantidad", "5")
    unid = st.text_input("Unidad de Medida", "pza")
    p_unit = st.text_input("Precio Unitario ($)", "600.00")
    p_total = st.text_input("Precio Total ($)", "3000.00")
    atentamente = st.text_input("Emitido por (Atte.)", "Ing. BRANDON JESUS")

# Una caja de texto más grande para la descripción del producto
descripcion = st.text_area("Descripción detallada", "Grating frp de vidrio 1 X 4")

st.markdown("---")

# 3. Empaquetamos todo en el diccionario que tu plantilla Typst ya conoce
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
if st.button("⚡ Generar Cotización PDF", type="primary"):
    try:
        with st.spinner("Compilando cotización con Typst..."):
            # Esto compila el PDF directamente en la memoria del servidor usando sys_inputs
            pdf_bytes = typst.compile("plantilla.typ", sys_inputs=datos_nuevos)
        
        st.success("¡PDF generado con éxito de manera interna!")
        
        # Le muestra un botón al usuario para descargar el archivo a su PC
        st.download_button(
            label="📥 Descargar Archivo PDF",
            data=pdf_bytes,
            file_name=f"Cotizacion_{nro_cotizacion.replace('/', '-')}.pdf",
            mime="application/pdf"
        )
    except Exception as e:
        st.error(f"Error al compilar el documento: {e}")