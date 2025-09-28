"""Interfaz de linea de comandos para generar el catalogo."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import LayoutConfig
from .io import catalogo_desde_fuente
from .model import Catalogo
from .render.builder import CatalogoRenderizador

_PRODUCTOS_DEMO = [
    {
        "categoria": "Amortiguadores",
        "nombre": "Amortiguador Delantero Heavy",
        "precio": "129.90 EUR",
        "oem": "CEM-77219",
        "descripcion": "Amortiguador bitubo con gas nitrogeno, disenado para carga elevada y uso en climas frios.",
    },
    {
        "categoria": "Amortiguadores",
        "nombre": "Amortiguador Delantero",
        "precio": "89.90 EUR",
        "oem": "CEM-77217",
        "descripcion": "Amortiguador hidraulico de alta durabilidad para modelos sedanes y crossover.",
    },
    {
        "categoria": "Amortiguadores",
        "nombre": "Amortiguador Trasero",
        "precio": "79.90 EUR",
        "oem": "CEM-77216",
        "descripcion": "Amortiguador de gas calibrado para rendimiento estable en todo terreno.",
    },
    {
        "categoria": "Amortiguadores",
        "nombre": "Amortiguador Deportivo",
        "precio": "159.90 EUR",
        "oem": "CEM-88311",
        "descripcion": "Configuracion deportiva con valvulas de alta respuesta y sellos reforzados.",
    },
    {
        "categoria": "Sistema de Motor",
        "nombre": "Bomba de Agua Ref. A100",
        "precio": "89.99 EUR",
        "oem": "OEM-55821",
        "descripcion": "Carcasa de aluminio reforzado y sello ceramico para alta durabilidad.",
    },
    {
        "categoria": "Sistema de Motor",
        "nombre": "Sensor ABS Rueda Delantera",
        "precio": "42.30 EUR",
        "oem": "OEM-99114",
        "descripcion": "Sensor de velocidad con recubrimiento anticorrosivo y cable mallado.",
    },
    {
        "categoria": "Sistema Electrico",
        "nombre": "Alternador 120A",
        "precio": "239.60 EUR",
        "oem": "OEM-44777",
        "descripcion": "Alternador de 120 amperios con regulador integrado y rotor balanceado.",
    },
    {
        "categoria": "Sistema Electrico",
        "nombre": "Motor de Arranque 9 Dientes",
        "precio": "178.50 EUR",
        "oem": "OEM-22017",
        "descripcion": "Motor de arranque con reduccion planetaria y bobinados tratados al vacio.",
    },

    {
        "categoria": "Sistema Electrico",
        "nombre": "Motor de Arranque 9 Dientes",
        "precio": "178.50 EUR",
        "oem": "OEM-22017",
        "descripcion": "Motor de arranque con reduccion planetaria y bobinados tratados al vacio.",
    },{
        "categoria": "Sistema Electrico",
        "nombre": "Motor de Arranque 9 Dientes",
        "precio": "178.50 EUR",
        "oem": "OEM-22017",
        "descripcion": "Motor de arranque con reduccion planetaria y bobinados tratados al vacio.",
    },{
        "categoria": "Sistema Electrico",
        "nombre": "Motor de Arranque 9 Dientes",
        "precio": "178.50 EUR",
        "oem": "OEM-22017",
        "descripcion": "Motor de arranque con reduccion planetaria y bobinados tratados al vacio.",
    },
]


def construir_catalogo_demo() -> Catalogo:
    """Construye un catalogo de demostracion con datos incluidos."""
    return Catalogo.desde_productos(_PRODUCTOS_DEMO)


def parsear_argumentos(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera un catalogo PDF de productos.")
    parser.add_argument("--input", "-i", help="Archivo JSON o CSV con productos.")
    parser.add_argument("--output", "-o", default="catalogo.pdf", help="Ruta de salida del PDF.")
    parser.add_argument("--montserrat-regular", dest="ruta_montserrat_regular", help="Ruta a la fuente Montserrat Regular.")
    parser.add_argument("--montserrat-negrita", dest="ruta_montserrat_negrita", help="Ruta a la fuente Montserrat Bold.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    argumentos = parsear_argumentos(argv)

    if argumentos.input:
        catalogo = catalogo_desde_fuente(argumentos.input)
    else:
        catalogo = construir_catalogo_demo()

    configuracion = LayoutConfig(
        ruta_montserrat_regular=argumentos.ruta_montserrat_regular,
        ruta_montserrat_negrita=argumentos.ruta_montserrat_negrita,
    )

    renderizador = CatalogoRenderizador(configuracion)
    renderizador.renderizar(catalogo, argumentos.output)

    ruta = Path(argumentos.output)
    print(f"Catalogo generado en {ruta.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
