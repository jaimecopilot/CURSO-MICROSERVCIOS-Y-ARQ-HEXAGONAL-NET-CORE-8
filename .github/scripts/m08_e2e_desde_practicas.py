#!/usr/bin/env python3
"""Reconstruye M08 desde el manual y conserva íntegra la base M07 7.4.

Los catálogos, los adaptadores y los retos se extraen de M08_PRACTICAS.md.
No consulta artefactos de autoría ni copia una implementación final M08.
"""
from __future__ import annotations

import argparse
from bisect import bisect_right
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path, PureWindowsPath
import re
import shutil
import sys
import tempfile
import xml.etree.ElementTree as ET
from m08_texto import parse_explanation

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'M08_API_GATEWAY'
PRACTICAS = BASE / 'PRACTICAS/M08_PRACTICAS.md'
M07 = ROOT / 'M07_OBSERVABILIDAD_RESILIENCIA/PROYECTO/7.4-retry-circuit-breaker-polly'
STAGES = ['8.1-introduccion-api-gateway', '8.2-configuracion-basica-yarp',
          '8.3-enrutamiento-peticiones', '8.4-balanceo-carga']
PROJECT_NAMES = ['ApiGateway', 'ConfiguracionYarp', 'Enrutamiento', 'Balanceo']
CATALOG_TESTS = [12, 10, 10, 10]
FUNCTIONAL_TESTS = [0, 26, 15, 5]
EXPECTED = [403 + sum(CATALOG_TESTS[:i+1]) + sum(FUNCTIONAL_TESTS[:i+1]) for i in range(4)]
PROJECT_COUNTS = [35, 37, 38, 39]
TEST_PROJECT_COUNTS = [23, 24, 25, 26]
DOCUMENT_COUNTS = [44, 46, 48, 50]
CHECKPOINTS = {f'8.{i}': {2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16}
               for i in (1, 2, 3, 4)}

_spec = importlib.util.spec_from_file_location('m05_e2e_common',
                                             Path(__file__).with_name('m05_e2e_desde_practicas.py'))
common = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(common)
LabError = common.LabError
check = common.check
command = common.command
manifest = common.manifest
manifest_sha = common.manifest_sha
copy_project = common.copy_project
build_and_test = common.build_and_test
compare_inherited = common.compare_inherited
compare_inherited_tests = common.compare_inherited_tests
IGNORED = common.IGNORED


def _markdown_exterior(content):
    """Conserva offsets y líneas, ocultando únicamente los bloques de código."""
    exterior = []
    fence = None
    last = []
    block = []
    for number, line in enumerate(content.splitlines(keepends=True), 1):
        opening = re.match(r'^(`{3,})([^`\n]*)\r?\n?$', line)
        if fence is None and opening:
            fence = len(opening.group(1))
            block = []
        elif fence is not None and re.fullmatch(r'`{' + str(fence) + r',}\s*', line):
            last = block
            fence = None
            exterior.append(re.sub(r'[^\n]', ' ', line))
            continue
        elif fence is not None:
            block.append(line.rstrip('\r\n'))
        else:
            explanation = parse_explanation(line)
            if explanation:
                index = explanation[0] - 1
                aligned = 0 <= index < len(last)
                if aligned:
                    aligned = explanation[1] == last[index].strip()
                check(aligned, f'Explicación desalineada en línea Markdown {number}: {line.strip()}')
        exterior.append(re.sub(r'[^\n]', ' ', line) if fence is not None else line)
    check(fence is None, 'Hay un bloque de código sin cerrar')
    return ''.join(exterior)


def _relative_path(value):
    check(isinstance(value, str) and bool(value.strip()), 'Ruta insegura: falta ruta relativa')
    check(not any(char in value for char in ('\\', '\x00', '\n', '\r')),
          f'Ruta insegura: usa separadores / y una ruta relativa: {value!r}')
    path = Path(value)
    check(not path.is_absolute() and not PureWindowsPath(value).drive
          and path.parts and '..' not in path.parts and str(path) != '.',
          f'Ruta insegura: {value!r}')
    return path


