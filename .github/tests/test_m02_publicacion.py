"""La publicación de M02 debe reflejar exactamente el código reconstruido."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/e2e_laboratorio_m02.py"
SPEC = importlib.util.spec_from_file_location("e2e_laboratorio_m02", SCRIPT)
M02 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M02)


class PublicacionM02Tests(unittest.TestCase):
    def test_reemplaza_codigo_y_configuracion_obsoletos_conservando_solo_readme(self):
        with tempfile.TemporaryDirectory(prefix="m02-publicacion-test-") as folder:
            root = Path(folder)
            source = root / "reconstruido"
            destination = root / "publicado"
            generated = {
                "src/AceriaApp.Api/Program.cs": "// Código reconstruido desde el manual.\n",
                "src/AceriaApp.Api/AceriaApp.Api.csproj": "<Project />\n",
                "src/AceriaApp.Api/appsettings.json": '{"ConnectionStrings":{}}\n',
                "tests/Compartido/SqlServerPruebas.cs": "// Helper reconstruido.\n",
            }
            stale = {
                "src/AceriaApp.Api/Obsoleto.cs": "// No reconstruido ni ejecutado.\n",
                "tests/PruebasViejas/PruebasViejas.csproj": "<Project />\n",
                "src/AceriaApp.Api/appsettings.Development.json": '{"Obsoleto":true}\n',
                "Directory.Build.targets": "<Project />\n",
                "docs/NoEsDocumentacion.cs": "// Tampoco debe conservarse.\n",
                "src/AceriaApp.Api/obj/Anterior.cs": "// Artefacto anterior.\n",
            }
            for relative, content in generated.items():
                M02.write(source, Path(relative), content)
            for relative, content in stale.items():
                M02.write(destination, Path(relative), content)
            M02.write(destination, Path("src/AceriaApp.Api/Program.cs"), "// Versión anterior.\n")
            readme = "# Guía editorial de la etapa\n"
            M02.write(destination, Path("README.md"), readme)
            # Los resultados intermedios del build tampoco forman parte de la publicación.
            M02.write(source, Path("src/AceriaApp.Api/bin/Release/temporal.dll"), "temporal")
            M02.write(source, Path("src/AceriaApp.Api/obj/generado.cs"), "temporal")

            M02.publish(source, destination)

            self.assertFalse((destination / "src/AceriaApp.Api/Obsoleto.cs").exists())
            actual = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
            self.assertEqual(actual, set(generated) | {"README.md"})
            for relative, content in generated.items():
                self.assertEqual((destination / relative).read_text(), content)
            self.assertEqual((destination / "README.md").read_text(), readme)

            # Publicar otra vez no cambia ni agrega archivos.
            M02.publish(source, destination)
            repeated = {path.relative_to(destination).as_posix() for path in destination.rglob("*") if path.is_file()}
            self.assertEqual(repeated, actual)


if __name__ == "__main__":
    unittest.main()
