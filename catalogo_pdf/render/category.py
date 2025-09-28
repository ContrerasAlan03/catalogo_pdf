"""Componentes para dibujar las cabeceras de cada categoria."""

from __future__ import annotations

from reportlab.lib.pagesizes import A4

from ..config import LayoutConfig
from .canvas_types import CanvasTipo
from .card import _dibujar_icono


def dibujar_categoria_banner(
    lienzo: CanvasTipo,
    configuracion: LayoutConfig,
    categoria: str,
    y_superior: float,
    ruta_icono: str | None,
) -> float:
    """Crea la franja de categoria y devuelve la nueva coordenada superior."""
    ancho_pagina, _ = A4
    altura_banner = configuracion.altura_banner_categoria
    limite_inferior = y_superior - altura_banner

    lienzo.saveState()
    lienzo.setFillColor(configuracion.color_fondo_categoria)
    radio_esquinas = 14
    lienzo.roundRect(
        configuracion.margen_x,
        limite_inferior,
        ancho_pagina - 2 * configuracion.margen_x,
        altura_banner,
        radio_esquinas,
        stroke=0,
        fill=1,
    )

    tamano_icono = configuracion.tamano_respaldo_icono
    icono_x = configuracion.margen_x + 24
    icono_y = limite_inferior + (altura_banner - tamano_icono) / 2
    _dibujar_icono(
        lienzo,
        ruta_icono,
        x=icono_x,
        y=icono_y,
        tamano=tamano_icono,
        color_respaldo=configuracion.color_respaldo_icono,
    )

    texto_x = icono_x + tamano_icono + 18
    etiqueta_y = limite_inferior + altura_banner - 22
    lienzo.setFont(configuracion.fuente_subtitulo, configuracion.tamano_etiqueta_categoria)
    lienzo.setFillColor(configuracion.color_secundario)
    lienzo.drawString(texto_x, etiqueta_y, "Categoria")

    lienzo.setFont(configuracion.fuente_encabezado, configuracion.tamano_titulo_categoria)
    lienzo.setFillColor(configuracion.color_texto_cuerpo)
    lienzo.drawString(texto_x, etiqueta_y - configuracion.tamano_titulo_categoria - 6, categoria.upper())
    lienzo.restoreState()
    return limite_inferior - configuracion.separacion_filas
