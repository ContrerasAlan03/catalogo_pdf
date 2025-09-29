"""Rutinas para dibujar el encabezado de cada pagina."""
from __future__ import annotations
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

from ..config import LayoutConfig
from .canvas_types import CanvasTipo


def _cargar_logo(ruta: Path | str | None) -> ImageReader | None:
    """Carga el logo desde disco si la ruta es valida."""
    if not ruta:
        return None
    ruta_path = Path(ruta)
    if not ruta_path.is_file():
        return None
    try:
        return ImageReader(str(ruta_path))
    except OSError:
        return None


def _dibujar_logo(
        
    lienzo: CanvasTipo,
    imagen: ImageReader | None,
    x: float,
    centro_y: float,
    max_altura: float,
    *,
    anchor: str = "left",
) -> float:
    #Dibuja un logo alineado y devuelve el ancho usado.
    
    if imagen is None:
        return 0.0
    ancho_original, alto_original = imagen.getSize()
    if alto_original <= 0:
        return 0.0
    escala = min(0.8, max_altura / float(alto_original))
    ancho = float(ancho_original) * escala
    alto = float(alto_original) * escala
    posicion_x = x - ancho if anchor == "right" else x
    posicion_y = centro_y - alto / 2
    lienzo.drawImage(
        imagen,
        posicion_x,
        posicion_y,
        width=ancho,
        height=alto,
        preserveAspectRatio=True,
        mask="auto",
    )
    return ancho


def dibujar_encabezado(lienzo: CanvasTipo, configuracion: LayoutConfig) -> None:
    """Dibuja el encabezado principal con logos y linea divisoria."""
    ancho_pagina, alto_pagina = A4
    altura_banner = getattr(configuracion, "altura_encabezado", alto_pagina * 0.28)  # o fija un número
    limite_superior = alto_pagina  # SIN margen arriba
    limite_inferior = limite_superior - altura_banner

    centro_y = limite_inferior + configuracion.altura_encabezado / 2

    lienzo.saveState()
    lienzo.setFillColor(configuracion.color_fondo_encabezado)
    lienzo.rect(0, limite_inferior, ancho_pagina, configuracion.altura_encabezado, stroke=0, fill=1)

    logo_autovenz = _cargar_logo(configuracion.logo_autovenz)
    logo_apr = _cargar_logo(configuracion.logo_apr)
    posicion_autovenz_x = configuracion.margen_x + configuracion.offset_logo_autovenz
    altura_autovenz = configuracion.alto_logo_autovenz or configuracion.alto_max_logo_encabezado
    posicion_apr_x = ancho_pagina - configuracion.margen_x + configuracion.offset_logo_apr
    altura_apr = configuracion.alto_logo_apr or configuracion.alto_max_logo_encabezado
    _dibujar_logo(
        lienzo,
        logo_autovenz,
        posicion_autovenz_x,
        centro_y,
        altura_autovenz,
    )
    _dibujar_logo(
        lienzo,
        logo_apr,
        posicion_apr_x,
        centro_y,
        altura_apr,
        anchor="right",
    )

    titulo = configuracion.titulo_encabezado
    lienzo.setFont(configuracion.fuente_encabezado, configuracion.tamano_marca_encabezado)
    #lienzo.setFillColor(colors.white)
    lienzo.drawCentredString(
        ancho_pagina / 2,
        centro_y - configuracion.tamano_marca_encabezado / 3,
        titulo,
    )

    lienzo.setStrokeColor(configuracion.color_secundario)
    lienzo.setLineWidth(1.2)
    lienzo.line(
        configuracion.margen_x,
        limite_inferior,
        ancho_pagina - configuracion.margen_x,
        limite_inferior,
    )
    lienzo.restoreState()

