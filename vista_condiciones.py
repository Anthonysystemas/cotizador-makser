import streamlit as st

import database as db
import pdf_service as svc

PREFIJOS_A_LIMPIAR = ("ft_", "cg_")


def _limpiar_para_nueva_cotizacion():
  """Borra del session_state todos los campos de la cotización anterior
  para que el formulario quede listo para una nueva."""
  claves_a_borrar = [
      k for k in st.session_state.keys()
      if k.startswith(PREFIJOS_A_LIMPIAR) or k == "lista_productos"
  ]
  for k in claves_a_borrar:
    del st.session_state[k]
  st.session_state["lista_productos"] = []


def renderizar_condiciones(codigo_cotizacion, num_actual):
  """Renderiza la Pestaña 3: Condiciones Generales + botón final que
  guarda todo en Supabase y genera el PDF consolidado."""
  st.subheader("Condiciones Generales de la Cotización")

  with st.container(border=True):
    st.text_input(
        "a) Precios",
        value=st.session_state.get("cg_precios", "En Dólares USA. No Incluye IGV."),
        key="cg_precios",
    )
    st.text_area(
        "b) Forma de Pago",
        value=st.session_state.get(
            "cg_forma_pago",
            "50% de adelanto y saldo contra entrega. Depósito en Cta. Cte."
            " N° 191 1479035 1 56 Banco de Crédito en Dólares.",
        ),
        key="cg_forma_pago",
        height=100,
    )
    st.text_input(
        "c) Tiempo de Entrega",
        value=st.session_state.get("cg_tiempo_entrega", "8 días útiles a partir del adelanto."),
        key="cg_tiempo_entrega",
    )
    st.text_input(
        "d) Tiempo Validez de Precio",
        value=st.session_state.get("cg_tiempo_validez", "7 días calendarios."),
        key="cg_tiempo_validez",
    )


  st.markdown("---")
  generar = st.button(
      "⚡Generar Cotización",
      type="primary",
      use_container_width=True,
  )

  if generar:
    if not st.session_state.get("lista_productos"):
      st.error(
          "⚠️ Atención: Debes agregar al menos un producto en la Pestaña 1"
          " (Cotización) antes de continuar."
      )
      return

    num_filas_ft = int(st.session_state.get("ft_num_filas", 4))
    detalles_ficha = []
    for idx in range(num_filas_ft):
      caract_val = st.session_state.get(f"ft_caract_{idx}", "").strip()
      medida_val = st.session_state.get(f"ft_med_{idx}", "").strip()
      if caract_val and medida_val:
        detalles_ficha.append({
            "orden": idx + 1,
            "etiqueta": caract_val,
            "valor": medida_val,
        })

    try:
      with st.spinner("Guardando en Supabase y compilando PDF completo..."):
        datos_completos = {
            "nro_cotizacion": st.session_state.get("nro_cotizacion", codigo_cotizacion),
            "fecha": st.session_state.get("fecha", ""),
            "cliente": st.session_state.get("cliente", ""),
            "contacto": st.session_state.get("contacto", ""),
            "atentamente": st.session_state.get("atentamente", ""),
            "p_total_general": st.session_state.get("p_total_general", "0.00"),
            "productos": st.session_state.get("lista_productos", []),
            "condiciones_generales": {
                "precios": st.session_state.get("cg_precios", ""),
                "forma_pago": st.session_state.get("cg_forma_pago", ""),
                "tiempo_entrega": st.session_state.get("cg_tiempo_entrega", ""),
                "tiempo_validez": st.session_state.get("cg_tiempo_validez", ""),
            },
            "ficha_tecnica": {
                "codigo_ficha": st.session_state.get("ft_codigo_ficha", ""),
                "titulo_producto": st.session_state.get("ft_titulo_producto", ""),
                "norma": st.session_state.get("ft_norma", ""),
                "etiqueta_material": st.session_state.get("ft_etiqueta_material", ""),
                "valor_material": st.session_state.get("ft_valor_material", ""),
                "acabado": st.session_state.get("ft_acabado", ""),
                "imagen_url": st.session_state.get("ft_imagen_url", "images/GRATING.jpg"),
                "detalles": detalles_ficha,
            },
        }

        # 1. Guardar la Ficha Técnica en Supabase (padre/hijo)
        db.guardar_ficha_tecnica(datos_completos["ficha_tecnica"])

        # 2. Generar el PDF consolidado (guarda cotización + condiciones adentro)
        pdf_bytes = svc.generar_documento_cotizacion(datos_completos, num_actual)

        st.session_state["pdf_listo"] = pdf_bytes
        st.session_state["archivo_nombre"] = (
            f"Cotizacion_{codigo_cotizacion.replace('/', '-')}.pdf"
        )
        st.session_state["mostrar_alerta_exito"] = True

        # 3. Limpiar todo para poder generar una siguiente cotización
        _limpiar_para_nueva_cotizacion()

        st.rerun()

    except Exception as ex:
      st.error(f"❌ Error durante el proceso: {ex}")