"""Configuracion del layout y constantes visuales del catalogo."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from reportlab.lib import colors

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOGO_AUTOVENZ = BASE_DIR / "imagenes" / "AUTOVENZ-LOGO.png"
DEFAULT_LOGO_APR = BASE_DIR / "imagenes" / "APR-LOGO.png"


@dataclass
class LayoutConfig:
    """Ajustes de layout y estilos usados en el catalogo PDF."""

    margen_x: float = 42
    margen_y: float = 40
    altura_encabezado: float = 95 #112
    separacion_encabezado: float = 26
    logo_autovenz: Optional[Path] = DEFAULT_LOGO_AUTOVENZ
    logo_apr: Optional[Path] = DEFAULT_LOGO_APR
    alto_max_logo_encabezado: float = 72
    offset_logo_autovenz: float = -30 # Ajuste fino de posicion horizontal
    offset_logo_apr: float = 30    # Ajuste fino de posicion horizontal
    alto_logo_autovenz: float = 54 # Altura deseada del logo en el encabezado
    alto_logo_apr: float = 120 # Altura deseada del logo en el encabezado
    titulo_encabezado: str = "CATALOGO DE PRODUCTOS" # Texto del encabezado
    altura_banner_categoria: float = 40 # Altura del banner de categoria
    columnas: int = 4       # Numero de columnas en el catalogo
    separacion_columnas: float = 18 # Espacio entre columnas     
    separacion_filas: float = 18 # Espacio entre filas
    altura_minima_tarjeta: float = 110 # Altura minima de cada tarjeta
    relleno_tarjeta: float = 10 # Relleno interno de cada tarjeta
    tamano_respaldo_icono: float = 34 # Tamano del respaldo del icono
    grosor_divisor: float = 0.6 # Grosor de la linea divisoria
    fuente_encabezado: str = "Helvetica-Bold" #Fuente del encabezado
    fuente_subtitulo: str = "Helvetica" # Fuente de los titulos
    fuente_cuerpo: str = "Helvetica"    # Fuente del texto normal
    tamano_marca_encabezado: int = 26 # Tamano del texto del encabezado
    tamano_eslogan_encabezado: int = 12 # Tamano del eslogan del encabezado
    tamano_etiqueta_categoria: int = 11 # Tamano del texto de la categoria
    tamano_titulo_categoria: int = 22 # Tamano del titulo de la categoria
    tamano_nombre_producto: int = 11 # Tamano del nombre del producto
    tamano_precio: int = 10 # Tamano del precio
    tamano_meta: int = 8 # Tamano del texto de la meta informacion
    tamano_descripcion: int = 8 # Tamano del texto de la descripcion
    interlineado_descripcion: int = 2 # Espacio entre lineas de la descripcion
    max_lineas_descripcion: int = 3 # Maximo numero de lineas en la descripcion
    color_primario: colors.Color = field(default_factory=lambda: colors.HexColor("#9B59B6"))
    color_secundario: colors.Color = field(default_factory=lambda: colors.HexColor("#F4D03F"))
    color_texto_cuerpo: colors.Color = field(default_factory=lambda: colors.HexColor("#2C3E50"))
    color_texto_tenue: colors.Color = field(default_factory=lambda: colors.HexColor("#56606B"))
    color_fondo_encabezado: colors.Color = field(default_factory=lambda: colors.HexColor("#111213"))
    color_fondo_categoria: colors.Color = field(default_factory=lambda: colors.HexColor("#F4F6FB"))
    color_divisor_tarjeta: colors.Color = field(default_factory=lambda: colors.HexColor("#E1E5ED"))
    color_respaldo_icono: colors.Color = field(default_factory=lambda: colors.HexColor("#2C3E50"))
    ruta_montserrat_regular: Optional[str] = None
    ruta_montserrat_negrita: Optional[str] = None


DEFAULT_LAYOUT = LayoutConfig()
