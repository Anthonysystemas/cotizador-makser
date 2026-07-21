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
        # 1. Cabecera
        respuesta_cabecera = supabase.table("cotizaciones").insert({
            "nro_cotizacion": datos["nro_cotizacion"],
            "fecha": datos["fecha"],
            "cliente": datos["cliente"],
            "contacto": datos["contacto"],
            "atentamente": datos["atentamente"]
        }).execute()

        if not respuesta_cabecera.data:
            raise Exception("No se pudo obtener el ID de la cotización generada.")

        cotizacion_id_generado = respuesta_cabecera.data[0]["id"]

        # 2. Detalles (Conversión segura de datos)
        detalles_a_insertar = []

        for prod in datos.get("productos", []):
            # Casteo seguro de valores numéricos
            cant_val = int(float(str(prod["cant"]).replace(",", ".")))
            p_unit_val = float(str(prod["p_unit"]).replace(",", "."))
            p_total_val = float(str(prod["p_total"]).replace(",", "."))

            detalles_a_insertar.append({
                "cotizacion_id": cotizacion_id_generado,
                "cantidad": cant_val,
                "unidad": str(prod["unid"]),
                "descripcion": str(prod["descripcion"]),
                "precio_unitario": p_unit_val,
                "precio_total": p_total_val
            })

        if detalles_a_insertar:
            supabase.table("detalle_cotizaciones").insert(detalles_a_insertar).execute()

    except Exception as e:
        raise Exception(f"Error en BD al guardar la cotización completa: {e}")