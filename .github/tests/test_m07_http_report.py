"""Regresiones del comprobador HTTP: rechazar evidencia incompleta o insegura."""
import contextlib,importlib.util,io,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(SCRIPTS))
spec=importlib.util.spec_from_file_location('m07_http_tests',SCRIPTS/'m07_http_real.py')
http=importlib.util.module_from_spec(spec);spec.loader.exec_module(http)
class ComprobadorHttpTests(unittest.TestCase):
    def test_informe_de_error_windows_utf8(self):
        escribir=Path.write_text
        def locale_windows(path,data,encoding=None,errors=None,newline=None):
            return escribir(path,data,encoding=encoding or 'cp1252',errors=errors,newline=newline)
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'M07_OBSERVABILIDAD_RESILIENCIA').mkdir()
            with patch.object(http,'ROOT',root),patch.object(http,'source_manifest',return_value={}),patch.object(http.sys,'argv',['m07_http_real.py','--windows']),patch.object(http.sys,'platform','win32'),patch.object(http.tempfile,'TemporaryDirectory',side_effect=RuntimeError('Conexión interrumpida después del arranque')),patch.object(Path,'write_text',locale_windows),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(1,http.main())
            report=json.loads((root/'M07_OBSERVABILIDAD_RESILIENCIA/M07_WINDOWS_RESULTADOS.json').read_bytes().decode('utf-8'))
            self.assertEqual('FAIL',report['resultado']);self.assertIn('Conexión',report['error'])
    def test_correlacion_exige_los_dos_servicios_y_plantilla(self):
        events=[{'Properties':{'CorrelationId':'abc','Servicio':s,'SourceContext':'AceriaApp.Observabilidad.ResumenPeticionMiddleware','Ruta':'/api/v1/materiales/{material}','Estado':200}} for s in ('Produccion','Inventario')]
        http.verify_correlation(events,'abc',[])
        with self.assertRaises(AssertionError):http.verify_correlation(events[:1],'abc',[])
        events[1]['Properties']['Ruta']='/api/v1/materiales/Acero'
        with self.assertRaises(AssertionError):http.verify_correlation(events,'abc',[])
    def test_ausencia_de_secretos_en_eventos_propios(self):
        events=[{'Properties':{'CorrelationId':'abc','Servicio':s,'SourceContext':'AceriaApp.Observabilidad.ResumenPeticionMiddleware','Ruta':'/ruta/{material}','Estado':200}} for s in ('Produccion','Inventario')]
        events[0]['Properties']['Dato']='sentinela'
        with self.assertRaises(AssertionError):http.verify_correlation(events,'abc',['sentinela'])
    def test_readiness_no_acepta_falso_verde_o_mensaje_interno(self):
        good={'estado':'Healthy','componentes':[{'nombre':'sql-AceriaApp','estado':'Healthy','milisegundos':1}]}
        http.verify_health(good,healthy=True)
        with self.assertRaises(AssertionError):http.verify_health(good,healthy=False)
        good['componentes'][0]['exception']='password'
        with self.assertRaises(AssertionError):http.verify_health(good,healthy=True)
    def test_docker_solo_controla_el_identificador_de_su_contenedor(self):
        with patch.dict(http.os.environ,{'ACERIA_RABBIT_CONTAINER_ID':'f'*64}),patch.object(http.subprocess,'run') as run:
            http.broker_action('stop');run.assert_called_once_with(['docker','stop','--time','3','f'*64],check=True,timeout=25)
        with patch.dict(http.os.environ,{'ACERIA_RABBIT_CONTAINER_ID':'rabbit ajeno'}),patch.object(http.subprocess,'run') as run:
            with self.assertRaises(ValueError):http.broker_action('stop')
            run.assert_not_called()
    def test_problem_details_exige_correlacion_tipo_y_ausencia_de_detalle(self):
        data={'status':500,'title':'Se ha producido un error interno.','type':'about:blank','traceId':'t','correlationId':'abc'}
        headers={'content-type':'application/problem+json','x-correlation-id':'abc'}
        http.verify_problem(data,headers,'abc')
        data['detail']='Detalle interno del fallo controlado.'
        with self.assertRaises(AssertionError):http.verify_problem(data,headers,'abc')
if __name__=='__main__':unittest.main()
