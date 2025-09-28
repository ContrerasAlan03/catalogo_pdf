"""Funciones de apoyo para calcular la grilla y saltos de pagina."""

from __future__ import annotations

from typing import List

from reportlab.lib.pagesizes import A4

from .config import LayoutConfig


def ancho_columna(configuracion: LayoutConfig, ancho_pagina: float | None = None) -> float:
    """Calcula el ancho util de cada columna del catalogo."""
    if ancho_pagina is None:
        ancho_pagina, _ = A4
    espacio_util = ancho_pagina - 2 * configuracion.margen_x
    separaciones = (configuracion.columnas - 1) * configuracion.separacion_columnas
    return (espacio_util - separaciones) / configuracion.columnas


def posiciones_columnas(configuracion: LayoutConfig, ancho_pagina: float | None = None) -> List[float]:
    """Devuelve las coordenadas X iniciales de cada columna."""
    if ancho_pagina is None:
        ancho_pagina, _ = A4
    base = configuracion.margen_x
    ancho = ancho_columna(configuracion, ancho_pagina)
    return [base + indice * (ancho + configuracion.separacion_columnas) for indice in range(configuracion.columnas)]


def altura_contenido_disponible(configuracion: LayoutConfig, alto_pagina: float | None = None) -> float:
    """Obtiene el alto disponible debajo del encabezado."""
    if alto_pagina is None:
        _, alto_pagina = A4
    return alto_pagina - configuracion.margen_y - configuracion.altura_encabezado - configuracion.separacion_encabezado


def filas_por_pagina(configuracion: LayoutConfig, alto_pagina: float | None = None) -> int:
    """Calcula cuantas filas completas caben debajo del encabezado."""
    altura_disponible = altura_contenido_disponible(configuracion, alto_pagina)
    altura_fila = configuracion.altura_minima_tarjeta + configuracion.separacion_filas
    if altura_fila <= 0:
        return 0
    return max(1, int(altura_disponible // altura_fila))
