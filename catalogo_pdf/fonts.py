"""Funciones relacionadas con el registro de fuentes personalizadas."""

from pathlib import Path
from typing import Optional

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .config import LayoutConfig


def _asegurar_fuente(nombre_fuente: str, ruta_fuente: Optional[str], fuentes_registradas: set[str]) -> bool:
    """Intenta registrar una fuente TrueType y devuelve si quedo disponible."""
    if not ruta_fuente:
        return False

    ruta_archivo = Path(ruta_fuente)
    if not ruta_archivo.is_file():
        return False

    if nombre_fuente in fuentes_registradas:
        return True

    try:
        pdfmetrics.registerFont(TTFont(nombre_fuente, str(ruta_archivo)))
    except Exception:
        return False

    fuentes_registradas.add(nombre_fuente)
    return True


def preparar_fuentes(configuracion: LayoutConfig) -> None:
    """Registra Montserrat si se proporcionan rutas validas."""
    if not (configuracion.ruta_montserrat_regular or configuracion.ruta_montserrat_negrita):
        return

    fuentes_registradas = set(pdfmetrics.getRegisteredFontNames())

    if _asegurar_fuente("Montserrat-Regular", configuracion.ruta_montserrat_regular, fuentes_registradas):
        configuracion.fuente_cuerpo = "Montserrat-Regular"
        configuracion.fuente_subtitulo = "Montserrat-Regular"

    if _asegurar_fuente("Montserrat-Bold", configuracion.ruta_montserrat_negrita, fuentes_registradas):
        configuracion.fuente_encabezado = "Montserrat-Bold"
