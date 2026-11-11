"""Contrato del reconstructor M07 con manuales pequeños e independientes."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/m07_e2e_desde_practicas.py'
SPEC = importlib.util.spec_from_file_location('m07_e2e_desde_practicas', SCRIPT)
M07 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M07)


def metadata(step, path, mode='crear', *, challenge=False, code='public class Ejemplo { }', kind='csharp', **extra):
    info = {'paso': step, 'ruta': path, 'modo': mode, **extra}
    label = 'M07_RETO' if challenge else 'M07_CODIGO'
    block = '<!-- ' + label + ' ' + json.dumps(info) + ' -->\n```' + kind + '\n' + code + '\n```\n'
    if kind == 'csharp':
        for number, line in enumerate(code.splitlines(), 1):
            quote = '`' + line.strip() + '`' if line.strip() else '(línea vacía)'
            block += f'- **Línea {number}:** {quote} → Explica la línea.\n\n'
    return block


def manual_fixture():
    """52 operaciones y cuatro retos: no requiere archivos del curso."""
    pieces = ['# Manual M07\n']
    for point in (1, 2, 3, 4):
        for step in range(1, 25):
            identifier = f'7.{point}.{step}'
            pieces.append(f'### PASO {identifier} — Ejercicio\n\n'
                          '**Procedimiento guiado.**\n\n'
                          '1. Localiza la carpeta.\n2. Crea el archivo.\n'
                          '3. Guarda el archivo.\n4. Revisa su contenido.\n\n')
            if 4 <= step <= 16:
                pieces.append(metadata(identifier, f'docs/p{point}-{step}.cs'))
            pieces.append('**Por qué funciona así.** Explicación.\n\n'
                          '**Verificación concreta.** Comprobación.\n\n')
        pieces.append('## Reto de ampliación (optativo)\n\n')
        for step in (1, 3, 6):
            pieces.append(metadata(f'7.{point}.reto.{step}', f'docs/p{point}-6.cs',
                                   'reemplazar', challenge=True, code=f'public class Ejemplo {{ }}\n// Reto {step}'))
    return ''.join(pieces)


class ParseMarkdownTests(unittest.TestCase):
    def test_extrae_codigo_y_retos_del_manual_completo(self):
        content = manual_fixture()
        try:
            actual, codes, challenges = M07.parse_markdown(content)
        except M07.LabError as exc:
            self.fail('El parser debe admitir los 96 pasos M07: ' + str(exc))
        self.assertEqual(actual, content)
        self.assertEqual(len(codes), 52)
        self.assertEqual(len(challenges), 12)
        self.assertEqual(codes[0], {'paso': '7.1.4', 'ruta': 'docs/p1-4.cs', 'modo': 'crear',
                                    'tipo': 'csharp', 'codigo': 'public class Ejemplo { }\n'})

    def test_rechaza_un_paso_ausente_o_duplicado(self):
        content = manual_fixture()
        for broken in (content.replace('### PASO 7.2.17 — Ejercicio', '### Otro apartado'),
                       content.replace('### PASO 7.2.17 —', '### PASO 7.2.16 —')):
            with self.subTest(broken=broken[:20]), self.assertRaises(M07.LabError):
                M07.parse_markdown(broken)

    def test_rechaza_metadatos_alterados_que_no_se_pueden_extraer(self):
        for before, after in (('"modo": "crear"', '"modo": "borrar"'),
                              ('"paso": "7.1.4"', '"paso": "7.1.99"'),
                              ('"ruta": "docs/p1-4.cs"', '"ruta": null'),
                              ('```csharp', '```python'),
                              ('"paso": "7.1.4"', '"paso": ')):
            with self.subTest(after=after), self.assertRaises(M07.LabError):
                M07.parse_markdown(manual_fixture().replace(before, after, 1))

    def test_rechaza_rutas_que_salen_de_la_etapa_en_windows_o_linux(self):
        for path in ('../fuera.cs', '/tmp/fuera.cs', r'C:\fuera.cs', r'..\fuera.cs',
                     'src/../../fuera.cs', '.', '', r'\\servidor\fuera.cs'):
            with self.subTest(path=path), self.assertRaises(M07.LabError):
                M07.parse_markdown(manual_fixture().replace('"docs/p1-4.cs"', json.dumps(path), 1))

    def test_rechaza_bloque_identificado_como_otro_paso(self):
        with self.assertRaisesRegex(M07.LabError, 'fuera de su paso'):
            M07.parse_markdown(manual_fixture().replace('"paso": "7.1.4"', '"paso": "7.1.5"', 1))

    def test_rechaza_cuatro_acciones_que_no_estan_numeradas_en_orden(self):
        with self.assertRaises(M07.LabError):
            M07.parse_markdown(manual_fixture().replace('3. Guarda el archivo.', '4. Guarda el archivo.', 1))

    def test_rechaza_una_quinta_accion(self):
        with self.assertRaises(M07.LabError):
            M07.parse_markdown(manual_fixture().replace('4. Revisa su contenido.\n', '4. Revisa su contenido.\n5. Repite.\n', 1))

    def test_rechaza_explicacion_que_cita_otra_linea(self):
        with self.assertRaisesRegex(M07.LabError, 'desalineada'):
            M07.parse_markdown(manual_fixture().replace('**Línea 1:** `public class Ejemplo { }`',
                                                       '**Línea 2:** `public class Ejemplo { }`', 1))

    def test_cuenta_lineas_vacias_y_rechaza_una_linea_vacia_falsa(self):
        content = manual_fixture().replace('public class Ejemplo { }\n```',
                                           '\npublic class Ejemplo { }\n```\n- **Línea 1:** (línea vacía) → Separa.', 1)
        content = content.replace('**Línea 1:** `public class Ejemplo { }`', '**Línea 2:** `public class Ejemplo { }`', 1)
        M07.parse_markdown(content)
        with self.assertRaisesRegex(M07.LabError, 'desalineada'):
            M07.parse_markdown(content.replace('**Línea 1:** (línea vacía)', '**Línea 2:** (línea vacía)', 1))

    def test_rechaza_retos_duplicados_aunque_haya_doce_fragmentos(self):
        with self.assertRaises(M07.LabError):
            M07.parse_markdown(manual_fixture().replace('"paso": "7.2.reto.6"', '"paso": "7.2.reto.3"', 1))

    def test_rechaza_inserciones_y_fragmentos_con_anclas_o_sangria(self):
        for before, after in (('"modo": "reemplazar"', '"modo": "insertar_antes"'),
                              ('"modo": "reemplazar"', '"modo": "reemplazar", "ancla": "Ejemplo"'),
                              ('"modo": "crear"', '"modo": "crear", "sangria": 4')):
            with self.subTest(after=after), self.assertRaises(M07.LabError):
                M07.parse_markdown(manual_fixture().replace(before, after, 1))

    def test_reto_admite_archivos_completos_con_tests_heredados(self):
        complete = 'public class Ejemplo { [Fact] public void Anterior() { } [Fact] public void Resumen() { } }'
        content = manual_fixture()
        for point in (1, 2, 3, 4):
            before = metadata(f'7.{point}.reto.6', f'docs/p{point}-6.cs', 'reemplazar', challenge=True, code='public class Ejemplo { }\n// Reto 6')
            after = metadata(f'7.{point}.reto.6', f'docs/p{point}-6.cs', 'reemplazar', challenge=True, code=complete)
            content = content.replace(before, after)
        _, _, challenges = M07.parse_markdown(content)
        self.assertEqual(len(challenges), 12)
        self.assertEqual(sum(c['codigo'].count('[Fact]') for c in challenges), 8)

    def test_admite_explicaciones_de_lineas_clave_sin_forzar_cobertura_total(self):
        content = manual_fixture().replace('- **Línea 1:** `public class Ejemplo { }` → Explica la línea.\n\n', '', 1)
        content = content.replace('- **Línea 2:** `// Reto 1` → Explica la línea.\n\n', '', 1)
        content = content.replace('**Línea 1:** `public class Ejemplo { }`', '**Línea 1:** `public class`', 1)
        _, codes, challenges = M07.parse_markdown(content)
        self.assertEqual(len(codes), 52)
        self.assertEqual(len(challenges), 12)

    def test_no_confunde_un_encabezado_dentro_del_codigo_con_un_paso(self):
        content = manual_fixture().replace(metadata('7.1.4', 'docs/p1-4.cs'),
                                          metadata('7.1.4', 'docs/p1-4.cs', kind='markdown', code='### PASO 7.9.99 — Ilustración'), 1)
        _, codes, _ = M07.parse_markdown(content)
        self.assertEqual(len(codes), 52)
        self.assertEqual(codes[0]['codigo'], '### PASO 7.9.99 — Ilustración\n')

    def test_markdown_admite_genericos_en_codigo_indentado_y_rechaza_prosa_sin_formato(self):
        original = metadata('7.1.4', 'docs/p1-4.cs')
        snippet = metadata('7.1.4', 'docs/p1-4.cs', kind='markdown',
                           code='Ejemplo:\n\n    builder.Services.AddCheck<SqlHealth>();')
        content = manual_fixture().replace(original, snippet, 1)
        try:
            _, codes, _ = M07.parse_markdown(content)
        except M07.LabError as exc:
            self.fail('El bloque indentado es código Markdown válido: ' + str(exc))
        self.assertIn('AddCheck<SqlHealth>', codes[0]['codigo'])
        with self.assertRaisesRegex(M07.LabError, 'Genérico sin formato'):
            M07.parse_markdown(content.replace('    builder.Services.AddCheck<SqlHealth>();',
                                               'Usa AddCheck<SqlHealth> para registrar.'))



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
    base = root / 'M06_COMUNICACION_MICROSERVICIOS/PROYECTO/6.3-cuando-usar-cada-enfoque'
    sql_fixture(base)
    for number in range(2, 18):
        write(base, f'tests/Base{number}/Base{number}.csproj', '<Project />')
    for number in range(11):
        write(base, f'src/Base{number}/Base{number}.csproj', '<Project />')
    for number in range(34):
        write(base, f'docs/base{number}.md', f'Documento {number}\n')
    write(base, 'AceriaApp.sln', '')
    content = manual_fixture()
    for point in (1, 2, 3, 4):
        content = content.replace(f'docs/p{point}-', f'src/notes/p{point}-')
        for step in (4, 16):
            content = content.replace(f'src/notes/p{point}-{step}.cs', f'docs/p{point}-{step}.md')
        test_name = ['Logging', 'HealthChecks', 'GestionExcepciones', 'Resiliencia'][point-1]
        additions = metadata(f'7.{point}.5', f'tests/AceriaApp.{test_name}.Tests/AceriaApp.{test_name}.Tests.csproj',
                             code='<Project />', kind='xml')
        if point == 1:
            for name in ('Observabilidad',):
                additions += metadata('7.1.5', f'src/Nuevo{name}/Nuevo{name}.csproj', code='<Project />', kind='xml')
        content = content.replace(metadata(f'7.{point}.5', f'src/notes/p{point}-5.cs'),
                                  metadata(f'7.{point}.5', f'src/notes/p{point}-5.cs') + additions)
    manual = write(root, 'M07_OBSERVABILIDAD_RESILIENCIA/PRACTICAS/M07_PRACTICAS.md', content)
    return base, manual


class RuntimeTests(unittest.TestCase):
    def test_anade_todos_los_proyectos_a_la_solucion_en_una_operacion(self):
        with tempfile.TemporaryDirectory() as folder:
            stage = Path(folder)
            for name in ('Uno', 'Dos', 'Tres'):
                write(stage, f'src/{name}/{name}.csproj', '<Project />')
            write(stage, 'src/Uno/obj/NoEsProyecto.csproj', '<Project />')
            with patch.object(M07, 'command', side_effect=fake_dotnet) as process:
                self.assertEqual(M07.ensure_solution(stage), 3)
            self.assertEqual(len((stage / 'AceriaApp.sln').read_text().splitlines()), 3)
            additions = [call for call in process.call_args_list if call.args[:4] ==
                         ('dotnet', 'sln', 'AceriaApp.sln', 'add')]
            self.assertEqual(len(additions), 1)
            self.assertEqual(set(additions[0].args[4:]),
                             {'src/Uno/Uno.csproj', 'src/Dos/Dos.csproj', 'src/Tres/Tres.csproj'})

    def test_reemplazos_completos_exigen_archivo_y_protegen_symlinks(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            stage = root / 'stage'
            stage.mkdir()
            with self.assertRaises(M07.LabError):
                M07.apply_one(stage, {'ruta': 'src/Ausente.cs', 'modo': 'reemplazar', 'codigo': 'nuevo'})
            write(stage, 'src/Ejemplo.cs', 'contenido anterior')
            M07.apply_one(stage, {'ruta': 'src/Ejemplo.cs', 'modo': 'reemplazar', 'codigo': 'contenido nuevo'})
            self.assertEqual((stage / 'src/Ejemplo.cs').read_text(), 'contenido nuevo')
            outside = root / 'fuera'
            outside.mkdir()
            (stage / 'enlace').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(M07.LabError):
                M07.apply_one(stage, {'ruta': 'enlace/Nuevo.cs', 'modo': 'crear', 'codigo': '// nuevo\n'})
            self.assertEqual(list(outside.iterdir()), [])

    def test_sql_exige_helper_solo_a_los_proyectos_que_usan_base_de_datos(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sql_fixture(root)
            self.assertEqual(M07.verify_sql_server(root), ['tests/Base0/Base0.csproj'])
            project = root / 'tests/Base0/Base0.csproj'
            project.write_text(project.read_text().replace('<Compile Include="../Compartido/SqlServerPruebas.cs" />', ''))
            with self.assertRaisesRegex(M07.LabError, 'helper'):
                M07.verify_sql_server(root)

    def test_sql_rechaza_proveedor_en_memoria_y_prueba_omitida(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sql_fixture(root)
            test = root / 'tests/Base1/DominioTests.cs'
            for content in ('options.UseInMemoryDatabase("test");',
                            '[Fact(Skip = "motor ausente")] public void Regla() { }'):
                with self.subTest(content=content):
                    test.write_text(content)
                    with self.assertRaises(M07.LabError):
                        M07.verify_sql_server(root)

    def test_no_tests_reconstruye_las_etapas_y_retos_sin_afirmar_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, manual = dry_run_fixture(root)
            before = {str(p.relative_to(base)): p.read_bytes() for p in base.rglob('*') if p.is_file()}
            report = root / 'informe.json'
            output = root / 'reconstruccion'
            with patch.multiple(M07, ROOT=root, M06=base, PRACTICAS=manual), \
                 patch.object(M07, 'command', side_effect=fake_dotnet), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(M07.main(['--no-tests', '--out', str(report), '--output-dir', str(output)]), 0)
            self.assertTrue(report.is_file(), 'El reconstructor debe escribir un informe verificable')
            result = json.loads(report.read_text())
            self.assertEqual(result['resumen']['resultado'], 'SIN_TESTS')
            self.assertEqual(len(result['pasos']), 96)
            self.assertEqual([stage['n_proyectos'] for stage in result['etapas']], [31, 32, 33, 34])
            self.assertTrue(all(stage['tests_acumulados'] is None for stage in result['etapas']))
            self.assertNotIn('"PASS"', report.read_text())
            self.assertEqual(result['retos_optativos']['resultado'], 'SIN_TESTS')
            after = {str(p.relative_to(base)): p.read_bytes() for p in base.rglob('*') if p.is_file()}
            self.assertEqual(after, before)
            self.assertNotIn('// Reto', (output / '7.1-logging/src/notes/p1-7.cs').read_text())

    def test_rechaza_una_modificacion_de_documentacion_heredada(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, manual = dry_run_fixture(root)
            content = manual.read_text().replace('### PASO 7.1.21 —',
                       metadata('7.1.20', 'docs/base0.md', 'reemplazar', kind='markdown', code='Alterado') +
                       '\n### PASO 7.1.21 —')
            manual.write_text(content)
            report = root / 'informe.json'
            with patch.multiple(M07, ROOT=root, M06=base, PRACTICAS=manual), \
                 patch.object(M07, 'command', side_effect=fake_dotnet), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(M07.main(['--no-tests', '--out', str(report), '--output-dir', str(root / 'salida')]), 1)
            self.assertEqual(json.loads(report.read_text())['resumen']['resultado'], 'FAIL')
            self.assertEqual((base / 'docs/base0.md').read_text(), 'Documento 0\n')

    def test_checkpoint_respeta_creacion_diferida_del_proyecto_de_tests(self):
        for point in (1, 2, 3, 4):
            with self.subTest(point=point), tempfile.TemporaryDirectory() as folder:
                stage = Path(folder)
                name = ['Logging', 'HealthChecks', 'GestionExcepciones', 'Resiliencia'][point-1]
                project = f'tests/AceriaApp.{name}.Tests/AceriaApp.{name}.Tests.csproj'
                creation = 12 if point in (1, 4) else 11
                final = 17 if point in (1, 4) else 16
                self.assertEqual(M07._checkpoint_target(point, creation - 1, stage),
                                 'src/AceriaApp.Api/AceriaApp.Api.csproj')
                self.assertEqual(M07._checkpoint_target(point, creation, stage),
                                 'src/AceriaApp.Api/AceriaApp.Api.csproj')
                write(stage, project, '<Project />')
                self.assertEqual(M07._checkpoint_target(point, creation, stage), project)
                self.assertEqual(M07._checkpoint_target(point, final, stage), 'AceriaApp.sln')
                self.assertEqual(M07._checkpoint_target(point, 2, stage), 'AceriaApp.sln')

    def test_rechaza_modificacion_de_tests_heredados(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, manual = dry_run_fixture(root)
            original = (base / 'tests/Base1/DominioTests.cs').read_bytes()
            content = manual.read_text().replace('### PASO 7.1.21 —',
                       metadata('7.1.20', 'tests/Base1/DominioTests.cs', 'reemplazar', code='Alterado') +
                       '\n### PASO 7.1.21 —')
            manual.write_text(content)
            report = root / 'informe.json'
            with patch.multiple(M07, ROOT=root, M06=base, PRACTICAS=manual), \
                 patch.object(M07, 'command', side_effect=fake_dotnet), contextlib.redirect_stdout(io.StringIO()):
                status = M07.main(['--no-tests', '--out', str(report), '--output-dir', str(root / 'salida')])
            self.assertEqual(status, 1)
            result = json.loads(report.read_text())
            self.assertEqual(result['resumen']['resultado'], 'FAIL')
            self.assertIn('Prueba heredada alterada', result['resumen']['error'])
            self.assertEqual((base / 'tests/Base1/DominioTests.cs').read_bytes(), original)

    def test_rechaza_etapa_sin_sus_dos_documentos_nuevos(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, manual = dry_run_fixture(root)
            manual.write_text(manual.read_text().replace('docs/p2-16.md', 'src/notes/p2-16.cs'))
            report = root / 'informe.json'
            with patch.multiple(M07, ROOT=root, M06=base, PRACTICAS=manual), \
                 patch.object(M07, 'command', side_effect=fake_dotnet), contextlib.redirect_stdout(io.StringIO()):
                status = M07.main(['--no-tests', '--out', str(report), '--output-dir', str(root / 'salida')])
            self.assertEqual(status, 1)
            result = json.loads(report.read_text())
            self.assertIn('38 documentos; hay 37', result['resumen']['error'])

    def test_rechaza_informe_de_salida_dentro_de_la_base(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            base, manual = dry_run_fixture(root)
            target = base / 'docs/base0.md'
            before = target.read_bytes()
            with patch.multiple(M07, ROOT=root, M06=base, PRACTICAS=manual), \
                 contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(M07.main(['--no-tests', '--out', str(target)]), 1)
            self.assertEqual(target.read_bytes(), before)

    def test_sql_inspecciona_tests_anidados_y_enlazados(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sql_fixture(root)
            write(root, 'tests/Base1/Casos/SqlTests.cs', 'var db = BaseSqlServer . Crear ();')
            with self.assertRaisesRegex(M07.LabError, 'helper'):
                M07.verify_sql_server(root)
            write(root, 'tests/Base1/Base1.csproj', '<Project><ItemGroup>'
                  '<Compile Include="../Compartido/SqlServerPruebas.cs" />'
                  '<PackageReference Include="Testcontainers.MsSql" Version="3.10.0" />'
                  '</ItemGroup></Project>')
            self.assertEqual(M07.verify_sql_server(root), ['tests/Base0/Base0.csproj', 'tests/Base1/Base1.csproj'])
            (root / 'tests/Base1/Casos/SqlTests.cs').unlink()
            write(root, 'compartido/SqlTests.cs', 'var db = BaseSqlServer . Crear ();')
            project = root / 'tests/Base1/Base1.csproj'
            project.write_text(project.read_text().replace('<ItemGroup>', '<ItemGroup><Compile Include="../../compartido/SqlTests.cs" />'))
            self.assertEqual(M07.verify_sql_server(root), ['tests/Base0/Base0.csproj', 'tests/Base1/Base1.csproj'])

    def test_sql_rechaza_skip_en_archivo_enlazado_fuera_de_tests(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sql_fixture(root)
            write(root, 'compartido/ReglaTests.cs', '[Fact(Skip = "omitida")] public void Regla() { }')
            write(root, 'tests/Base1/Base1.csproj', '<Project><ItemGroup>'
                  '<Compile Include="../../compartido/ReglaTests.cs" />'
                  '</ItemGroup></Project>')
            with self.assertRaisesRegex(M07.LabError, 'omitida'):
                M07.verify_sql_server(root)

    def test_resultado_del_reto_exige_solo_una_prueba_adicional_ejecutada(self):
        for point, count in enumerate((26, 22, 22, 50), 1):
            name = ['Logging', 'HealthChecks', 'GestionExcepciones', 'Resiliencia'][point-1]
            outcome = {'proyectos': [{'tests': count + 1, 'metodos': [f'AceriaApp.{name}.Tests.Resumen']}]}
            self.assertEqual(M07._target_result(outcome, point, extra=1)['tests'], count + 1)
            outcome['proyectos'][0]['tests'] += 1
            with self.assertRaisesRegex(M07.LabError, 'esperadas'):
                M07._target_result(outcome, point, extra=1)


if __name__ == '__main__':
    unittest.main()
