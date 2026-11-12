"""El manual M08 es una entrada verificable, no una declaración de pruebas."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / '.github/scripts/m08_e2e_desde_practicas.py'
sys.path.insert(0, str(SCRIPT.parent))


class ReconstruccionM08Tests(unittest.TestCase):
    def module(self):
        self.assertTrue(SCRIPT.is_file(), 'Falta el reconstructor de M08 desde las prácticas')
        spec = importlib.util.spec_from_file_location('m08_e2e_test', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_rechaza_rutas_fuera_del_directorio_de_la_etapa(self):
        module = self.module()
        for path in ('../previo.txt', '/tmp/ajeno.txt', 'C:/ajeno.txt', 'a\\b.txt', '.', ''):
            with self.subTest(path=path), self.assertRaises(module.LabError):
                module._relative_path(path)

    def test_crear_no_sobrescribe_un_archivo_existente(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            stage = Path(temporary)
            (stage / 'archivo.txt').write_text('preservar', encoding='utf-8')
            with self.assertRaises(module.LabError):
                module.apply_one(stage, {'ruta': 'archivo.txt', 'modo': 'crear', 'codigo': 'otra cosa'})
            self.assertEqual((stage / 'archivo.txt').read_text(), 'preservar')

    def test_reemplazar_exige_que_el_archivo_exista(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(module.LabError):
                module.apply_one(Path(temporary), {'ruta': 'ausente.txt', 'modo': 'reemplazar', 'codigo': 'x'})

    def test_manual_truncado_se_rechaza_antes_de_crear_etapas(self):
        module = self.module()
        with self.assertRaises(module.LabError):
            module.parse_markdown('# Manual incompleto\n### PASO 8.1.1 — Empezar\n')

    def test_un_listado_no_puede_crear_pasos_editoriales_falsos(self):
        module = self.module()
        text = '```markdown\n### PASO 8.1.1 — No es un paso\n```\n'
        self.assertNotIn('PASO', module._markdown_exterior(text))

    def test_una_explicacion_no_puede_citar_otra_linea(self):
        module = self.module()
        with self.assertRaises(module.LabError):
            module._markdown_exterior('```csharp\nvar x = 1;\n```\n- **Línea 1:** `var x = 2;` Explicación.\n')

    def test_el_proveedor_heredado_sigue_siendo_sql_server(self):
        module = self.module()
        relational = module.verify_sql_server(module.M07)
        self.assertGreater(len(relational), 0)

    def test_rechaza_un_informe_dentro_de_la_base_sin_modificarla(self):
        module = self.module()
        destination = module.M07 / 'no-escribir-informe-m08.json'
        self.assertFalse(destination.exists())
        self.assertEqual(module.main(['--no-tests', '--out', str(destination)]), 1)
        self.assertFalse(destination.exists())


if __name__ == '__main__':
    unittest.main()