def parse_markdown(content):
    """Valida el contrato editorial y devuelve solo operaciones ejecutables."""
    exterior = _markdown_exterior(content)
    expected = [f'8.{point}.{step}' for point in (1, 2, 3, 4) for step in range(1, 25)]
    positions = list(re.finditer(r'^### PASO (\S+) —', exterior, re.M))
    check([match.group(1) for match in positions] == expected,
          'Los 96 pasos no están completos o en orden')
    check(not re.search(r'(?i)\b(?:fuente|procedencia)\b', content),
          'Texto editorial no permitido en el manual')
    check(not re.search(r'^#{1,6}\s+Errores comunes del ejercicio completo', exterior, re.M | re.I),
          'Hay un bloque global de errores repetido')
    for index, position in enumerate(positions):
        end = positions[index + 1].start() if index + 1 < len(positions) else len(exterior)
        body = exterior[position.end():end]
        action = re.search(r'\*\*Procedimiento guiado\.\*\*\n\n((?:\d+\. [^\n]+\n)+)', body)
        check(action is not None, position.group(1) + ': falta procedimiento guiado')
        check(re.findall(r'^(\d+)\. ', action.group(1), re.M) == ['1', '2', '3', '4'],
              position.group(1) + ': debe haber cuatro acciones')
        check('**Por qué funciona así.**' in body and '**Verificación concreta.**' in body,
              position.group(1) + ': faltan explicación o verificación')

    challenge_headings = list(re.finditer(r'^## Reto de ampliación \(optativo\)\s*$', exterior, re.M))
    check(len(challenge_headings) == 4, 'Deben existir cuatro retos optativos completos')
    step_offsets = [position.start() for position in positions]
    challenge_points = []
    for heading in challenge_headings:
        index = bisect_right(step_offsets, heading.start()) - 1
        check(index >= 0, 'Reto fuera de un punto')
        challenge_points.append(positions[index].group(1))
    check(challenge_points == ['8.1.24', '8.2.24', '8.3.24', '8.4.24'], 'Los retos deben cerrar sus cuatro puntos')

    records = {'M08_CODIGO': [], 'M08_RETO': []}
    pattern = re.compile(r'<!-- (M08_CODIGO|M08_RETO) (\{[^\n]+\}) -->\n'
                         r'```(csharp|xml|markdown|json|text)\n([\s\S]*?)\n```(?=\n|$)')
    markers = list(re.finditer(r'<!--\s*M08_(?:CODIGO|RETO)\b', exterior))
    matches = [match for match in pattern.finditer(content)
               if exterior[match.start():match.start() + 4] == '<!--']
    check([marker.start() for marker in markers] == [match.start() for match in matches],
          'Hay metadatos o bloques M08 incompletos o con formato no válido')
    for match in matches:
        kind = match.group(1)
        try:
            info = json.loads(match.group(2))
        except (ValueError, TypeError) as exc:
            raise LabError('Metadatos JSON no válidos: ' + str(exc)) from exc
        check(isinstance(info, dict), 'Los metadatos deben ser un objeto JSON')
        path = _relative_path(info.get('ruta'))
        mode = info.get('modo')
        check(mode in ('crear', 'reemplazar'), 'Operación no válida: ' + str(mode))
        check(set(info) == {'paso', 'ruta', 'modo'},
              'Los archivos completos solo admiten paso, ruta y modo; no anclas ni sangría')
        identifier = info.get('paso')
        check(isinstance(identifier, str) and
              (identifier in expected if kind == 'M08_CODIGO'
               else re.fullmatch(r'8\.[1-4]\.reto\.(1|3|6)', identifier)),
              'Paso de bloque no válido: ' + str(identifier))
        index = bisect_right(step_offsets, match.start()) - 1
        check(index >= 0, f'Bloque de {identifier} fuera de su paso')
        current = positions[index].group(1)
        check(identifier == current if kind == 'M08_CODIGO' else identifier[:3] == current[:3],
              f'Bloque de {identifier} fuera de su paso')
        if kind == 'M08_RETO':
            point = int(identifier[2]) - 1
            check(challenge_headings[point].start() < match.start(), 'Fragmento fuera del reto optativo')
            check(match.group(3) == 'csharp', 'Los fragmentos de reto deben ser C#')
        info.update(tipo=match.group(3), codigo=match.group(4) + '\n')
        records[kind].append(info)
        if info['tipo'] == 'markdown':
            for line in info['codigo'].splitlines():
                if line.startswith(('    ', '\t')):
                    continue  # Markdown permite ilustraciones de código indentado.
                check(not any(re.search(r'\b\w+<[^>]+>', part) for part in re.split(r'`[^`]*`', line)),
                      f'Genérico sin formato de código en {path}: {line}')
    codes, challenges = records['M08_CODIGO'], records['M08_RETO']
    check(len(codes) >= 52, 'Faltan operaciones obligatorias del catálogo')
    for point in (1, 2, 3, 4):
        check(sum(record['paso'].startswith(f'8.{point}.') for record in codes) >= 13,
              f'Faltan operaciones obligatorias de 8.{point}')
    check([record['paso'] for record in challenges] ==
          [f'8.{point}.reto.{step}' for point in (1, 2, 3, 4) for step in (1, 3, 6)],
          'Deben existir tres fragmentos distintos y ordenados por cada reto')
    return content, codes, challenges


