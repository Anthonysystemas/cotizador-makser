// Leer variables enviadas desde Python (con valores por defecto por si acaso)
#let nro_cotizacion = sys.inputs.at("nro_cotizacion", default: "296/26")
#let fecha = sys.inputs.at("fecha", default: "Lima 24 de Junio de 2026")
#let cliente = sys.inputs.at("cliente", default: "PREMOSAIC S.A.")
#let contacto = sys.inputs.at("contacto", default: "Fabio Gutierrez")

// Datos del artículo
#let cant = sys.inputs.at("cant", default: "1")
#let unid = sys.inputs.at("unid", default: "gl")
#let descripcion = sys.inputs.at("descripcion", default: "Grating 10 piezas según plano...")
#let p_unit = sys.inputs.at("p_unit", default: "1050.00")
#let p_total = sys.inputs.at("p_total", default: "1050.00")
#let atentamente = sys.inputs.at("Attentamente", default: "ING. ELIO CORONEL GABRIEL")

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

// --- TABLA DE ARTÍCULOS ---
#set table(stroke: 0.5pt + black)
#table(
  columns: (40pt, 40pt, 1fr, 55pt, 55pt),
  align: (center, center, left, right, right),
  fill: (x, y) => if y == 0 { rgb("#f2f2f2") } else { white },
  [*CAN*], [*UN*], [#align(center)[*DESCRIPCIÓN*]], [*P. UNIT.*], [*P. TOTAL*],
  [#cant], [#unid], [#descripcion], [#p_unit], [#p_total]
)

// --- ESPECIFICACIONES TÉCNICAS ---
#rect(width: 100%, stroke: 0.5pt + black, inset: 10pt)[
  #text(weight: "bold", size: 9pt)[CARACTERÍSTICAS TÉCNICAS GRATING TOPI 19W-4]
  #v(2pt)
  #grid(
    columns: (1fr, auto),
    gutter: 1em,
    [
      #set text(size: 9pt)
      - Platina Portante (PP) = 3/16" x 1 1/2"
      - Separación entre platinas (SP) = 30mm
      - Barra cuadrilla torsional = 1/4"
      - Separación entre barras (SB) = 102mm
      
      #v(5pt)
      *FABRICACIÓN SEGÚN NORMA NAAMM MB 531*\
      Materiales Platinas y Barra: ASTM A36 DE ACEROS AREQUIPA.\
      *Acabado: Con platinas dentadas y en negro natural.*
    ],
    image("images/GRATING.jpg", width: 140pt)
  )
]

#v(-2pt)
#text(fill: blue, weight: "bold", size: 9pt)[NOTA: Precio en la Planta.]

#v(10pt)

// --- CONDICIONES GENERALES ---
#text(weight: "bold", size: 10pt)[CONDICIONES GENERALES:]
#v(2pt)
#grid(
  columns: (15pt, 140pt, 1fr),
  row-gutter: 8pt,
  align: (left, left, left),
  
  [a)], [PRECIOS], [: *En Dólares USA. No Incluye IGV.*],
  [b)], [FORMA DE PAGO], [: 50% de adelanto y saldo contra entrega. *Depósito en Cta. Cte. N° 191 1479035 1 56 Banco de Crédito en Dólares.*],
  [c)], [TIEMPO DE ENTREGA], [: 8 días útiles a partir del adelanto.],
  [d)], [TIEMPO VALIDEZ DE PRECIO], [: 7 días calendarios.]
)

#v(30pt)
#align(center)[
  #text(size: 10pt)[
    Atte. #h(0.5em) #text(fill: blue, weight: "bold")[#atentamente]
  ]
]