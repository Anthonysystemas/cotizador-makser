// ==========================================
// 1. VARIABLES DE COTIZACIÓN Y CLIENTE
// ==========================================
#let nro_cotizacion = sys.inputs.at("nro_cotizacion", default: "296/26")
#let fecha = sys.inputs.at("fecha", default: "Lima 24 de Junio de 2026")
#let cliente = sys.inputs.at("cliente", default: "PREMOSAIC S.A.")
#let contacto = sys.inputs.at("contacto", default: "Fabio Gutierrez")
#let atentamente = sys.inputs.at("atentamente", default: "ING. ELIO CORONEL GABRIEL")
#let p_total_general = sys.inputs.at("p_total_general", default: "0.00")

// Parseo de lista de productos para la cotización
#let productos_json = sys.inputs.at("productos_json", default: "[]")
#let productos = json(bytes(productos_json))

// ==========================================
// 1B. VARIABLES DE CONDICIONES GENERALES (nuevo)
// ==========================================
#let precios = sys.inputs.at("precios", default: "En Dólares USA. No Incluye IGV.")
#let forma_pago = sys.inputs.at("forma_pago", default: "50% de adelanto y saldo contra entrega. Depósito en Cta. Cte. N° 191 1479035 1 56 Banco de Crédito en Dólares.")
#let tiempo_entrega = sys.inputs.at("tiempo_entrega", default: "8 días útiles a partir del adelanto.")
#let tiempo_validez = sys.inputs.at("tiempo_validez", default: "7 días calendarios.")

// ==========================================
// 2. VARIABLES EXCLUSIVAS DE FICHA TÉCNICA
// ==========================================
#let nro_ficha = sys.inputs.at("nro_ficha", default: "FT-2026-001")
#let producto_nombre = sys.inputs.at("producto_nombre", default: "GRATING ELECTROSOLDADO 19W-4")
#let categoria = sys.inputs.at("categoria", default: "Rejillas Industriales")
#let descripcion_general = sys.inputs.at("descripcion_general", default: "Rejilla metálica electrosoldada de alta resistencia.")
#let imagen_producto = sys.inputs.at("imagen_producto", default: "images/GRATING.jpg")

#let norma = sys.inputs.at("norma", default: "FABRICACIÓN SEGÚN NORMA NAAMM MB 531")
#let etiqueta_mat = sys.inputs.at("etiqueta_mat", default: "Materiales Platinas y Barra:")
#let valor_mat = sys.inputs.at("valor_mat", default: "ASTM A36 DE ACEROS AREQUIPA.")
#let acabado = sys.inputs.at("acabado", default: "Con platinas dentadas y en negro natural.")
#let nota_pie = sys.inputs.at("nota_pie", default: "NOTA: Precio en la Planta.")

// Parseo de características dinámicas (relación Padre-Hijo)
#let especificaciones_json = sys.inputs.at("especificaciones_json", default: "[]")
#let especificaciones = json(bytes(especificaciones_json))


#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 1.5cm, left: 2cm, right: 2cm),
  background: rect(
    width: 100% - 1cm,
    height: 100% - 1cm,
    stroke: 0.5pt + black,
    radius: 0pt
  )
)
#set text(font: "Liberation Sans", size: 10pt, lang: "es")

// --- ENCABEZADO ---
#grid(
  columns: (1fr, 2.2fr),
  gutter: 1.5em,
  align: (center + horizon, left + horizon),

  image("images/logo makser.jpg", width: 85%),

  [
    #align(center)[
      #text(fill: rgb("#ff0000"), weight: 900, size: 22pt)[MAKSER PERU S.A.C]\
      #v(-4pt)
      #text(fill: blue, weight: "bold", size: 12pt)[RUC: 20505579527]
    ]

    #v(5pt)

    #grid(
      columns: (24pt, 1fr),
      row-gutter: 9pt,
      align: (center + horizon, left + horizon),

      image("images/ubicacion.png", width: 14pt),
      [Av. Eduardo de Habich 318 Int 205 Urb. Ingeniería SMP],

      image("images/mapa.png", width: 14pt),
      [Av. Huarangal Parcela 42 Lot 25 Carabayllo],

      image("images/llamada-telefonica.png", width: 14pt),
      [*982798062*],

      image("images/email.png", width: 14pt),
      [jesus\@makserperu.com #h(4em) makser_peru\@yahoo.es]
    )
  ]
)

#v(-4pt)
#line(length: 100%, stroke: 2pt + rgb("#cc0000"))
#v(10pt)

// --- TÍTULO Y FECHA ---
#align(right)[
  #text(weight: "bold", size: 13pt)[COTIZACIÓN N° #nro_cotizacion]
]

#fecha

#v(8pt)
Señores:\
*#cliente*
#align(right)[
  *Atención: #contacto*
]

#v(8pt)
A su solicitud es grato presentar la cotización por el suministro de:

// --- TABLA DE ARTÍCULOS (multi-producto) ---
#set table(stroke: 0.5pt + black)
#table(
  columns: (40pt, 40pt, 1fr, 55pt, 55pt),
  align: (center, center, left, right, right),
  fill: (x, y) => if y == 0 { rgb("#f2f2f2") } else { white },
  [*CAN*], [*UN*], [#align(center)[*DESCRIPCIÓN*]], [*P. UNIT.*], [*P. TOTAL*],
  ..productos.map(p => (
    [#p.cant], [#p.unid], [#p.descripcion], [#p.p_unit], [#p.p_total]
  )).flatten()
)

#align(right)[
  #text(weight: "bold", size: 10pt)[TOTAL GENERAL: \$ #p_total_general]
]

// ==========================================
// BLOQUE DE CARACTERÍSTICAS TÉCNICAS
// ==========================================
#rect(width: 100%, stroke: 0.5pt + black, inset: 10pt)[
  #text(weight: "bold", size: 9pt)[CARACTERÍSTICAS TÉCNICAS #producto_nombre]
  #v(2pt)
   #grid(
     columns: (1fr, auto),
     gutter: 1em,
     [
       #set text(size: 9pt)

       #for item in especificaciones [
         - #item.etiqueta = #item.valor \
       ]

       #v(5pt)
       *#norma*\
       #etiqueta_mat #valor_mat \
       *Acabado: #acabado*
     ],
     box(
     width: 160pt,
     clip: true,
     radius: 4pt,
     [
       #image(
         imagen_producto, 
         width: 160pt,
         fit: "cover"
       )
     ]
   )
  )
]
#v(-2pt)
#text(fill: blue, weight: "bold", size: 9pt)[#nota_pie]

#v(10pt)

// --- CONDICIONES GENERALES (ahora dinámico) ---
#text(weight: "bold", size: 10pt)[CONDICIONES GENERALES:]
#v(2pt)
#grid(
  columns: (15pt, 140pt, 1fr),
  row-gutter: 8pt,
  align: (left, left, left),

  [a)], [PRECIOS], [: #strong[#precios]],
  [b)], [FORMA DE PAGO], [: #strong[#forma_pago]],
  [c)], [TIEMPO DE ENTREGA], [: #tiempo_entrega],
  [d)], [TIEMPO VALIDEZ DE PRECIO], [: #tiempo_validez]
)

#v(30pt)
#align(center)[
  #text(size: 10pt)[
    Atte. #h(0.5em) #text(fill: blue, weight: "bold")[#atentamente]
  ]
]