def read_markdown(path=None):
    return parse_markdown((path or PRACTICAS).read_text(encoding='utf-8'))


def projects(stage):
    return sorted(path for path in stage.rglob('*.csproj')
                  if not any(part in IGNORED for part in path.relative_to(stage).parts))


def ensure_solution(stage):
    """Registra todos los proyectos completos con una única invocación add."""
    if not (stage / 'AceriaApp.sln').exists():
        command('dotnet', 'new', 'sln', '--name', 'AceriaApp', cwd=stage)
    files = projects(stage)
    check(files, 'La etapa no contiene proyectos')
    paths = [path.relative_to(stage).as_posix() for path in files]
    command('dotnet', 'sln', 'AceriaApp.sln', 'add', *paths, cwd=stage)
    listing = command('dotnet', 'sln', 'AceriaApp.sln', 'list', cwd=stage)
    listed = {line.strip().replace('\\', '/') for line in listing.splitlines()}
    for path in paths:
        check(path in listed, f'La solución omite {path}')
    return len(files)


def apply_one(stage, record):
    check(record.get('modo') in ('crear', 'reemplazar'), 'Operación no válida: ' + str(record.get('modo')))
    path = _relative_path(record.get('ruta'))
    target = (stage / path).resolve()
    check(target.is_relative_to(stage.resolve()), f'Ruta fuera de la etapa mediante enlace: {path}')
    return common.apply_one(stage, record)


def verify_sql_server(stage):
    """Exige SQL Server solo a integración y rechaza exclusiones de pruebas."""
    relational = {path.replace('\\', '/') for path in common.verify_sql_server(stage)}
    skip = re.compile(r'\[(?:\w+\.)?(?:Fact|Theory)(?:Attribute)?\s*\([^\]]*\bSkip\s*='
                      r'|\[(?:SkippableFact|SkippableTheory)\b'
                      r'|\bSkipException\b|\bAssert\s*\.\s*Skip(?:When|Unless)?\s*\(')
    for path in (stage / 'tests').rglob('*.cs'):
        if any(part in IGNORED for part in path.relative_to(stage).parts):
            continue
        check(not skip.search(path.read_text(encoding='utf-8')),
              f'Prueba omitida o condicional no permitida: {path.relative_to(stage)}')
    # Incluye subcarpetas de tests y archivos enlazados; los tests de dominio
    # no adquieren dependencia SQL por compartir solución con integración.
    for project in projects(stage):
        if not project.is_relative_to(stage / 'tests'):
            continue
        xml = ET.parse(project)
        includes = [node.get('Include', '').replace('\\', '/') for node in xml.findall('.//Compile')]
        files = [path for path in project.parent.rglob('*.cs')
                 if not any(part in IGNORED for part in path.relative_to(project.parent).parts)]
        files += [project.parent / include for include in includes]
        for path in files:
            if path.is_file() and path.suffix == '.cs':
                check(not skip.search(path.read_text(encoding='utf-8')),
                      f'Prueba omitida o condicional no permitida: {path}')
        uses_database = any(path.is_file() and path.name != 'SqlServerPruebas.cs'
                            and re.search(r'\bBaseSqlServer\s*\.\s*Crear\s*\(',
                                          path.read_text(encoding='utf-8')) for path in files)
        if not uses_database:
            continue
        check('../Compartido/SqlServerPruebas.cs' in includes,
              f'Falta vincular el helper SQL Server: {project.relative_to(stage)}')
        packages = {node.get('Include'): node.get('Version') for node in xml.findall('.//PackageReference')}
        check(packages.get('Testcontainers.MsSql') == '3.10.0',
              f'Falta Testcontainers.MsSql 3.10.0: {project.relative_to(stage)}')
        relational.add(project.relative_to(stage).as_posix())
    return sorted(relational)


