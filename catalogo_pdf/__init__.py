"""Utilidades para generar catalogos PDF de productos automotrices."""

from .config import LayoutConfig
from .model import Catalogo, Categoria, Producto
from .render.builder import CatalogoRenderizador

__all__ = [
    "LayoutConfig",
    "Producto",
    "Categoria",
    "Catalogo",
    "CatalogoRenderizador",
]
