import streamlit as st

import database as db
import pdf_service as svc

PREFIJOS_A_LIMPIAR = ("ft_", "cg_")


def _limpiar_para_nueva_cotizacion():
    """Borra del session_state todos los campos de la cotización anterior
    para que el formulario quede listo para una nueva."""
    claves_a_borrar = [
        k
        for k in st.session_state.keys()
        if k.startswith(PREFIJOS_A_LIMPIAR) or k == "lista_productos"
    ]
    for k in claves_a_borrar:
        del st.session_state[k]
    st.session_state["lista_productos"] = []


def renderizar_condiciones(codigo_cotizacion=None, num_actual=None):
    """Renderiza la Pestaña 3: Condiciones Generales y Generación de PDF."""
    st.title("Condiciones Generales")

    if codigo_cotizacion:
        st.session_state["numero_cotizacion"] = codigo_cotizacion
    if num_actual:
        st.session_state["num_actual_cotizacion"] = num_actual

    # -------------------------------------------------------------
    # 1. VALORES AUTOMÁTICOS / FIJOS DE CONDICIONES GENERALES
    # -------------------------------------------------------------
    st.session_state["cond_precios"] = st.session_state.get(
        "cond_precios", "En Dólares USA / No incluyen IGV"
    )
    st.session_state["cond_forma_pago"] = st.session_state.get(
        "cond_forma_pago", "50% de adelanto y saldo contra entrega"
    )
    st.session_state["cond_validez_oferta"] = st.session_state.get(
        "cond_validez_oferta", "07 días calendarios"
    )
    st.session_state["cond_garantia"] = st.session_state.get(
        "cond_garantia", "1 año por defectos de fabricación"
    )
    st.session_state["cond_lugar_entrega"] = st.session_state.get(
        "cond_lugar_entrega", "Planta Carabayllo / Puesto en obra según acuerdo"
    )

    # -------------------------------------------------------------
    # 2. ÚNICO CAMPO EDITABLE EN INTERFAZ
    # -------------------------------------------------------------
    with st.container(border=True):
        st.text_input(
            "Tiempo de Entrega *",
            value=st.session_state.get(
                "cond_tiempo_entrega", "03 a 05 días hábiles previa aprobación"
            ),
            key="cond_tiempo_entrega",
            help="Escriba el plazo de entrega para esta cotización",
        )

    st.markdown("---")

    # -------------------------------------------------------------
    # 3. BOTÓN DE GENERACIÓN Y DESCARGA DEL PDF
    # -------------------------------------------------------------
    st.subheader("2. Finalizar Cotización")

    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        generar = st.button(
            "⚙️ Generar Documento PDF", type="primary", use_container_width=True
        )

    if generar:
        try:
            platina = st.session_state.get("ft_platina_portante", '3/16" x 1 1/2"')
            acabado_base = st.session_state.get("ft_acabado", "Con platinas dentadas y en negro natural.")

            detalles_base = st.session_state.get("ft_detalles", [])
            detalles_completos = [{"etiqueta": "Platina Portante (PP)", "valor": platina}] + detalles_base

            datos_cotizacion = {
                "nro_cotizacion": st.session_state.get("numero_cotizacion", "COT-001"),
                "fecha": st.session_state.get("fecha_cotizacion", ""),
                "cliente": st.session_state.get("cliente", ""),
                "contacto": st.session_state.get("contacto", ""),
                "atentamente": st.session_state.get("atentamente", "Área Comercial"),
                "p_total_general": st.session_state.get("p_total_general", "0.00"),
                "productos": st.session_state.get("lista_productos", []),
                "ficha_tecnica": {
                    "codigo_ficha": st.session_state.get("ft_codigo_ficha", ""),
                    "titulo_producto": st.session_state.get("ft_titulo_producto", "GRATING TOPI 19W-4"),
                    "norma": st.session_state.get("ft_norma", "FABRICACIÓN SEGÚN NORMA NAAMM MB 531"),
                    "etiqueta_material": st.session_state.get("ft_etiqueta_material", "Materiales Platinas y Barra:"),
                    "valor_material": st.session_state.get("ft_valor_material", "ASTM A36 DE ACEROS AREQUIPA."),
                    "acabado": acabado_base,
                    "imagen_url": st.session_state.get("ft_imagen_url", "images/GRATING.jpg"),
                    "nota_pie": st.session_state.get("ft_nota_pie", "NOTA: Precio en la Planta."),
                    "detalles": detalles_completos,
                },
                "condiciones_generales": {
                    "precios": st.session_state.get("cond_precios", "En Dólares USA / No incluyen IGV"),
                    "forma_pago": st.session_state.get("cond_forma_pago", ""),
                    "tiempo_entrega": st.session_state.get("cond_tiempo_entrega", ""),
                    "tiempo_validez": st.session_state.get("cond_validez_oferta", ""),
                },
            }

            numero_actual_cot = st.session_state.get(
                "num_actual_cotizacion", num_actual or 1
            )

            # Invocar servicio Typst
            pdf_bytes = svc.generar_documento_cotizacion(
                datos_cotizacion, numero_actual_cot
            )

            st.session_state["pdf_bytes"] = pdf_bytes
            st.success("¡PDF generado con éxito!")

        except Exception as e:
            st.error(f"Error al generar el PDF: {e}")

    # Descarga directa del archivo PDF
    if "pdf_bytes" in st.session_state and st.session_state["pdf_bytes"]:
        nro_doc = st.session_state.get("numero_cotizacion", "Cotizacion").replace("/", "_")
        nombre_archivo = f"{nro_doc}.pdf"

        with col_btn2:
            st.download_button(
                label="📥 Descargar Cotización PDF",
                data=st.session_state["pdf_bytes"],
                file_name=nombre_archivo,
                mime="application/pdf",
                type="secondary",
                use_container_width=True,
            )