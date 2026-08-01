import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from supabase import Client, create_client


if load_dotenv:
    load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
  raise ValueError(
      "Faltan las credenciales de Supabase.\n\n"
      "Configúralas según tu entorno:\n\n"
      "1. LOCAL: Crea un archivo '.env' en la raíz del proyecto con:\n"
      "   SUPABASE_URL=https://...supabase.co\n"
      "   SUPABASE_KEY=sb_...\n\n"
      "2. RENDER: En el dashboard de Render, ve a tu servicio → "
      "Environment → Environment Variables y agrega:\n"
      "   SUPABASE_URL  = https://tu-proyecto.supabase.co\n"
      "   SUPABASE_KEY  = sb_...\n\n"
      "3. STREAMLIT: En .streamlit/secrets.toml o Streamlit Cloud Secrets."
  )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# FUNCIONES PARA COTIZACIONES
# ==========================================


def obtener_siguiente_codigo():
  """Obtiene el correlativo actual de cotización desde la tabla 'contador_cotizacion'."""
  try:
    respuesta = (
        supabase.table("contador_cotizacion")
        .select("numero, anio")
        .eq("id", 1)
        .execute()
    )
    if respuesta.data:
      registro = respuesta.data[0]
      return (
          f"{registro['numero']}/{registro['anio']}",
          registro["numero"],
          registro["anio"],
      )
  except Exception as e:
    raise Exception(f"Error en BD al obtener código: {e}")
  return "000/00", 0, 0


def incrementar_contador(numero_actual):
  """Incrementa en 1 el contador de cotizaciones en la base de datos."""
  try:
    nuevo_numero = numero_actual + 1
    supabase.table("contador_cotizacion").update({"numero": nuevo_numero}).eq(
        "id", 1
    ).execute()
  except Exception as e:
    raise Exception(f"Error en BD al incrementar el contador: {e}")


def guardar_datos_cotizacion(datos):
  """Guarda la cabecera en 'cotizaciones' y sus items en 'detalle_cotizaciones'."""
  try:
    # 1. Cabecera de la Cotización
    respuesta_cabecera = (
        supabase.table("cotizaciones")
        .insert({
            "nro_cotizacion": datos.get("nro_cotizacion"),
            "fecha": datos.get("fecha"),
            "cliente": datos.get("cliente"),
            "contacto": datos.get("contacto"),
            "atentamente": datos.get("atentamente"),
        })
        .execute()
    )

    if not respuesta_cabecera.data:
      raise Exception(
          "No se pudo obtener el ID de la cotización generada."
      )

    cotizacion_id_generado = respuesta_cabecera.data[0]["id"]

    # 2. Detalles de Productos
    detalles_a_insertar = []
    for prod in datos.get("productos", []):
      cant_val = int(float(str(prod.get("cant", 0)).replace(",", ".")))
      p_unit_val = float(str(prod.get("p_unit", 0)).replace(",", "."))
      p_total_val = float(str(prod.get("p_total", 0)).replace(",", "."))

      detalles_a_insertar.append({
          "cotizacion_id": cotizacion_id_generado,
          "cantidad": cant_val,
          "unidad": str(prod.get("unid", "")),
          "descripcion": str(prod.get("descripcion", "")),
          "precio_unitario": p_unit_val,
          "precio_total": p_total_val,
      })

    if detalles_a_insertar:
      supabase.table("detalle_cotizaciones").insert(
          detalles_a_insertar
      ).execute()

    return cotizacion_id_generado

  except Exception as e:
    raise Exception(f"Error en BD al guardar la cotización completa: {e}")


# ==========================================
# FUNCIONES PARA FICHA TÉCNICA
# ==========================================


def obtener_ficha_tecnica_por_id(ficha_id: int):
  """Obtiene la cabecera y las características dinámicas de una Ficha Técnica por su ID."""
  try:
    respuesta = (
        supabase.table("caracteristicas_tecnicas")
        .select("*, detalles_caracteristicas_tecnicas(*)")
        .eq("id", ficha_id)
        .single()
        .execute()
    )
    return respuesta.data
  except Exception as e:
    raise Exception(
        f"Error en BD al obtener la ficha técnica {ficha_id}: {e}"
    )


def guardar_ficha_tecnica(datos_ficha):
  """Guarda la cabecera en 'caracteristicas_tecnicas' y sus características

  hijo en 'detalles_caracteristicas_tecnicas'.
  """
  try:
    # 1. Insertar Cabecera (Padre)
    respuesta_padre = (
        supabase.table("caracteristicas_tecnicas")
        .insert({
            "codigo_ficha": datos_ficha.get("codigo_ficha"),
            "titulo_producto": datos_ficha.get("titulo_producto"),
            "norma": datos_ficha.get("norma"),
            "etiqueta_material": datos_ficha.get("etiqueta_material"),
            "valor_material": datos_ficha.get("valor_material"),
            "acabado": datos_ficha.get("acabado"),
            "imagen_url": datos_ficha.get("imagen_url"),
            "nota_pie": datos_ficha.get("nota_pie"),
        })
        .execute()
    )

    if not respuesta_padre.data:
      raise Exception(
          "No se pudo obtener el ID de la Ficha Técnica creada."
      )

    ficha_id_generado = respuesta_padre.data[0]["id"]

    # 2. Insertar Detalle (Hijo - Mapeo a 'caracteristica_id')
    detalles_a_insertar = []
    for idx, det in enumerate(datos_ficha.get("detalles", []), start=1):
      detalles_a_insertar.append({
          "caracteristica_id": ficha_id_generado,  # Columna en Supabase
          "orden": det.get("orden", idx),
          "etiqueta": str(det.get("etiqueta", "")),
          "valor": str(det.get("valor", "")),
      })

    if detalles_a_insertar:
      supabase.table("detalles_caracteristicas_tecnicas").insert(
          detalles_a_insertar
      ).execute()

    return ficha_id_generado

  except Exception as e:
    raise Exception(f"Error en BD al guardar la Ficha Técnica: {e}")

  # ==========================================
# FUNCIONES PARA CONDICIONES GENERALES
# ==========================================


def guardar_condiciones_generales(cotizacion_id, datos):
  """Guarda las condiciones generales de una cotización, ligadas por cotizacion_id."""
  try:
    supabase.table("condiciones_generales").insert({
        "cotizacion_id": cotizacion_id,
        "precios": datos.get("precios", ""),
        "forma_pago": datos.get("forma_pago", ""),
        "tiempo_entrega": datos.get("tiempo_entrega", ""),
        "tiempo_validez": datos.get("tiempo_validez", ""),
    }).execute()
  except Exception as e:
    raise Exception(f"Error en BD al guardar condiciones generales: {e}")

def buscar_ficha_por_codigo(codigo_ficha: str):
  """Busca una ficha técnica existente por su código único."""
  if not codigo_ficha:
    return None
  try:
    respuesta = (
        supabase.table("caracteristicas_tecnicas")
        .select("*, detalles_caracteristicas_tecnicas(*)")
        .eq("codigo_ficha", codigo_ficha)
        .execute()
    )
    return respuesta.data[0] if respuesta.data else None
  except Exception as e:
    raise Exception(f"Error en BD al buscar ficha por código: {e}")  