def _target_result(outcome, point, extra=0):
    name = f'AceriaApp.{PROJECT_NAMES[point - 1]}.Tests'
    matches = [project for project in outcome['proyectos']
               if any(method.startswith(name + '.') for method in project['metodos'])]
    check(len(matches) == 1, 'No se identifica el proyecto de tests ' + name)
    expected = CATALOG_TESTS[point - 1] + FUNCTIONAL_TESTS[point - 1] + extra
    check(matches[0]['tests'] == expected, f'{name}: esperadas {expected} pruebas')
    return matches[0]


def verify_challenges(output, records, *, run_tests=True):
    before = manifest(output)
    results = []
    for point, slug in enumerate(STAGES, 1):
        entry = {'punto': f'8.{point}', 'estado': 'FAIL'}
        try:
            batch = [record for record in records if record['paso'].startswith(f'8.{point}.reto.')]
            check(len(batch) == 3, f'Reto 8.{point}: faltan fragmentos')
            with tempfile.TemporaryDirectory(prefix=f'm08-reto-{point}-') as temporary:
                stage = Path(temporary) / slug
                copy_project(output / slug, stage)
                for record in batch:
                    apply_one(stage, record)
                check(len(projects(stage)) == PROJECT_COUNTS[point - 1],
                      f'Reto 8.{point}: número de proyectos alterado')
                expected_project = CATALOG_TESTS[point - 1] + FUNCTIONAL_TESTS[point - 1] + 1
                entry.update(fragmentos_csharp=3,
                             archivos=sorted({record['ruta'] for record in batch}),
                             tests_proyecto_esperados=expected_project,
                             tests_solucion_esperados=EXPECTED[point - 1] + 1)
                if run_tests:
                    ensure_solution(stage)
                    outcome = build_and_test(stage, EXPECTED[point - 1] + 1)
                    check(outcome['test_projects'] == TEST_PROJECT_COUNTS[point - 1],
                          f'Reto 8.{point}: falta un proyecto de tests')
                    target = _target_result(outcome, point, extra=1)
                    check(any('.Resumen_ConCatalogoPorDefecto_' in method for method in target['metodos']),
                          f'Reto 8.{point}: no se ejecutó la prueba del resumen')
                    entry.update(estado='PASS', tests_proyecto=target['tests'],
                                 tests_solucion=outcome['tests'], test_resumen='PASS')
                else:
                    entry.update(estado='SIN_TESTS', tests_proyecto=None,
                                 tests_solucion=None, test_resumen='SIN_TESTS')
        except Exception as exc:
            entry['error'] = str(exc)
        results.append(entry)
        print(json.dumps(entry, ensure_ascii=False), flush=True)
    check(manifest(output) == before, 'Los retos han modificado las etapas obligatorias')
    status = 'FAIL' if any(entry['estado'] == 'FAIL' for entry in results) else ('PASS' if run_tests else 'SIN_TESTS')
    return {'resultado': status, 'etapas_obligatorias_intactas': True, 'retos': results}


