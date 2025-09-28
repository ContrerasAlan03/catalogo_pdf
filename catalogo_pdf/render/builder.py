"""Orquestador principal del renderizado del catalogo."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from ..config import LayoutConfig
from ..fonts import preparar_fuentes
from ..layout import ancho_columna, posiciones_columnas
from ..model import Catalogo, Categoria, Producto
from .canvas_types import CanvasTipo
from .card import dibujar_tarjeta_producto
from .category import dibujar_categoria_banner
from .header import dibujar_encabezado


class CatalogoRenderizador:
    """Encapsula la logica para componer y exportar el catalogo."""

    def __init__(self, configuracion: LayoutConfig | None = None) -> None:
        self.configuracion = configuracion or LayoutConfig()
        self._pagina_iniciada = False

    def renderizar(self, catalogo: Catalogo, ruta_pdf: str) -> None:
        """Genera un PDF ubicando las categorias y productos en paginas."""
        preparar_fuentes(self.configuracion)
        lienzo = canvas.Canvas(str(Path(ruta_pdf)), pagesize=A4)
        ancho_pagina, alto_pagina = A4
        y_cursor = self._iniciar_pagina(lienzo, alto_pagina)
        columnas_x = posiciones_columnas(self.configuracion, ancho_pagina)
        ancho_col = ancho_columna(self.configuracion, ancho_pagina)

        for categoria in catalogo.categorias:
            y_cursor = self._renderizar_categoria(
                lienzo,
                categoria,
                ancho_pagina,
                alto_pagina,
                y_cursor,
                columnas_x,
                ancho_col,
            )

        lienzo.save()

    # ------------------------------------------------------------------
    def _iniciar_pagina(self, lienzo: CanvasTipo, alto_pagina: float) -> float:
        if self._pagina_iniciada:
            lienzo.showPage()
        else:
            self._pagina_iniciada = True
        dibujar_encabezado(lienzo, self.configuracion)
        return alto_pagina - self.configuracion.margen_y - self.configuracion.altura_encabezado - self.configuracion.separacion_encabezado

    def _renderizar_categoria(
        self,
        lienzo: CanvasTipo,
        categoria: Categoria,
        ancho_pagina: float,
        alto_pagina: float,
        y_cursor: float,
        columnas_x: list[float],
        ancho_col: float,
    ) -> float:
        configuracion = self.configuracion
        icono = categoria.icono_predeterminado
        altura_requerida = configuracion.altura_banner_categoria + configuracion.altura_minima_tarjeta + configuracion.separacion_filas

        if y_cursor - altura_requerida < configuracion.margen_y:
            y_cursor = self._iniciar_pagina(lienzo, alto_pagina)

        y_cursor = dibujar_categoria_banner(lienzo, configuracion, categoria.nombre, y_cursor, icono)
        y_cursor -= configuracion.separacion_filas / 2

        fila_superior = y_cursor
        columna_actual = 0

        for indice_producto, producto in enumerate(categoria.productos):
            if columna_actual == 0 and fila_superior - configuracion.altura_minima_tarjeta < configuracion.margen_y:
                y_cursor = self._iniciar_pagina(lienzo, alto_pagina)
                etiqueta = f"{categoria.nombre} (CONT.)"
                y_cursor = dibujar_categoria_banner(lienzo, configuracion, etiqueta, y_cursor, icono)
                y_cursor -= configuracion.separacion_filas / 2
                fila_superior = y_cursor

            x_izquierda = columnas_x[columna_actual]
            dibujar_tarjeta_producto(
                lienzo,
                configuracion,
                producto,
                x_izquierda=x_izquierda,
                y_superior=fila_superior,
                ancho=ancho_col,
                alto=configuracion.altura_minima_tarjeta,
            )

            if columna_actual == configuracion.columnas - 1:
                columna_actual = 0
                fila_superior -= configuracion.altura_minima_tarjeta + configuracion.separacion_filas
            else:
                columna_actual += 1

        if columna_actual == 0:
            y_cursor = fila_superior
        else:
            y_cursor = fila_superior - configuracion.altura_minima_tarjeta - configuracion.separacion_filas

        return y_cursor
