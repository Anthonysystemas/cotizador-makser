import json
import typst
from database import (
    guardar_condiciones_generales,
    guardar_datos_cotizacion,
    incrementar_contador,
    supabase,
)


def generar_documento_cotizacion(datos, num_actual):
  try:
    datos_para_typst = {}

    # 1. Campos de texto básicos (se pasan directamente como string)
    campos_texto = [
        "nro_cotizacion",
        "fecha",
        "cliente",
        "contacto",
        "atentamente",
        "p_total_general",
    ]
    for k in campos_texto:
      datos_para_typst[k] = str(datos.get(k, ""))

    # 2. Productos en formato JSON
    datos_para_typst["productos_json"] = json.dumps(datos.get("productos", []))

    # 3. Datos de la Ficha Técnica
    ficha = datos.get("ficha_tecnica", {})
    datos_para_typst["mostrar_ficha_tecnica"] = "true" if datos.get("mostrar_ficha_tecnica", True) else "false"
    datos_para_typst["nro_ficha"] = str(ficha.get("codigo_ficha", ""))
    datos_para_typst["producto_nombre"] = str(ficha.get("titulo_producto", ""))
    datos_para_typst["norma"] = str(ficha.get("norma", ""))
    datos_para_typst["etiqueta_mat"] = str(ficha.get("etiqueta_material", ""))
    datos_para_typst["valor_mat"] = str(ficha.get("valor_material", ""))
    datos_para_typst["acabado"] = str(ficha.get("acabado", ""))
    datos_para_typst["nota_pie"] = str(ficha.get("nota_pie", ""))
    datos_para_typst["imagen_producto"] = str(ficha.get("imagen_url", ""))
    datos_para_typst["especificaciones_json"] = json.dumps(
        ficha.get("detalles", [])
    )

    # 4. Condiciones Generales
    condiciones = datos.get("condiciones_generales", {})
    datos_para_typst["precios"] = str(condiciones.get("precios", ""))
    datos_para_typst["forma_pago"] = str(condiciones.get("forma_pago", ""))
    datos_para_typst["tiempo_entrega"] = str(condiciones.get("tiempo_entrega", ""))
    datos_para_typst["tiempo_validez"] = str(condiciones.get("tiempo_validez", ""))

    # Compilación limpia del PDF
    pdf_bytes = typst.compile("plantilla.typ", sys_inputs=datos_para_typst)

    # Registro en base de datos (opcional - no interrumpe la generación del PDF)
    if supabase:
      try:
        cotizacion_id = guardar_datos_cotizacion(datos)
        guardar_condiciones_generales(cotizacion_id, condiciones)
        incrementar_contador(num_actual)
      except Exception as db_err:
        print(f"⚠️  Error al guardar en BD (PDF generado igual): {db_err}")

    return pdf_bytes
  except Exception as e:
    raise Exception(f"Fallo en el servicio de cotización: {e}")


def generar_pdf_ficha_tecnica(codigo_ficha: str) -> bytes:
  if supabase is None:
    raise Exception(
        "Supabase no está configurado. No se puede obtener la ficha técnica."
    )
  try:
    res = (
        supabase.table("caracteristicas_tecnicas")
        .select("*, detalles_caracteristicas_tecnicas(*)")
        .eq("codigo_ficha", codigo_ficha)
        .execute()
    )

    if not res.data:
      raise Exception(
          f"No se encontró la ficha técnica con el código: {codigo_ficha}"
      )
    ficha = res.data[0]

    detalles = ficha.get("detalles_caracteristicas_tecnicas", [])
    detalles.sort(key=lambda x: x.get("orden", 0))

    campos_ficha = [
        "codigo_ficha",
        "titulo_producto",
        "norma",
        "etiqueta_material",
        "valor_material",
        "acabado",
        "imagen_url",
        "nota_pie",
    ]

    datos_typst = {k: str(ficha.get(k, "")) for k in campos_ficha}
    datos_typst["detalles_json"] = json.dumps(detalles)

    pdf_bytes = typst.compile(
        "plantilla_ficha_tecnica.typ", sys_inputs=datos_typst
    )

    return pdf_bytes

  except Exception as e:
    raise Exception(f"Fallo en el servicio de ficha técnica: {e}")