def _checkpoint_target(point, step, stage=None):
    """El proyecto de pruebas nace en 11; el registro final se hace en 16."""
    if step in (2, 16):
        return 'AceriaApp.sln'
    name = f'AceriaApp.{PROJECT_NAMES[point - 1]}.Tests'
    target = f'tests/{name}/{name}.csproj'
    if step >= 11 and (stage is None or (stage / target).is_file()):
        return target
    return 'src/AceriaApp.Api/AceriaApp.Api.csproj'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=BASE / 'M08_E2E_RESULTADOS.json')
    parser.add_argument('--output-dir', type=Path, default=BASE / 'PROYECTO')
    parser.add_argument('--no-tests', action='store_true',
                        help='Reconstruye e inspecciona sin compilar ni ejecutar pruebas; resultado SIN_TESTS')
    args = parser.parse_args(argv)
    report = {'fecha': datetime.now(timezone.utc).isoformat(), 'manual': 'PRACTICAS/M08_PRACTICAS.md',
              'construccion': 'base M07 7.4 más bloques del manual, sin copiar una etapa final M08',
              'etapas': [], 'pasos': []}
    base_path = M07.resolve()
    # Un informe no debe poder modificar silenciosamente la base protegida.
    if args.out.resolve().is_relative_to(base_path):
        print('El informe de salida no puede escribirse dentro de la base M07', file=sys.stderr)
        return 1
    try:
        revision = os.environ.get('GITHUB_SHA') or command('git', 'rev-parse', 'HEAD', cwd=ROOT).strip()
        check(bool(re.fullmatch(r'[0-9a-f]{40}', revision)), 'Falta una revisión Git completa')
        report['commit_comprobado'] = revision
        content, codes, challenges = read_markdown()
        report['manual_sha256'] = common.text_sha(content)
        check(M07.is_dir(), 'No existe la base M07 7.4')
        base_manifest = manifest(M07)
        base_projects = projects(M07)
        base_test_projects = [project for project in base_projects if project.is_relative_to(M07 / 'tests')]
        check(len(base_projects) == 34, 'La base M07 debe contener exactamente 34 proyectos')
        check(len(base_test_projects) == 22, 'La base M07 debe contener exactamente 22 proyectos de tests')
        check(len(list((M07 / 'docs').glob('*.md'))) == 42, 'La base M07 debe conservar sus 42 documentos Markdown')
        report['base_m07'] = {'etapa': str(M07.relative_to(ROOT)), 'proyectos': 34, 'tests': 403,
                              'proyectos_tests': 22, 'sha256': manifest_sha(base_manifest),
                              'archivos': base_manifest}
        output = args.output_dir.resolve()
        check(output != base_path and base_path not in output.parents and output not in base_path.parents,
              'El directorio de salida se solapa con la base M07')
        output.mkdir(parents=True, exist_ok=True)
        previous = M07
        for point, slug in enumerate(STAGES, 1):
            stage = output / slug
            check(not stage.is_symlink(), f'La etapa de salida no puede ser un enlace: {stage}')
            if stage.exists():
                shutil.rmtree(stage)
            previous_manifest = manifest(previous)
            copy_project(previous, stage)
            compilations = []
            operations = 0
            for step in range(1, 25):
                identifier = f'8.{point}.{step}'
                batch = [record for record in codes if record['paso'] == identifier]
                # Todos los archivos de un paso se completan antes del checkpoint.
                for record in batch:
                    apply_one(stage, record)
                    operations += 1
                compiled = False
                if not args.no_tests and step in CHECKPOINTS[f'8.{point}']:
                    target = _checkpoint_target(point, step, stage)
                    if target == 'AceriaApp.sln':
                        ensure_solution(stage)
                    command('dotnet', 'build', target, '-c', 'Release', '--disable-build-servers', '-m:1', '-p:NuGetAudit=false', cwd=stage)
                    compilations.append({'paso': identifier, 'objetivo': target, 'resultado': 'PASS'})
                    compiled = True
                report['pasos'].append({'paso': identifier, 'codigo_escrito': len(batch),
                                         'archivos': [record['ruta'] for record in batch],
                                         'resultado': 'codigo_aplicado_y_compilado' if batch and compiled
                                         else 'codigo_aplicado' if batch else 'guia_manual_no_simulada'})
            total_projects = ensure_solution(stage)
            check(total_projects == PROJECT_COUNTS[point - 1],
                  f'Etapa {slug}: se esperaban {PROJECT_COUNTS[point - 1]} proyectos; hay {total_projects}')
            test_projects = [project for project in projects(stage) if project.is_relative_to(stage / 'tests')]
            check(len(test_projects) == TEST_PROJECT_COUNTS[point - 1],
                  f'Etapa {slug}: número de proyectos de tests incorrecto')
            documents = len(list((stage / 'docs').glob('*.md')))
            check(documents == DOCUMENT_COUNTS[point - 1],
                  f'Etapa {slug}: se esperaban {DOCUMENT_COUNTS[point - 1]} documentos; hay {documents}')
            sql_projects = verify_sql_server(stage)
            inherited = compare_inherited(previous, stage)
            inherited_tests = compare_inherited_tests(previous, stage)
            check(manifest(previous) == previous_manifest, 'La etapa anterior se ha alterado')
            if args.no_tests:
                outcome = {'tests': None, 'test_projects': None, 'proyectos': []}
            else:
                outcome = build_and_test(stage, EXPECTED[point - 1])
                check(outcome['test_projects'] == TEST_PROJECT_COUNTS[point - 1],
                      f'Etapa {slug}: falta un proyecto de tests ejecutado')
                _target_result(outcome, point)
            current_manifest = manifest(stage)
            report['etapas'].append({
                'punto': f'8.{point}', 'carpeta': slug, 'pasos': 24, 'operaciones_codigo': operations,
                'n_proyectos': total_projects, 'n_proyectos_tests': len(test_projects), 'n_documentos': documents,
                'documentos_heredados_identicos': inherited,
                'archivos_tests_heredados_identicos': inherited_tests,
                'proveedor_configurado': 'Microsoft.EntityFrameworkCore.SqlServer',
                'proyectos_sql_server': sql_projects,
                'builds_intermedios': len(compilations), 'compilaciones': compilations,
                'tests_acumulados': outcome['tests'], 'tests_catalogo_nuevos': CATALOG_TESTS[point - 1],
                'tests_funcionales_nuevos': FUNCTIONAL_TESTS[point - 1], 'expected': EXPECTED[point - 1],
                'tests_proyectos': outcome['proyectos'], 'estado': 'SIN_TESTS' if args.no_tests else 'PASS',
                'sha256': manifest_sha(current_manifest), 'archivos': current_manifest,
            })
            print(f'M08 8.{point}: {operations} operaciones desde manual; {len(compilations)} '
                  f'compilaciones intermedias; {outcome["tests"]} tests; {total_projects} proyectos', flush=True)
            previous = stage
        check(len(report['pasos']) == 96, 'No se han recorrido los 96 pasos')
        check(manifest(M07) == base_manifest, 'La base M07 ha cambiado')
        report['retos_optativos'] = verify_challenges(output, challenges, run_tests=not args.no_tests)
        check(report['retos_optativos']['resultado'] != 'FAIL', 'Hay retos optativos sin superar')
        check(manifest(M07) == base_manifest, 'La base M07 ha cambiado al verificar retos')
        report['resumen'] = {
            'resultado': 'SIN_TESTS' if args.no_tests else 'PASS', 'pasos': 96,
            'operaciones_codigo': len(codes), 'archivos_distintos': len({record['ruta'] for record in codes}),
            'builds_intermedios': sum(stage['builds_intermedios'] for stage in report['etapas']),
            'tests_por_etapa': [stage['tests_acumulados'] for stage in report['etapas']],
            'tests_por_etapa_esperados': EXPECTED, 'base_m07_intacta': True,
        }
    except Exception as exc:
        report['resumen'] = {'resultado': 'FAIL', 'error': str(exc)}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report['resumen'], ensure_ascii=False), flush=True)
    return 1 if report['resumen']['resultado'] == 'FAIL' else 0


if __name__ == '__main__':
    sys.exit(main())
