"""Contratos de publicación M08: evidencia, revisión y hashes reales de archivos."""
from __future__ import annotations
import contextlib, importlib.util, io, json, os, sys, tarfile, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts'
sys.path.insert(0,str(SCRIPTS))

def load(name):
    path=SCRIPTS/(name+'.py')
    if not path.exists():return None
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

pack=load('m08_empaquetar');close=load('m08_cerrar');validate=load('m08_validar')
SHA='a'*40


def write(root,path,value):
    target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(value,bytes):target.write_bytes(value)
    else:target.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n' if isinstance(value,(dict,list)) else value,encoding='utf-8')
    return target


def fixture(root):
    base=root/'M08_API_GATEWAY'
    for i,slug in enumerate(pack.STAGES,1):
        write(base,f'PROYECTO/{slug}/src/Program.cs',f'// Etapa {i}: correlación\n')
    for kind in ('TEORIA','PRACTICAS'):
        write(base,f'{kind}/M08_{kind}.md',f'# {kind}: observación\n')
        write(base,f'{kind}/M08_{kind}.pdf',b'%PDF-fixture\n')
    from validar_sqlserver import file_manifest,source_manifest
    e2e={'commit_comprobado':SHA,'manual_sha256':pack.sha(base/'PRACTICAS/M08_PRACTICAS.md'),
         'resumen':{'resultado':'PASS','pasos':96,'tests_por_etapa':pack.EXPECTED,'base_m07_intacta':True},
         'etapas':[{'estado':'PASS','tests_acumulados':n,'n_proyectos':pack.PROJECT_COUNTS[i],'n_proyectos_tests':pack.TEST_PROJECT_COUNTS[i],'n_documentos':pack.DOCUMENT_COUNTS[i], 'tests_proyectos':[{'proyecto':f'test-{j}','tests':n-pack.TEST_PROJECT_COUNTS[i]+1 if j==0 else 1,'metodos':[f'm{t}' for t in range(n-pack.TEST_PROJECT_COUNTS[i]+1 if j==0 else 1)]} for j in range(pack.TEST_PROJECT_COUNTS[i])]}
                   for i,n in enumerate(pack.EXPECTED)],
         'retos_optativos':{'resultado':'PASS','etapas_obligatorias_intactas':True,
                           'retos':[{'estado':'PASS','tests_solucion':n+1,'tests_proyecto':pack.CATALOG_TESTS[i]+pack.FUNCTIONAL_TESTS[i]+1,'test_resumen':'PASS'}
                                    for i,n in enumerate(pack.EXPECTED)]}}
    from m08_e2e_desde_practicas import manifest,manifest_sha
    for i,stage in enumerate(e2e['etapas']):
        files=manifest(base/'PROYECTO'/pack.STAGES[i])
        stage.update(punto=f'8.{i+1}',carpeta=pack.STAGES[i],archivos=files,sha256=manifest_sha(files))
    sql={'resultado':'PASS','commit_comprobado':SHA,'tests_por_etapa':pack.EXPECTED,
         'manual_sha256':pack.sha(base/'PRACTICAS/M08_PRACTICAS.md'),
         'archivos_proyectos_sha256':file_manifest(base/'PROYECTO'),
         'codigo_normalizado_sha256':source_manifest(base/'PROYECTO'),
         'proveedor':'Microsoft.EntityFrameworkCore.SqlServer','bases_verificadas':1,
         'evidencias_bd':[{'provider':'Microsoft.EntityFrameworkCore.SqlServer','engineEdition':4,'version':'16.0.1',
                          'database':'AceriaTest_fixture','modo':'conexion_externa','origen':'Testcontainers'}]}
    smoke={'resultado':'PASS','commit_comprobado':SHA,'codigo_normalizado_sha256':source_manifest(base/'PROYECTO'/pack.STAGES[-1]),
           **{key:'PASS' for key in (*pack.SMOKE_CHECKS,'mensajeria')},
           'balanceo_instancias':['inventario-1','inventario-2'],'recuperacion_instancias':['inventario-1','inventario-2'],
           'instancia_caida':['inventario-2']*6,'todos_caidos_http':503,'persistencia_orden_id':'abc',
           'mensajeria_orden_id':'abc','mensajeria_evento_id':'evt','mensajeria_total':30,
           'head_sin_cuerpo':True,
           'casos_http':[{'metodo':'POST' if n!=404 else 'GET','ruta':'/api/v1/ordenes','estado':n} for n in (201,400,404,405,409,422)]+[{'metodo':'HEAD','ruta':path,'estado':200} for path in ('/api/v1/materiales/Acero','/inventario/api/v1/materiales/Acero')]}
    pdf=[{'documento':kind,'paginas':1,'paginas_blancas':[],'desbordamientos':[],'bloques_omitidos':0,
          'markdown_sha256':pack.sha(base/kind/f'M08_{kind}.md'),'pdf_sha256':pack.sha(base/kind/f'M08_{kind}.pdf')}
         for kind in ('TEORIA','PRACTICAS')]
    for name,data in [('M08_E2E_RESULTADOS.json',e2e),('M08_SQLSERVER_RESULTADOS.json',sql),
                      ('M08_HTTP_RESULTADOS.json',smoke),('M08_WINDOWS_RESULTADOS.json',{**smoke,'mensajeria':'CUBIERTA_EN_LINUX'}),
                      ('REPORTE_PDF_M08.json',pdf)]:write(base,name,data)
    return base


class PublicacionTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(pack,'Falta implementar m08_empaquetar')
        self.assertIsNotNone(close,'Falta implementar m08_cerrar')
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.base=fixture(self.root)

    def bundle(self):
        return [pack.package(kind,root=self.root,revision=SHA) for kind in ('linux','windows','pdf')]

    def test_paquetes_y_cierre_exigen_evidencia_coherente_y_misma_revision(self):
        archives=self.bundle()
        for archive in archives:
            self.assertTrue(archive.is_file())
            with tarfile.open(archive) as tar:
                self.assertTrue(any(n.startswith('.qa/m08-certificados/') for n in tar.getnames()))
        result=close.close_module(root=self.root,revision=SHA,run_url='https://example.test/run')
        self.assertEqual(result['resultado'],'PASS')
        self.assertIn(str(pack.EXPECTED[-1]), (self.base/'CIERRE_AUTOMATIZADO.md').read_text(encoding='utf-8'))

    def test_sin_tests_no_se_puede_empaquetar(self):
        path=self.base/'M08_E2E_RESULTADOS.json';data=json.loads(path.read_text());data['resumen']['resultado']='SIN_TESTS';write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'E2E'):
            pack.package('linux',root=self.root,revision=SHA)
        self.assertFalse((self.root/'.qa/m08-artefactos/linux.tar.gz').exists())

    def test_e2e_de_otra_revision_no_puede_certificar_este_codigo(self):
        path=self.base/'M08_E2E_RESULTADOS.json';data=json.loads(path.read_text());data['commit_comprobado']='b'*40;write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'revisión'):
            pack.package('linux',root=self.root,revision=SHA)

    def test_e2e_con_hashes_de_otro_codigo_no_puede_empaquetarse(self):
        from m08_e2e_desde_practicas import manifest_sha
        path=self.base/'M08_E2E_RESULTADOS.json';data=json.loads(path.read_text())
        data['etapas'][0]['archivos']['src/Program.cs']='b'*64
        data['etapas'][0]['sha256']=manifest_sha(data['etapas'][0]['archivos'])
        write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'E2E.*código|E2E.*hash'):
            pack.package('linux',root=self.root,revision=SHA)

    def test_reto_incompleto_bloquea_paquete(self):
        path=self.base/'M08_E2E_RESULTADOS.json';data=json.loads(path.read_text());data['retos_optativos']['retos'][1]['tests_solucion']-=1;write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'reto'):
            pack.package('linux',root=self.root,revision=SHA)

    def test_codigo_mutado_despues_de_empaquetar_bloquea_cierre(self):
        self.bundle();write(self.base,f'PROYECTO/{pack.STAGES[-1]}/src/Program.cs','// cambiado\n')
        with self.assertRaisesRegex(ValueError,'hash|archivo|código'):
            close.close_module(root=self.root,revision=SHA,run_url='run')
        self.assertFalse((self.base/'CIERRE_AUTOMATIZADO.md').exists())

    def test_certificado_de_otra_revision_bloquea_cierre(self):
        self.bundle();path=self.root/'.qa/m08-certificados/windows.json';data=json.loads(path.read_text());data['commit_comprobado']='b'*40;write(self.root,str(path.relative_to(self.root)),data)
        with self.assertRaisesRegex(ValueError,'revisión'):
            close.close_module(root=self.root,revision=SHA,run_url='run')

    def test_pdf_con_bloques_omitidos_no_se_empaqueta(self):
        path=self.base/'REPORTE_PDF_M08.json';data=json.loads(path.read_text());data[1]['bloques_omitidos']=1;write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'PDF'):
            pack.package('pdf',root=self.root,revision=SHA)

    def test_smoke_sin_balanceo_comprobado_no_se_empaqueta(self):
        path=self.base/'M08_HTTP_RESULTADOS.json';data=json.loads(path.read_text());data['balanceo']='SIN_TESTS';write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'balanceo'):
            pack.package('linux',root=self.root,revision=SHA)

    def test_windows_debe_corresponder_al_codigo_publicado(self):
        path=self.base/'M08_WINDOWS_RESULTADOS.json';data=json.loads(path.read_text());data['codigo_normalizado_sha256']={'src/Program.cs':'otro'};write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'Windows|código'):
            pack.package('windows',root=self.root,revision=SHA)

    def test_certificado_incompleto_no_puede_ocultar_archivos_del_artefacto(self):
        self.bundle();path=self.root/'.qa/m08-certificados/linux.json';data=json.loads(path.read_text())
        omitted=next(key for key in data['archivos_sha256'] if key.endswith('Program.cs'))
        del data['archivos_sha256'][omitted];write(self.root,str(path.relative_to(self.root)),data)
        with self.assertRaisesRegex(ValueError,'certificado|Certificado'):
            close.close_module(root=self.root,revision=SHA,run_url='run')

    def test_metodo_no_publicado_debe_estar_comprobado(self):
        path=self.base/'M08_HTTP_RESULTADOS.json';data=json.loads(path.read_text());data['casos_http']=[row for row in data['casos_http'] if row['estado']!=405];write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'contratos HTTP'):pack.package('linux',root=self.root,revision=SHA)

    def test_head_anunciado_debe_estar_acreditado_en_el_backend_real(self):
        path=self.base/'M08_HTTP_RESULTADOS.json';data=json.loads(path.read_text());data['casos_http']=[row for row in data['casos_http'] if row['metodo']!='HEAD'];write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'HEAD'):
            pack.package('linux',root=self.root,revision=SHA)

    def test_smoke_de_otra_revision_bloquea_paquete(self):
        path=self.base/'M08_HTTP_RESULTADOS.json';data=json.loads(path.read_text());data['commit_comprobado']='b'*40;write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'revisión'):pack.package('linux',root=self.root,revision=SHA)

    def test_flags_pass_sin_resultados_concretos_no_acreditan_balanceo(self):
        path=self.base/'M08_HTTP_RESULTADOS.json';data=json.loads(path.read_text());data.pop('balanceo_instancias',None);write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'instancias|balanceo'):pack.package('linux',root=self.root,revision=SHA)

    def test_mensajeria_sin_proyeccion_real_bloquea_paquete(self):
        path=self.base/'M08_HTTP_RESULTADOS.json';data=json.loads(path.read_text());data.pop('mensajeria_evento_id',None);write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'mensajería'):pack.package('linux',root=self.root,revision=SHA)

    def test_test_omitido_aunque_conteo_total_coincida_bloquea_e2e(self):
        path=self.base/'M08_E2E_RESULTADOS.json';data=json.loads(path.read_text());data['etapas'][0]['tests_omitidos']=1;write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'omitid|TRX'):pack.package('linux',root=self.root,revision=SHA)

    def test_inventario_de_tests_incompleto_no_se_puede_certificar(self):
        path=self.base/'M08_E2E_RESULTADOS.json';data=json.loads(path.read_text());data['etapas'][0]['tests_proyectos']=[];write(self.base,path.name,data)
        with self.assertRaisesRegex(ValueError,'tests|TRX'):pack.package('linux',root=self.root,revision=SHA)


class ValidacionTests(unittest.TestCase):
    def test_fallo_de_precondicion_se_escribe_en_utf8_sin_lanzar_procesos(self):
        self.assertIsNotNone(validate,'Falta implementar m08_validar')
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);base=root/'M08_API_GATEWAY';base.mkdir()
            original=Path.write_text
            def locale_windows(path,data,encoding=None,errors=None,newline=None):
                return original(path,data,encoding=encoding or 'cp1252',errors=errors,newline=newline)
            with patch.dict(os.environ,{'GITHUB_SHA':SHA},clear=True), patch.object(validate,'ROOT',root), \
                 patch.object(validate,'BASE',base), patch.object(validate.subprocess,'run') as process, \
                 patch.object(Path,'write_text',locale_windows), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(validate.main(),1)
            process.assert_not_called()
            report=json.loads((base/'M08_SQLSERVER_RESULTADOS.json').read_bytes().decode('utf-8'))
            self.assertEqual(report['resultado'],'FAIL')
            self.assertIn('conexión',report['error'])

if __name__=='__main__':unittest.main()
