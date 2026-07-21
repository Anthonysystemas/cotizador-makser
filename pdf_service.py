import json
import typst
from database import guardar_datos_cotizacion, incrementar_contador

def generar_documento_cotizacion(datos, num_actual):
    try:
        campos_texto = ["nro_cotizacion", "fecha", "cliente", "contacto", "atentamente", "p_total_general"]
        datos_para_typst = {k: str(datos[k]) for k in campos_texto}
        datos_para_typst["productos_json"] = json.dumps(datos["productos"])

        pdf_bytes = typst.compile("plantilla.typ", sys_inputs=datos_para_typst)

        guardar_datos_cotizacion(datos)
        incrementar_contador(num_actual)

        return pdf_bytes
    except Exception as e:
        raise Exception(f"Fallo en el servicio de cotización: {e}")