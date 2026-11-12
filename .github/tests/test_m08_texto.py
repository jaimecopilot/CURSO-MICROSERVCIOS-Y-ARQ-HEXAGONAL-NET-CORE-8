"""Regresiones de citas de código Markdown que también contienen backticks."""
import importlib.util
from pathlib import Path
import unittest


class CitasM08Tests(unittest.TestCase):
    def module(self):
        path = Path(__file__).resolve().parents[1] / 'scripts/m08_texto.py'
        spec = importlib.util.spec_from_file_location('m08_texto_test', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_cita_de_markdown_con_codigo_interno_conserva_toda_la_linea(self):
        parse = self.module().parse_explanation
        self.assertEqual(parse('- **Línea 3:** `` Ejecuta `dotnet test` aquí. `` Explicación.'),
                         (3, 'Ejecuta `dotnet test` aquí.'))

    def test_cita_de_fence_interno_no_se_confunde_con_delimitador(self):
        parse = self.module().parse_explanation
        self.assertEqual(parse('- **Línea 7:** ```` ```csharp ```` Explicación.'), (7, '```csharp'))

    def test_distingue_linea_vacia_y_cita_simple(self):
        parse = self.module().parse_explanation
        self.assertEqual(parse('- **Línea 1:** (línea vacía) Separa.'), (1, ''))
        self.assertEqual(parse('- **Línea 2:** `var x = 1;` Declara.'), (2, 'var x = 1;'))
        self.assertIsNone(parse('Texto sin explicación numerada.'))

    def test_explicacion_marcada_sin_cita_verificable_se_rechaza(self):
        parse = self.module().parse_explanation
        with self.assertRaises(ValueError):
            parse('- **Línea 1:** Explicación sin cita.')


if __name__ == '__main__':
    unittest.main()
