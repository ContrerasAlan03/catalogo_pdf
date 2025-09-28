# Catalogo PDF

## Como funciona el proyecto
- catalogo_pdf/cli.py (lineas 98-124) parsea argumentos de linea de comandos, carga tu JSON o CSV y arma un Catalogo listo para renderizado.
- catalogo_pdf/io.py (lineas 13-39) convierte los datos crudos en instancias de producto y acepta archivos .json o .csv.
- catalogo_pdf/config.py (lineas 14-55) define margenes, tipografias y parametros del encabezado, incluidos los logos.
- catalogo_pdf/render/builder.py crea un lienzo ReportLab y entrega cada pagina; el encabezado se dibuja con catalogo_pdf/render/header.py (lineas 60-100), que coloca los logos y centra el titulo.

## Paso a paso para generar tu PDF desde JSON
1. Instala dependencias: crea un entorno virtual y ejecuta pip install reportlab (agrega otras librerias que uses en el proyecto).
2. Coloca tus logos en la carpeta imagenes (ver seccion de nombres). Si quieres usar otras rutas, ajusta la configuracion segun la seccion de ajustes.
3. Prepara el archivo JSON con la estructura recomendada (ver ejemplo al final).
4. Ejecuta el generador desde la raiz del proyecto:
   python -m catalogo_pdf.cli --input ruta/a/tus_productos.json --output catalogo.pdf
   - Omite --input para generar el PDF demo con los datos internos (catalogo_pdf/cli.py:13-90).
   - Usa --montserrat-regular y --montserrat-negrita si quieres registrar fuentes personalizadas.
5. Revisa el PDF generado en la ruta indicada en --output.

## Carpeta y nombres de imagenes
- Ubicacion por defecto: coloca todos los recursos graficos en la carpeta imagenes, al mismo nivel que catalogo_pdf.
- Logos esperados:
  - AUTOVENZ-LOGO.png (logo principal, se dibuja a la izquierda del encabezado).
  - APR-LOGO.png (logo aliado, se dibuja a la derecha).
- Si usas otros nombres o formatos, actualiza las rutas en catalogo_pdf/config.py (lineas 10-23).

## Donde modificar rutas y ajustes
- Ruta base y nombre del logo principal (catalogo_pdf/config.py:10): cambia el Path para apuntar a tu archivo si no usas imagenes/AUTOVENZ-LOGO.png.
- Ruta base y nombre del logo aliado (catalogo_pdf/config.py:11): igual que el anterior, pero para el logo de la derecha.
- Rutas pasadas a cada ejecucion (catalogo_pdf/config.py:22-23): sobrescribe logo_autovenz y logo_apr al crear una instancia de LayoutConfig si quieres rutas distintas por ejecucion.
- Altura maxima visible de los logos (catalogo_pdf/config.py:24): incrementa o reduce alto_max_logo_encabezado para escalar los logos sin deformarlos.
- Texto centrado en el encabezado (catalogo_pdf/render/header.py:89): ajusta la cadena titulo para cambiar el mensaje central.
- Colores y tipografias del encabezado (catalogo_pdf/config.py:33-50): modifica fuentes y colores utilizados por el renderer.
- Salida y carga de datos por CLI (catalogo_pdf/cli.py:98-124): personaliza argumentos como --input, --output y fuentes.

## Estructura recomendada del JSON
El comando espera una lista de productos. Cada producto debe incluir, al menos, las mismas llaves usadas en los datos demo:
[
  {
    "categoria": "Sistema de Frenos",
    "nombre": "Pastillas Ceramicas Premium",
    "precio": "89.90 EUR",
    "oem": "OEM-12345",
    "descripcion": "Juego de pastillas con sensor de desgaste y compuesto ceramico."
  }
]

Campos adicionales seran ignorados por el renderer, pero puedes extender catalogo_pdf/model.py si necesitas mostrarlos.
