import os
from datetime import datetime
import streamlit as st
import typst
from supabase import create_client, Client

# =============================================================================
# CONEXIÓN Y LOGICA DE SUPABASE
# =============================================================================

# Credenciales de Supabase (Usa las variables de entorno, y si no existen, toma tus credenciales por defecto)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://qsndihdikzxleihyazlt.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_t0zRA7Neynf2lSATcw3QDA_EN2AZQaM")

# Inicializar el cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_siguiente_codigo():
    """Trae el número actual y año desde Supabase para armar el formato de la cotización."""
    try:
        # Consultamos la fila con id = 1
        respuesta = supabase.table("contador_cotizacion").select("numero, anio").eq("id", 1).execute()
        if respuesta.data:
            registro = respuesta.data[0]
            numero = registro["numero"]
            anio = registro["anio"]
            # Formato final: "300/26"
            return f"{numero}/{anio}", numero, anio
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")
    return "000/00", 0, 0

def incrementar_contador(numero_actual):
    """Incrementa de forma secuencial el número en la base de datos."""
    try:
        nuevo_numero = numero_actual + 1
        supabase.table("contador_cotizacion").update({"numero": nuevo_numero}).eq("id", 1).execute()
    except Exception as e:
        st.error(f"Error al actualizar el contador: {e}")
def guardar_datos_cotizacion(datos):
    """Inserta una nueva fila en la tabla 'cotizaciones' con los datos ingresados."""
    try:
        supabase.table("cotizaciones").insert({
            "nro_cotizacion": datos["nro_cotizacion"],
            "fecha": datos["fecha"],
            "cliente": datos["cliente"],
            "contacto": datos["contacto"],
            "atentamente": datos["atentamente"],
            "cantidad": int(datos["cant"]),
            "unidad": datos["unid"],
            "precio_unitario": float(datos["p_unit"]),
            "precio_total": float(datos["p_total"]),
            "descripcion": datos["descripcion"]
        }).execute()
    except Exception as e:
        st.error(f"Error al guardar los datos en Supabase: {e}")        

# =============================================================================
# CONFIGURACIÓN DE LA INTERFAZ STREAMLIT
# =============================================================================

# 1. Configuración del título de la pestaña web
st.set_page_config(page_title="Makser Perú - Cotizaciones", page_icon="📋", layout="wide")

st.title("🚀 Sistema de Cotizaciones - Makser Perú S.A.C.")
st.write("Llena los campos de las columnas. Al finalizar, presiona el botón para compilar.")

st.markdown(" ")

# Cargar el número de cotización actual desde la Base de Datos en tiempo real
codigo_cotizacion, num_actual, anio_actual = obtener_siguiente_codigo()

# Contenedor visual con borde
with st.container(border=True):
    col1, col2 = st.columns(2)

with col1:
    # Muestra el número recuperado de Supabase de forma dinámica
    nro_cotizacion = st.text_input("Número de Cotización", codigo_cotizacion, disabled=True)
    
    # Calendario Interactivo para la Fecha
    fecha_usuario = st.date_input("Selecciona la Fecha de Emisión", value=datetime.today())
    
    # Diccionario de meses en español
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    fecha = f"Lima, {fecha_usuario.day} de {meses[fecha_usuario.month - 1]} de {fecha_usuario.year}"
            
    # Campos de entrada para el cliente y contacto
    cliente = st.text_input("Cliente / Empresa", "MAKSER PERU S.A.C.")
    contacto = st.text_input("Contacto / Atención", "Ing. ANTHONY JESUS")
    
    # Emitido por
    atentamente = st.text_input("Emitido por (Atte.)", "ING. ELIO CORONEL GABRIEL")

with col2:
    # Cálculos Automáticos en Tiempo Real
    cant_num = st.number_input("Cantidad", min_value=1, value=5, step=1)
    unid = st.text_input("Unidad de Medida", "pza")
    p_unit_num = st.number_input("Precio Unitario ($)", min_value=0.0, value=600.00, step=0.01, format="%.2f")
    
    # El total se calcula multiplicando en tiempo real
    total_calculado = cant_num * p_unit_num
    
    # Convertimos a texto para Typst
    cant = str(cant_num)
    p_unit = f"{p_unit_num:.2f}"
    p_total = f"{total_calculado:.2f}"
    
    # Caja de texto informativa del total calculado (bloqueada)
    st.text_input("Precio Total ($) [Calculado Automáticamente]", p_total, disabled=True)

# Fuera de las columnas ocupa todo el ancho
descripcion = st.text_area("Descripción detallada", "Grating frp de vidrio 1 X 4", height=100)

st.markdown("---")

# 3. Tu diccionario original con las variables procesadas
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
        
        # 1. Guardar los datos de la cotización en Supabase
        guardar_datos_cotizacion(datos_nuevos)
        
        # 2. Incrementar el contador en Supabase para el siguiente documento
        incrementar_contador(num_actual)
        
        # 3. Guardamos el PDF en la memoria de la sesión para que no se borre al recargar
        st.session_state["pdf_listo"] = pdf_bytes
        st.session_state["archivo_nombre"] = f"Cotizacion_{nro_cotizacion.replace('/', '-')}.pdf"
        
        st.success("¡PDF generado con éxito de manera interna!")
        
        # 4. Forzamos la recarga automática para actualizar el número en pantalla de inmediato
        st.rerun()
        
    except Exception as e:
        st.error(f"Error al compilar el documento: {e}")

# =============================================================================
# MOSTRAR BOTÓN DE DESCARGA SI EL PDF YA SE GENERÓ
# =============================================================================
# Esto se coloca al final de todo el archivo, fuera de cualquier bloque "if"
if "pdf_listo" in st.session_state:
    st.markdown("### 📄 Tu documento está listo")
    st.download_button(
        label="📥 Descargar Archivo PDF",
        data=st.session_state["pdf_listo"],
        file_name=st.session_state["archivo_nombre"],
        mime="application/pdf",
        use_container_width=True
    )
    # Opcional: Limpiamos la sesión para que el botón desaparezca al cambiar de pestaña
    del st.session_state["pdf_listo"]