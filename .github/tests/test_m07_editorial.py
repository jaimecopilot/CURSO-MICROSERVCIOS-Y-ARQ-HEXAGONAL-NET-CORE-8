"""Regresiones de la limpieza editorial M07: los ejemplos ejecutables son inmutables."""
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANUAL = ROOT / "M07_OBSERVABILIDAD_RESILIENCIA/PRACTICAS/M07_PRACTICAS.md"
GOLDEN_SHA1 = "ad6fd926a43501ed5fd03b6668c63965d7a20ec1"


class AuditoriaM07(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = MANUAL.read_text(encoding="utf-8")

    def test_contrato_codigo_marcadores_inalterado(self):
        source = self.content
        code = re.findall(r"^```[^\n]*\n[\s\S]*?^```$", source, re.M)
        marks = re.findall(r"<!-- M07_(?:CODIGO|RETO) [^\n]* -->", source)
        self.assertEqual(len(code), 137)
        self.assertEqual(len(marks), 105)
        data = ("\x00".join(code) + "\x00MARKERS\x00" + "\x00".join(marks)).encode("utf-8")
        digest = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
        self.assertEqual(digest, GOLDEN_SHA1)

    def test_pasosenorden(self):
        expected = [f"7.{i}.{j}" for i in range(1, 5) for j in range(1, 25)]
        current = re.findall(r"^### PASO (7\.[1-4]\.\d+) —", self.content, re.M)
        self.assertEqual(current, expected)

    def test_comentarios_selectivos(self):
        notes = re.findall(r"^- \*\*Línea \d+:\*\*", self.content, re.M)
        self.assertLess(len(notes), 400)
        self.assertGreater(len(notes), 100)
        self.assertNotIn("**Lectura del código.** Los números cuentan", self.content)
        self.assertNotIn("**Lectura de las líneas clave.**", self.content)


if __name__ == "__main__":
    unittest.main()
