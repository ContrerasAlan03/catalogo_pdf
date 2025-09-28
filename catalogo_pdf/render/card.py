"""Componentes para dibujar tarjetas individuales de producto."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from reportlab.lib import colors
from reportlab.lib.utils import ImageReader, simpleSplit

from ..config import LayoutConfig
from ..model import Producto
from .canvas_types import CanvasTipo


def _dibujar_icono(
    lienzo: CanvasTipo,
    ruta_icono: Optional[str],
    *,
    x: float,
    y: float,
    tamano: float,
    color_respaldo: colors.Color,
) -> None:
    """Inserta un icono existente o dibuja un circulo de respaldo con texto."""
    lienzo.saveState()
    lienzo.setFillColor(color_respaldo)
    lienzo.circle(x + tamano / 2, y + tamano / 2, tamano / 2, stroke=0, fill=1)

    if ruta_icono:
        ruta_archivo = Path(ruta_icono)
        if ruta_archivo.is_file():
            imagen = ImageReader(str(ruta_archivo))
            ancho_imagen, alto_imagen = imagen.getSize()
            relacion = min(tamano / ancho_imagen, tamano / alto_imagen)
            ancho_dibujo = ancho_imagen * relacion
            alto_dibujo = alto_imagen * relacion
            posicion_x = x + (tamano - ancho_dibujo) / 2
            posicion_y = y + (tamano - alto_dibujo) / 2
            lienzo.drawImage(
                str(ruta_archivo),
                posicion_x,
                posicion_y,
                width=ancho_dibujo,
                height=alto_dibujo,
                preserveAspectRatio=True,
                mask="auto",
            )
            lienzo.restoreState()
            return

    texto = "NO PHOTO"
    tamano_fuente = max(6, tamano * 0.32)
    lienzo.setFillColor(colors.white)
    lienzo.setFont("Helvetica-Bold", tamano_fuente)
    lienzo.drawCentredString(x + tamano / 2, y + tamano / 2 - tamano_fuente / 3, texto)
    lienzo.restoreState()


def dibujar_tarjeta_producto(
    lienzo: CanvasTipo,
    configuracion: LayoutConfig,
    producto: Producto,
    *,
    x_izquierda: float,
    y_superior: float,
    ancho: float,
    alto: float,
) -> None:
    """Dibuja los datos principales de un producto dentro de una tarjeta."""
    lienzo.saveState()
    relleno = configuracion.relleno_tarjeta
    texto_x = x_izquierda + relleno
    ancho_texto = ancho - 2 * relleno
    y_actual = y_superior - relleno

    tamano_icono = configuracion.tamano_respaldo_icono
    y_icono = y_actual - tamano_icono
    ruta_icono = producto.icono or producto.imagen
    _dibujar_icono(
        lienzo,
        ruta_icono,
        x=texto_x,
        y=y_icono,
        tamano=tamano_icono,
        color_respaldo=configuracion.color_respaldo_icono,
    )
    y_actual = y_icono - relleno * 0.8

    lienzo.setFont(configuracion.fuente_encabezado, configuracion.tamano_nombre_producto)
    lienzo.setFillColor(configuracion.color_texto_cuerpo)
    lineas_nombre = simpleSplit(
        producto.nombre,
        configuracion.fuente_encabezado,
        configuracion.tamano_nombre_producto,
        ancho_texto,
    )
    for linea in lineas_nombre:
        y_actual -= configuracion.tamano_nombre_producto
        lienzo.drawString(texto_x, y_actual, linea)
        y_actual -= 2

    if producto.precio:
        lienzo.setFont(configuracion.fuente_encabezado, configuracion.tamano_precio)
        lienzo.setFillColor(configuracion.color_secundario)
        y_actual -= configuracion.tamano_precio
        lienzo.drawString(texto_x, y_actual, producto.precio)
        y_actual -= 4

    metadatos = []
    if producto.oem:
        metadatos.append(f"OEM: {producto.oem}")
    if producto.referencia:
        metadatos.append(f"Ref: {producto.referencia}")

    if metadatos:
        lienzo.setFont(configuracion.fuente_subtitulo, configuracion.tamano_meta)
        lienzo.setFillColor(configuracion.color_texto_tenue)
        for dato in metadatos:
            y_actual -= configuracion.tamano_meta
            lienzo.drawString(texto_x, y_actual, dato)
            y_actual -= 2

    descripcion = producto.descripcion.strip()
    if descripcion:
        lienzo.setFont(configuracion.fuente_cuerpo, configuracion.tamano_descripcion)
        lienzo.setFillColor(configuracion.color_texto_cuerpo)
        lineas_descripcion = simpleSplit(
            descripcion,
            configuracion.fuente_cuerpo,
            configuracion.tamano_descripcion,
            ancho_texto,
        )
        lineas_limitadas = lineas_descripcion[: configuracion.max_lineas_descripcion]
        for linea in lineas_limitadas:
            y_actual -= configuracion.tamano_descripcion
            lienzo.drawString(texto_x, y_actual, linea)
            y_actual -= configuracion.interlineado_descripcion

    y_divisor = y_superior - alto
    lienzo.setStrokeColor(configuracion.color_divisor_tarjeta)
    lienzo.setLineWidth(configuracion.grosor_divisor)
    lienzo.line(x_izquierda, y_divisor, x_izquierda + ancho, y_divisor)
    lienzo.restoreState()
