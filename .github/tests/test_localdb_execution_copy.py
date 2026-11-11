import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('localdb_http',SCRIPTS/'comprobar_localdb_http.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ExecutionCopyTests(unittest.TestCase):
    def test_copia_corta_conserva_codigo_y_no_reutiliza_binarios(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'nombre-de-repositorio-muy-largo'/'etapa';target=root/'corta'
            (source/'src/Api/bin').mkdir(parents=True)
            (source/'src/Api/Program.cs').write_text('class Program {}\n')
            (source/'src/Api/bin/obsoleto.dll').write_text('anterior')
            actual=m.prepare_execution_stage(source,target)
            self.assertEqual(actual,target)
            self.assertEqual(m.source_manifest(actual),m.source_manifest(source))
            self.assertFalse((actual/'src/Api/bin').exists())
if __name__=='__main__':unittest.main()
