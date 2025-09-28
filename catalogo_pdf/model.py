"""Modelos de datos de alto nivel para el catalogo."""

from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence


@dataclass
class Producto:
    """Producto que aparecera en una tarjeta del catalogo."""

    categoria: str = "General"
    nombre: str = "Producto"
    precio: str | None = None
    oem: str | None = None
    referencia: str | None = None
    descripcion: str = ""
    icono: str | None = None
    icono_categoria: str | None = None
    imagen: str | None = None
    extras: Mapping[str, str] = field(default_factory=dict)

    @classmethod
    def desde_mapeo(cls, datos: Mapping[str, str]) -> "Producto":
        """Crea un producto normalizando claves comunes provenientes de CSV/JSON."""
        extras = {
            clave: valor
            for clave, valor in datos.items()
            if clave
            not in {
                "categoria",
                "nombre",
                "precio",
                "oem",
                "referencia",
                "descripcion",
                "icono",
                "icono_categoria",
                "imagen",
            }
        }
        return cls(
            categoria=str(datos.get("categoria") or "General"),
            nombre=str(datos.get("nombre") or "Producto"),
            precio=datos.get("precio") or None,
            oem=datos.get("oem") or None,
            referencia=datos.get("referencia") or None,
            descripcion=str(datos.get("descripcion") or ""),
            icono=datos.get("icono") or None,
            icono_categoria=datos.get("icono_categoria") or None,
            imagen=datos.get("imagen") or None,
            extras=extras,
        )


@dataclass
class Categoria:
    """Agrupacion de productos que comparten un nombre y opcionalmente un icono."""

    nombre: str
    productos: Sequence[Producto]

    @property
    def icono_predeterminado(self) -> str | None:
        for producto in self.productos:
            if producto.icono_categoria:
                return producto.icono_categoria
            if producto.icono:
                return producto.icono
        return None


@dataclass
class Catalogo:
    """Coleccion ordenada de categorias lista para ser rendereada."""

    categorias: Sequence[Categoria]

    @classmethod
    def desde_productos(cls, iterable: Iterable[Mapping[str, str]]) -> "Catalogo":
        """Genera el catalogo agrupando por categoria y preservando el orden de entrada."""
        agrupados: "OrderedDict[str, list[Producto]]" = OrderedDict()
        for datos in iterable:
            producto = Producto.desde_mapeo(datos)
            agrupados.setdefault(producto.categoria, []).append(producto)

        categorias = [Categoria(nombre=nombre, productos=tuple(productos)) for nombre, productos in agrupados.items()]
        return cls(categorias=categorias)
