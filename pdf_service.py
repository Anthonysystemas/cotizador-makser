import typst
from database import guardar_datos_cotizacion, incrementar_contador

def generar_documento_cotizacion(datos, num_actual):
    """Orquesta la compilación del PDF y el registro en la base de datos."""
    try:
        # 1. Whitelist explícita: solo los campos que la plantilla Typst necesita.
        #    Esto evita que CUALQUIER campo nuevo que agregues a `datos` en el futuro
        #    (listas, dicts, números, etc.) rompa typst.compile sin que sepas por qué.
        campos_typst = [
            "nro_cotizacion", "fecha", "cliente", "contacto",
            "atentamente", "cant", "unid", "descripcion", "p_unit", "p_total",
        ]
        datos_para_typst = {k: str(datos[k]) for k in campos_typst}

        # 2. Validación defensiva (opcional pero útil para debug):
        #    si algo no es str puro, falla aquí con un mensaje claro en vez del
        #    error críptico de PyO3.
        no_str = {k: type(v) for k, v in datos_para_typst.items() if not isinstance(v, str)}
        if no_str:
            raise TypeError(f"Campos no-string antes de compilar: {no_str}")

        # 3. Compilar PDF solo con campos de texto
        pdf_bytes = typst.compile("plantilla.typ", sys_inputs=datos_para_typst)

        # 4. Guardar en Supabase (este sí necesita 'datos' completo con la lista "productos")
        guardar_datos_cotizacion(datos)

        # 5. Incrementar correlativo
        incrementar_contador(num_actual)

        return pdf_bytes

    except Exception as e:
        raise Exception(f"Fallo en el servicio de cotización: {e}")