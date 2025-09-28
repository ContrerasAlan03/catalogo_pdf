"""Funciones de entrada/salida para cargar datos externos."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Sequence

from .model import Catalogo, Producto


def cargar_productos_desde_json(ruta: str | Path) -> Sequence[Producto]:
    """Lee una lista de productos desde un archivo JSON."""
    ruta = Path(ruta)
    contenido = json.loads(ruta.read_text(encoding="utf-8"))
    if not isinstance(contenido, list):
        raise ValueError("El archivo JSON debe contener una lista de productos")
    return [Producto.desde_mapeo(elemento) for elemento in contenido]


def cargar_productos_desde_csv(ruta: str | Path) -> Sequence[Producto]:
    """Lee productos desde un CSV con cabeceras."""
    ruta = Path(ruta)
    with ruta.open(encoding="utf-8", newline="") as manejador:
        lector = csv.DictReader(manejador)
        return [Producto.desde_mapeo(fila) for fila in lector]


def catalogo_desde_fuente(ruta: str | Path) -> Catalogo:
    """Detecta la extension y construye un catalogo listo para renderear."""
    ruta = Path(ruta)
    extension = ruta.suffix.lower()
    if extension == ".json":
        productos = cargar_productos_desde_json(ruta)
    elif extension == ".csv":
        productos = cargar_productos_desde_csv(ruta)
    else:
        raise ValueError(f"Formato de archivo no soportado: {extension}")
    return Catalogo.desde_productos(productos)
