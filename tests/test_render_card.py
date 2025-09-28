import unittest

from reportlab.lib import colors

from catalogo_pdf.render.card import _dibujar_icono


class CanvasFalso:
    def __init__(self) -> None:
        self.textos: list[str] = []

    def saveState(self) -> None:
        pass

    def restoreState(self) -> None:
        pass

    def setFillColor(self, _color) -> None:
        pass

    def circle(self, *_args, **_kwargs) -> None:
        pass

    def setFont(self, *_args, **_kwargs) -> None:
        pass

    def drawCentredString(self, _x: float, _y: float, texto: str) -> None:
        self.textos.append(texto)

    def drawImage(self, *_args, **_kwargs) -> None:
        raise AssertionError("drawImage no deberia invocarse sin icono")


class IconoTests(unittest.TestCase):
    def test_dibujar_icono_sin_archivo_muestra_no_photo(self) -> None:
        lienzo = CanvasFalso()
        _dibujar_icono(
            lienzo,
            ruta_icono=None,
            x=0,
            y=0,
            tamano=40,
            color_respaldo=colors.black,
        )
        self.assertIn("NO PHOTO", lienzo.textos)


if __name__ == "__main__":
    unittest.main()
