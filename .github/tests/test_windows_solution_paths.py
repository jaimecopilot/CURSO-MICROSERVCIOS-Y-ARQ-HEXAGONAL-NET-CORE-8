import importlib.util
import tempfile
import unittest
from pathlib import Path, PureWindowsPath
from unittest.mock import patch

class FakeWindowsProject:
    def relative_to(self, stage):
        return PureWindowsPath('src/AceriaApp.Api/AceriaApp.Api.csproj')

class WindowsSolutionTests(unittest.TestCase):
    def test_proyectos_windows_se_reconocen_en_listado_normalizado(self):
        for module in [4,5]:
            with self.subTest(module=module), tempfile.TemporaryDirectory() as temp:
                script=Path(__file__).resolve().parents[1]/'scripts'/f'm0{module}_e2e_desde_practicas.py'
                spec=importlib.util.spec_from_file_location(f'm{module}',script)
                m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
                stage=Path(temp);(stage/'AceriaApp.sln').write_text('')
                with patch.object(m,'projects',return_value=[FakeWindowsProject()]), patch.object(m,'command',return_value='src\\AceriaApp.Api\\AceriaApp.Api.csproj'):
                    self.assertEqual(m.ensure_solution(stage),1)

if __name__=='__main__':unittest.main()
