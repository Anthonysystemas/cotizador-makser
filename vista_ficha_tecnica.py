import os
import time
import streamlit as st


def renderizar_ficha_tecnica():
    """Renderiza la Pestaña 2: Ficha Técnica.
    Muestra visualmente todos los datos fijos de la plantilla de Typst (solo lectura)
    y permite editar los campos específicos (Acabado, Platina, Imagen y Nota).
    """
    st.title("Ficha Técnica")

    # -------------------------------------------------------------
    # 0. CHECKBOX INICIAL (¿LLEVA FICHA TÉCNICA?)
    # -------------------------------------------------------------
    lleva_ficha = st.checkbox(
        "¿Esta cotización incluye Ficha Técnica?",
        value=st.session_state.get("lleva_ficha_tecnica", True)
    )
    st.session_state["lleva_ficha_tecnica"] = lleva_ficha

    if not lleva_ficha:
        st.info("ℹ️ Esta cotización no incluirá Ficha Técnica en el documento final.")
        return

    # -------------------------------------------------------------
    # 1. VALORES AUTOMÁTICOS / FIJOS DE LA PLANTILLA TYPST
    # -------------------------------------------------------------
    if "ft_codigo_ficha" not in st.session_state:
        st.session_state["ft_codigo_ficha"] = f"FT-2026-{str(int(time.time()))[-4:]}"

    st.session_state["ft_titulo_producto"] = st.session_state.get(
        "ft_titulo_producto", "GRATING TOPI 19W-4"
    )
    st.session_state["ft_norma"] = st.session_state.get(
        "ft_norma", "FABRICACIÓN SEGÚN NORMA NAAMM MB 531"
    )
    st.session_state["ft_etiqueta_material"] = st.session_state.get(
        "ft_etiqueta_material", "Materiales Platinas y Barra:"
    )
    st.session_state["ft_valor_material"] = st.session_state.get(
        "ft_valor_material", "ASTM A36 DE ACEROS AREQUIPA."
    )
    st.session_state["ft_detalles"] = st.session_state.get("ft_detalles", [
        {"etiqueta": "Separación entre platinas (SP)", "valor": "30mm"},
        {"etiqueta": "Barra cuadrilla torsional", "valor": "1/4″"},
        {"etiqueta": "Separación entre barras (SB)", "valor": "102mm"},
    ])

    # -------------------------------------------------------------
    # 2. CAMPOS EDITABLES (lo único que el usuario puede cambiar)
    # -------------------------------------------------------------
    st.subheader("1. Edición de Ficha Técnica")

    with st.container(border=True):
        col_ft1, col_ft2 = st.columns(2)

        with col_ft1:
            st.text_input(
                "Acabado *",
                value=st.session_state.get("ft_acabado", "Con platinas dentadas y en negro natural."),
                key="ft_acabado",
                help="Especifique el acabado del producto",
            )

            st.text_input(
                "Platina Portante (PP) *",
                value=st.session_state.get("ft_platina_portante", '3/16" x 1 1/2"'),
                key="ft_platina_portante",
                help="Modifique la medida de la Platina Portante",
            )

        with col_ft2:
            imagen_subida = st.file_uploader(
                "Imagen del producto *",
                type=["jpg", "jpeg", "png"],
                help="Si no subes una imagen, se usará la imagen por defecto.",
                key="ft_imagen_subida",
            )

            if imagen_subida is not None:
                os.makedirs("images/subidas", exist_ok=True)
                extension = imagen_subida.name.split(".")[-1].lower()
                codigo_ficha_actual = st.session_state["ft_codigo_ficha"]
                nombre_archivo = f"images/subidas/{codigo_ficha_actual}.{extension}"

                with open(nombre_archivo, "wb") as archivo_salida:
                    archivo_salida.write(imagen_subida.getbuffer())

                st.session_state["ft_imagen_url"] = nombre_archivo
                st.image(imagen_subida, caption="Vista previa del producto", width=150)
            elif "ft_imagen_url" not in st.session_state:
                st.session_state["ft_imagen_url"] = "images/GRATING.jpg"

    # -------------------------------------------------------------
    # 3. NOTA (texto libre, aparece en la parte inferior del PDF)
    # -------------------------------------------------------------
    st.subheader("2. Nota")

    with st.container(border=True):
        st.text_input(
            "Nota *",
            value=st.session_state.get("ft_nota_pie", "NOTA: Precio en la Planta."),
            key="ft_nota_pie",
            help="Texto que aparecerá en la parte inferior de la cotización en el PDF",
        )