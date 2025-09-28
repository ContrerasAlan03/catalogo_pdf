import unittest

from catalogo_pdf.cli import parsear_argumentos


class CliTests(unittest.TestCase):
    def test_parsear_argumentos_por_defecto(self) -> None:
        args = parsear_argumentos([])
        self.assertEqual(args.output, "catalogo.pdf")

    def test_parsear_argumentos_personalizados(self) -> None:
        args = parsear_argumentos(["--input", "productos.json", "--output", "salida.pdf"])
        self.assertEqual(args.input, "productos.json")
        self.assertEqual(args.output, "salida.pdf")


if __name__ == "__main__":
    unittest.main()
