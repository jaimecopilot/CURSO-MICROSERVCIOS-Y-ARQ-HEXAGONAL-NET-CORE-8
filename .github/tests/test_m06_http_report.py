"""El informe de Windows debe poder leerse como UTF-8 en el cierre Linux."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location('m06_http_report_test', SCRIPTS / 'm06_http_real.py')
http = importlib.util.module_from_spec(spec)
spec.loader.exec_module(http)

class InformeMultiplataformaTests(unittest.TestCase):
    def test_error_de_windows_se_guarda_en_utf8_independientemente_del_locale(self):
        escribir = Path.write_text
        def locale_windows(path, data, encoding=None, errors=None, newline=None):
            return escribir(path, data, encoding=encoding or 'cp1252', errors=errors, newline=newline)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'M06_COMUNICACION_MICROSERVICIOS').mkdir()
            with patch.object(http, 'ROOT', root), patch.object(http, 'source_manifest', return_value={}), \
                 patch.object(http.sys, 'argv', ['m06_http_real.py', '--windows']), \
                 patch.object(http.sys, 'platform', 'win32'), \
                 patch.object(http.tempfile, 'TemporaryDirectory', side_effect=RuntimeError('Conexión interrumpida después del arranque')), \
                 patch.object(Path, 'write_text', locale_windows), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(1, http.main())
            data = (root / 'M06_COMUNICACION_MICROSERVICIOS/M06_WINDOWS_RESULTADOS.json').read_bytes()
            report = json.loads(data.decode('utf-8'))
            self.assertEqual('FAIL', report['resultado'])
            self.assertEqual('Conexión interrumpida después del arranque', report['error'])

if __name__ == '__main__':
    unittest.main()
