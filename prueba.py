"""Script de apoyo que genera un catalogo de demostracion."""

from catalogo_pdf.cli import construir_catalogo_demo
from catalogo_pdf.render.builder import CatalogoRenderizador


if __name__ == "__main__":
    catalogo = construir_catalogo_demo()
    renderizador = CatalogoRenderizador()
    renderizador.renderizar(catalogo, "catalogo_demo.pdf")
    print("Plantilla de catalogo generada en catalogo_demo.pdf")
