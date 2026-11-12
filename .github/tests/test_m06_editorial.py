"""Regresión editorial M06: conserva código, retos y construcción paso a paso."""
import hashlib
import re
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[2] / "M06_COMUNICACION_MICROSERVICIOS/PRACTICAS/M06_PRACTICAS.md"
GOLDEN = "9320c00ac908574bf541cf6c25dac7bee08367b5"


class M06Edicion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = FILE.read_text(encoding="utf-8")

    def test_contract_code_markers_golden(self):
        fences = re.findall(r"^```[^\n]*\n[\s\S]*?^```$", self.source, flags=re.M)
        markers = re.findall(r"<!-- M06_(?:CODIGO|RETO) [^\n]* -->", self.source)
        self.assertEqual((len(fences), len(markers)), (114, 101))
        payload = ("\x00".join(fences) + "\x00MARKERS\x00" + "\x00".join(markers)).encode("utf-8")
        sha = hashlib.sha1(f"blob {len(payload)}\0".encode("ascii") + payload).hexdigest()
        self.assertEqual(sha, GOLDEN)

    def test_pasosenorden(self):
        expected = [f"6.{i}.{j}" for i in range(1, 4) for j in range(1, 25)]
        actual = re.findall(r"^### PASO (6\.[1-3]\.\d+) —", self.source, flags=re.M)
        self.assertEqual(actual, expected)

    def test_comentarios_no_repetidos_masivamente(self):
        entries = re.findall(r"^- \*\*Línea \d+:\*\*", self.source, re.M)
        self.assertGreater(len(entries), 100)
        self.assertLess(len(entries), 300)
        self.assertNotIn("**Lectura de las líneas clave.**", self.source)
        self.assertNotIn("**Lectura del código.** Los números cuentan", self.source)


if __name__ == "__main__":
    unittest.main()
