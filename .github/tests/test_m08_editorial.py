"""Regresiones editoriales de M08: protege los archivos de código y la guía ejecutable."""
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANUAL = ROOT / "M08_API_GATEWAY/PRACTICAS/M08_PRACTICAS.md"
GOLDEN_CODE_BLOB_SHA1 = "b4b1a4da0787fd175cf4f6625ce5be6548a7deca"


def bloques_y_marcadores(texto: str) -> tuple[list[str], list[str]]:
    bloques = re.findall(r"^```[^\n]*\n[\s\S]*?^```$", texto, flags=re.M)
    marcadores = re.findall(r"<!-- M08_(?:CODIGO|RETO) [^\n]* -->", texto)
    return bloques, marcadores


def huella_git_del_contrato(texto: str) -> str:
    bloques, marcadores = bloques_y_marcadores(texto)
    datos = ("\x00".join(bloques) + "\x00MARKERS\x00" + "\x00".join(marcadores)).encode("utf-8")
    return hashlib.sha1(f"blob {len(datos)}\0".encode("ascii") + datos).hexdigest()


class AuditoriaEditorialM08(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.texto = MANUAL.read_text(encoding="utf-8")

    def test_codigo_y_marcadores_binariamente_equivalentes_al_original(self):
        """Comprueba que ningún código o marcador del manual original fue alterado."""
        self.assertEqual(huella_git_del_contrato(self.texto), GOLDEN_CODE_BLOB_SHA1)

    def test_etapas_pasos_y_retos_conservados(self):
        self.assertEqual(len(re.findall(r"^### PASO 8\.[1-4]\.\d+ —", self.texto, flags=re.M)), 96)
        self.assertEqual(len(re.findall(r"<!-- M08_CODIGO ", self.texto)), 66)
        self.assertEqual(len(re.findall(r"<!-- M08_RETO ", self.texto)), 12)
        self.assertEqual(len(bloques_y_marcadores(self.texto)[0]), 96)
        for numero in range(1, 5):
            self.assertIn(f"# Punto 8.{numero} —", self.texto)

    def test_lecturas_selectivas_sin_titulares_huerfanos(self):
        self.assertNotIn("Lectura del archivo, línea por línea.", self.texto)
        lineas = self.texto.splitlines()
        for i, linea in enumerate(lineas):
            if linea == "**Lectura selectiva del archivo: decisiones y comprobaciones relevantes.**":
                j = i + 1
                while j < len(lineas) and not lineas[j].strip():
                    j += 1
                self.assertRegex(lineas[j], r"^- \*\*Línea \d+:\*\*")

    def test_evitar_reaparicion_de_relleno_mecanico(self):
        # El contrato principal sigue siendo la equivalencia del código;
        # este umbral impide regresar accidentalmente a miles de glosas triviales.
        explicaciones = re.findall(r"^- \*\*Línea \d+:\*\*", self.texto, flags=re.M)
        self.assertLess(len(explicaciones), 500)
        self.assertGreater(len(explicaciones), 100)


if __name__ == "__main__":
    unittest.main()
