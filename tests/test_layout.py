import unittest

from catalogo_pdf.config import LayoutConfig
from catalogo_pdf.layout import ancho_columna, filas_por_pagina


class LayoutTests(unittest.TestCase):
    def test_ancho_columna_es_positivo(self) -> None:
        configuracion = LayoutConfig()
        resultado = ancho_columna(configuracion, ancho_pagina=595)
        self.assertGreater(resultado, 0)

    def test_filas_por_pagina_estima_valor_entero(self) -> None:
        configuracion = LayoutConfig()
        filas = filas_por_pagina(configuracion, alto_pagina=842)
        self.assertGreaterEqual(filas, 1)


if __name__ == "__main__":
    unittest.main()
