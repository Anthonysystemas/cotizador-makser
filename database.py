import os
from supabase import create_client, Client

# Credenciales
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://qsndihdikzxleihyazlt.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_t0zRA7Neynf2lSATcw3QDA_EN2AZQaM")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def obtener_siguiente_codigo():
    try:
        respuesta = supabase.table("contador_cotizacion").select("numero, anio").eq("id", 1).execute()
        if respuesta.data:
            registro = respuesta.data[0]
            return f"{registro['numero']}/{registro['anio']}", registro["numero"], registro["anio"]
    except Exception as e:
        raise Exception(f"Error en BD al obtener código: {e}")
    return "000/00", 0, 0

def incrementar_contador(numero_actual):
    try:
        nuevo_numero = numero_actual + 1
        supabase.table("contador_cotizacion").update({"numero": nuevo_numero}).eq("id", 1).execute()
    except Exception as e:
        raise Exception(f"Error en BD al incrementar: {e}")

def guardar_datos_cotizacion(datos):
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
        raise Exception(f"Error en BD al guardar: {e}")