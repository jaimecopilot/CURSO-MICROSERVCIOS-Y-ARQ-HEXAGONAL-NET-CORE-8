import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/validar_sqlserver.py'

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('validar_sqlserver', SCRIPT)
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.report = {'resumen': {'resultado': 'PASS', 'tests_por_etapa': [3, 7, 12, 16]},
                       'etapas': [{'resultado': 'PASS', 'tests': n} for n in [3, 7, 12, 16]]}
        self.row = {'provider': 'Microsoft.EntityFrameworkCore.SqlServer', 'engineEdition': 4,
                    'version': '16.0.1', 'database': 'AceriaTest_123',
                    'modo': 'conexion_externa', 'origen': 'Testcontainers'}
    def save(self):
        (self.directory / 'database.json').write_text(json.dumps(self.row))
    def test_pass_sin_conexion_sql_no_acredita_integracion(self):
        with self.assertRaisesRegex(ValueError, 'evidencia SQL'):
            self.m.validate_evidence(self.report, 2, self.directory)
    def test_sqlite_no_se_acepta_aunque_el_resumen_diga_pass(self):
        self.row['provider'] = 'Microsoft.EntityFrameworkCore.Sqlite'
        self.save()
        with self.assertRaisesRegex(ValueError, 'proveedor'):
            self.m.validate_evidence(self.report, 2, self.directory)
    def test_sql_express_con_version_real_acredita_el_motor(self):
        self.save()
        result = self.m.validate_evidence(self.report, 2, self.directory)
        self.assertEqual(result['bases_verificadas'], 1)
        self.assertEqual(result['resultado'], 'PASS')
    def test_etapa_sin_tests_bloquea_el_cierre(self):
        self.save()
        self.report['etapas'][2]['resultado'] = 'SIN_EJECUTAR_TESTS'
        with self.assertRaisesRegex(ValueError, 'etapa'):
            self.m.validate_evidence(self.report, 2, self.directory)
    def test_version_y_edicion_son_obligatorias(self):
        self.save()
        self.row['engineEdition'] = 3
        self.save()
        with self.assertRaisesRegex(ValueError, 'Express'):
            self.m.validate_evidence(self.report, 2, self.directory)
    def test_reto_fallido_no_puede_cerrarse(self):
        self.save()
        self.report['retos_optativos'] = {'resultado': 'FAIL'}
        with self.assertRaisesRegex(ValueError, 'reto'):
            self.m.validate_evidence(self.report, 2, self.directory)

    def test_windows_debe_haber_ejecutado_el_codigo_que_se_publica(self):
        with self.assertRaisesRegex(ValueError, 'Windows'):
            self.m.validate_windows_sources({'src/Program.cs': 'viejo'}, {'etapa/src/Program.cs': 'nuevo'}, 'etapa')
    def test_windows_rechaza_un_archivo_ejecutable_no_comprobado(self):
        with self.assertRaisesRegex(ValueError, 'Windows'):
            self.m.validate_windows_sources({}, {'etapa/src/Program.cs': 'nuevo'}, 'etapa')
    def test_windows_acepta_el_mismo_codigo_reconstruido(self):
        self.m.validate_windows_sources({'src/Program.cs': 'igual'}, {'etapa/src/Program.cs': 'igual'}, 'etapa')

if __name__ == '__main__':
    unittest.main()
