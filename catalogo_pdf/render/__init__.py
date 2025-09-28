"""Submodulo que contiene las rutinas de dibujo para el catalogo."""

from .card import _dibujar_icono, dibujar_tarjeta_producto
from .category import dibujar_categoria_banner
from .header import dibujar_encabezado

__all__ = [
    "dibujar_encabezado",
    "dibujar_categoria_banner",
    "dibujar_tarjeta_producto",
    "_dibujar_icono",
]
