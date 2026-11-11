"""Contrato del reconstructor M06 con manuales pequeños e independientes."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/m06_e2e_desde_practicas.py'
SPEC = importlib.util.spec_from_file_location('m06_e2e_desde_practicas', SCRIPT)
M06 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M06)


def metadata(step, path, mode='crear', *, challenge=False, code='public class Ejemplo { }', kind='csharp', **extra):
    info = {'paso': step, 'ruta': path, 'modo': mode, **extra}
    label = 'M06_RETO' if challenge else 'M06_CODIGO'
    return '<!-- ' + label + ' ' + json.dumps(info) + ' -->\n```' + kind + '\n' + code + '\n```\n'


def manual_fixture():
    """39 operaciones y tres retos: no requiere archivos del curso."""
    pieces = ['# Manual M06\n']
    for point in (1, 2, 3):
        for step in range(1, 25):
            identifier = f'6.{point}.{step}'
            pieces.append(f'### PASO {identifier} — Ejercicio\n\n'
                          '**Procedimiento guiado.**\n\n'
                          '1. Localiza la carpeta.\n2. Crea el archivo.\n'
                          '3. Guarda el archivo.\n4. Revisa su contenido.\n\n')
            if 4 <= step <= 16:
                pieces.append(metadata(identifier, f'docs/p{point}-{step}.cs'))
                if step == 6:
                    pieces.append('- **Línea 1:** `public class Ejemplo { }` → Declara el ejemplo.\n\n')
            pieces.append('**Por qué funciona así.** Explicación.\n\n'
                          '**Verificación concreta.** Comprobación.\n\n')
        pieces.append('## Reto de ampliación (optativo)\n\n')
        for step in (1, 3, 6):
            pieces.append(metadata(f'6.{point}.reto.{step}', f'docs/p{point}-6.cs',
                                   'insertar_antes', challenge=True, ancla='public class Ejemplo',
                                   code=f'// Reto {step}'))
    return ''.join(pieces)


class ParseMarkdownTests(unittest.TestCase):
    def test_extrae_codigo_y_retos_del_manual_completo(self):
        content = manual_fixture()
        actual, codes, challenges = M06.parse_markdown(content)
        self.assertEqual(actual, content)
        self.assertEqual(len(codes), 39)
        self.assertEqual(len(challenges), 9)
        self.assertEqual(codes[0], {'paso': '6.1.4', 'ruta': 'docs/p1-4.cs', 'modo': 'crear',
                                    'tipo': 'csharp', 'codigo': 'public class Ejemplo { }\n'})

    def test_rechaza_un_paso_ausente_o_duplicado(self):
        content = manual_fixture()
        for broken in (content.replace('### PASO 6.2.17 — Ejercicio', '### Otro apartado'),
                       content.replace('### PASO 6.2.17 —', '### PASO 6.2.16 —')):
            with self.subTest(broken=broken[:20]), self.assertRaises(M06.LabError):
                M06.parse_markdown(broken)

    def test_rechaza_metadatos_alterados_que_no_se_pueden_extraer(self):
        for before, after in (('"modo": "crear"', '"modo": "borrar"'),
                              ('"paso": "6.1.4"', '"paso": "6.1.99"'),
                              ('"ruta": "docs/p1-4.cs"', '"ruta": null'),
                              ('```csharp', '```python'),
                              ('"paso": "6.1.4"', '"paso": ')):
            with self.subTest(after=after), self.assertRaises(M06.LabError):
                M06.parse_markdown(manual_fixture().replace(before, after, 1))

    def test_rechaza_rutas_que_salen_de_la_etapa_en_windows_o_linux(self):
        for path in ('../fuera.cs', '/tmp/fuera.cs', r'C:\fuera.cs', r'..\fuera.cs',
                     'src/../../fuera.cs', '.', '', r'\\servidor\fuera.cs'):
            with self.subTest(path=path), self.assertRaises(M06.LabError):
                M06.parse_markdown(manual_fixture().replace('"docs/p1-4.cs"', json.dumps(path), 1))

    def test_rechaza_bloque_identificado_como_otro_paso(self):
        with self.assertRaisesRegex(M06.LabError, 'fuera de su paso'):
            M06.parse_markdown(manual_fixture().replace('"paso": "6.1.4"', '"paso": "6.1.5"', 1))

    def test_rechaza_cuatro_acciones_que_no_estan_numeradas_en_orden(self):
        with self.assertRaises(M06.LabError):
            M06.parse_markdown(manual_fixture().replace('3. Guarda el archivo.', '4. Guarda el archivo.', 1))

    def test_rechaza_una_quinta_accion(self):
        with self.assertRaises(M06.LabError):
            M06.parse_markdown(manual_fixture().replace('4. Revisa su contenido.\n', '4. Revisa su contenido.\n5. Repite.\n', 1))

    def test_rechaza_explicacion_que_cita_otra_linea(self):
        with self.assertRaisesRegex(M06.LabError, 'desalineada'):
            M06.parse_markdown(manual_fixture().replace('**Línea 1:** `public class Ejemplo { }`',
                                                       '**Línea 2:** `public class Ejemplo { }`', 1))

    def test_cuenta_lineas_vacias_y_rechaza_una_linea_vacia_falsa(self):
        content = manual_fixture().replace('public class Ejemplo { }\n```',
                                           '\npublic class Ejemplo { }\n```\n- **Línea 1:** (línea vacía) → Separa.', 1)
        M06.parse_markdown(content)
        with self.assertRaisesRegex(M06.LabError, 'desalineada'):
            M06.parse_markdown(content.replace('**Línea 1:** (línea vacía)', '**Línea 2:** (línea vacía)', 1))

    def test_rechaza_retos_duplicados_aunque_haya_nueve_fragmentos(self):
        with self.assertRaises(M06.LabError):
            M06.parse_markdown(manual_fixture().replace('"paso": "6.2.reto.6"', '"paso": "6.2.reto.3"', 1))

    def test_rechaza_insercion_sin_ancla(self):
        with self.assertRaises(M06.LabError):
            M06.parse_markdown(manual_fixture().replace(', "ancla": "public class Ejemplo"', '', 1))

    def test_no_confunde_un_encabezado_dentro_del_codigo_con_un_paso(self):
        content = manual_fixture().replace('```csharp\npublic class Ejemplo { }\n```',
                                          '```markdown\n### PASO 6.9.99 — Ilustración\n```', 1)
        _, codes, _ = M06.parse_markdown(content)
        self.assertEqual(len(codes), 39)
        self.assertEqual(codes[0]['codigo'], '### PASO 6.9.99 — Ilustración\n')


def write(root, path, content):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding='utf-8')
    return target


def sql_fixture(root):
    write(root, 'tests/Compartido/SqlServerPruebas.cs', 'public class BaseSqlServer { }')
    write(root, 'tests/Base0/Base0.csproj', '<Project><ItemGroup>'
          '<Compile Include="../Compartido/SqlServerPruebas.cs" />'
          '<PackageReference Include="Testcontainers.MsSql" Version="3.10.0" />'
          '</ItemGroup></Project>')
    write(root, 'tests/Base0/PersistenciaTests.cs', 'var bd = BaseSqlServer.Crear();')
    write(root, 'tests/Base1/Base1.csproj', '<Project />')
    write(root, 'tests/Base1/DominioTests.cs', '[Fact] public void Regla() { }')


def fake_dotnet(*args, cwd, **kwargs):
    """Solo el proceso externo se sustituye; se conserva el estado de la solución."""
    solution = cwd / 'AceriaApp.sln'
    if args[:3] == ('dotnet', 'new', 'sln'):
        solution.write_text('')
        return ''
    if args[:4] == ('dotnet', 'sln', 'AceriaApp.sln', 'add'):
        paths = set(solution.read_text().splitlines()) | set(args[4:])
        solution.write_text('\n'.join(sorted(paths)) + '\n')
        return ''
    if args == ('dotnet', 'sln', 'AceriaApp.sln', 'list'):
        return solution.read_text()
    raise AssertionError('Un modo sin pruebas no puede ejecutar ' + repr(args))


def dry_run_fixture(root):
    base = root / 'M05_DDD_CQRS/PROYECTO/5.5-dominio-aceria'
    sql_fixture(base)
    for number in range(2, 15):
        write(base, f'tests/Base{number}/Base{number}.csproj', '<Project />')
    for number in range(7):
        write(base, f'src/Base{number}/Base{number}.csproj', '<Project />')
    for number in range(28):
        write(base, f'docs/base{number}.md', f'Documento {number}\n')
    write(base, 'AceriaApp.sln', '')
    content = manual_fixture()
    for point in (1, 2, 3):
        content = content.replace(f'docs/p{point}-', f'src/notes/p{point}-')
        test_name = ['ComunicacionSincrona', 'ComunicacionAsincrona', 'Decisiones'][point-1]
        additions = metadata(f'6.{point}.5', f'tests/AceriaApp.{test_name}.Tests/AceriaApp.{test_name}.Tests.csproj',
                             code='<Project />', kind='xml')
        if point == 1:
            for name in ('Contratos', 'Aplicacion', 'Infraestructura', 'Inventario'):
                additions += metadata('6.1.5', f'src/Nuevo{name}/Nuevo{name}.csproj', code='<Project />', kind='xml')
        content = content.replace(metadata(f'6.{point}.5', f'src/notes/p{point}-5.cs'),
                                  metadata(f'6.{point}.5', f'src/notes/p{point}-5.cs') + additions)
    manual = write(root, 'M06_COMUNICACION_MICROSERVICIOS/PRACTICAS/M06_PRACTICAS.md', content)
    return base, manual


class RuntimeTests(unittest.TestCase):
    def test_anade_todos_los_proyectos_a_la_solucion_en_una_operacion(self):
        with tempfile.TemporaryDirectory() as folder:
            stage = Path(folder)
            for name in ('Uno', 'Dos', 'Tres'):
                write(stage, f'src/{name}/{name}.csproj', '<Project />')
            write(stage, 'src/Uno/obj/NoEsProyecto.csproj', '<Project />')
            with patch.object(M06, 'command', side_effect=fake_dotnet) as process:
                self.assertEqual(M06.ensure_solution(stage), 3)
            self.assertEqual(len((stage / 'AceriaApp.sln').read_text().splitlines()), 3)
            additions = [call for call in process.call_args_list if call.args[:4] ==
                         ('dotnet', 'sln', 'AceriaApp.sln', 'add')]
            self.assertEqual(len(additions), 1)
            self.assertEqual(set(additions[0].args[4:]),
                             {'src/Uno/Uno.csproj', 'src/Dos/Dos.csproj', 'src/Tres/Tres.csproj'})

    def test_una_insercion_exige_ancla_unica_y_no_puede_escribir_por_un_symlink(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            stage = root / 'stage'
            stage.mkdir()
            write(stage, 'src/Ejemplo.cs', 'ancla ancla')
            data = {'ruta': 'src/Ejemplo.cs', 'modo': 'insertar_antes', 'ancla': 'ancla', 'codigo': '// nuevo\n'}
            with self.assertRaises(M06.LabError):
                M06.apply_one(stage, data)
            outside = root / 'fuera'
            outside.mkdir()
            (stage / 'enlace').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(M06.LabError):
                M06.apply_one(stage, {'ruta': 'enlace/Nuevo.cs', 'modo': 'crear', 'codigo': '// nuevo\n'})
            self.assertEqual(list(outside.iterdir()), [])

    def test_sql_exige_helper_solo_a_los_proyectos_que_usan_base_de_datos(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sql_fixture(root)
            self.assertEqual(M06.verify_sql_server(root), ['tests/Base0/Base0.csproj'])
            project = root / 'tests/Base0/Base0.csproj'
            project.write_text(project.read_text().replace('<Compile Include="../Compartido/SqlServerPruebas.cs" />', ''))
            with self.assertRaisesRegex(M06.LabError, 'helper'):
                M06.verify_sql_server(root)

    def test_sql_rechaza_proveedor_en_memoria_y_prueba_omitida(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sql_fixture(root)
            test = root / 'tests/Base1/DominioTests.cs'
            for content in ('options.UseInMemoryDatabase("test");',
                            '[Fact(Skip = "motor ausente")] public void Regla() { }'):
                with self.subTest(content=content):
                    test.write_text(content)
                    with self.assertRaises(M06.LabError):
                        M06.verify_sql_server(root)

    def test_no_tests_reconstruye_las_etapas_y_retos_sin_afirmar_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, manual = dry_run_fixture(root)
            before = {str(p.relative_to(base)): p.read_bytes() for p in base.rglob('*') if p.is_file()}
            report = root / 'informe.json'
            output = root / 'reconstruccion'
            with patch.multiple(M06, ROOT=root, M05=base, PRACTICAS=manual), \
                 patch.object(M06, 'command', side_effect=fake_dotnet), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(M06.main(['--no-tests', '--out', str(report), '--output-dir', str(output)]), 0)
            self.assertTrue(report.is_file(), 'El reconstructor debe escribir un informe verificable')
            result = json.loads(report.read_text())
            self.assertEqual(result['resumen']['resultado'], 'SIN_TESTS')
            self.assertEqual(len(result['pasos']), 72)
            self.assertEqual([stage['n_proyectos'] for stage in result['etapas']], [27, 28, 29])
            self.assertTrue(all(stage['tests_acumulados'] is None for stage in result['etapas']))
            self.assertNotIn('"PASS"', report.read_text())
            self.assertEqual(result['retos_optativos']['resultado'], 'SIN_TESTS')
            after = {str(p.relative_to(base)): p.read_bytes() for p in base.rglob('*') if p.is_file()}
            self.assertEqual(after, before)
            self.assertNotIn('// Reto', (output / '6.1-comunicacion-sincrona-http/src/notes/p1-6.cs').read_text())

    def test_rechaza_una_modificacion_de_documentacion_heredada(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, manual = dry_run_fixture(root)
            content = manual.read_text().replace('### PASO 6.1.21 —',
                       metadata('6.1.20', 'docs/base0.md', 'reemplazar', kind='markdown', code='Alterado') +
                       '\n### PASO 6.1.21 —')
            manual.write_text(content)
            report = root / 'informe.json'
            with patch.multiple(M06, ROOT=root, M05=base, PRACTICAS=manual), \
                 patch.object(M06, 'command', side_effect=fake_dotnet), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(M06.main(['--no-tests', '--out', str(report), '--output-dir', str(root / 'salida')]), 1)
            self.assertEqual(json.loads(report.read_text())['resumen']['resultado'], 'FAIL')
            self.assertEqual((base / 'docs/base0.md').read_text(), 'Documento 0\n')


if __name__ == '__main__':
    unittest.main()
