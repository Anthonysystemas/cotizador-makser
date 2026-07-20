import typst
from database import guardar_datos_cotizacion, incrementar_contador

def generar_documento_cotizacion(datos, num_actual):
    """Orquesta la compilación del PDF y el registro en la base de datos."""
    try:
        # 1. Intentar compilar el PDF con Typst
        pdf_bytes = typst.compile("plantilla.typ", sys_inputs=datos)
        
        # 2. Si compila bien, guardar datos en Supabase
        guardar_datos_cotizacion(datos)
        
        # 3. Incrementar el contador correlativo
        incrementar_contador(num_actual)
        
        return pdf_bytes
    except Exception as e:
        # Si algo falla en el camino, lanza el error hacia la vista
        raise Exception(f"Fallo en el servicio de cotización: {e}")