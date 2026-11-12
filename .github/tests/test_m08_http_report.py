"""Regresiones del smoke: evidencia específica y peticiones HTTP reales."""
import importlib.util,sys,unittest,threading,json
from pathlib import Path
from http.server import BaseHTTPRequestHandler,HTTPServer
SCRIPTS=Path(__file__).resolve().parents[1]/'scripts';sys.path.insert(0,str(SCRIPTS))
def load():
 p=SCRIPTS/'m08_http_real.py'
 if not p.exists():return None
 spec=importlib.util.spec_from_file_location('m08_http_tests',p)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
http=load()
class ComprobadorTests(unittest.TestCase):
 def setUp(self):self.assertIsNotNone(http,'Falta m08_http_real')
 def test_liveness_conserva_contrato_propio_gateway_y_backends(self):
  self.assertTrue(hasattr(http,'verify_liveness'),'Falta verificación de liveness por servicio')
  http.verify_liveness('gateway',{'servicio':'Gateway','estado':'vivo'})
  for name in ('produccion','inventario-1','inventario-2'):
   http.verify_liveness(name,{'estado':'Healthy','componentes':[]})
  for name,data in (('gateway',{'estado':'Healthy','componentes':[]}),('gateway',{'servicio':'Gateway','estado':'vivo','otro':'dato'}),('produccion',{'servicio':'Gateway','estado':'vivo'}),('inventario-1',{'estado':'Unhealthy','componentes':[]})):
   with self.assertRaises(AssertionError):http.verify_liveness(name,data)
 def test_correlacion_exige_gateway_y_ambos_servicios(self):
  events=[{'Properties':{'CorrelationId':'abc','Servicio':service,'SourceContext':'AceriaApp.Observabilidad.ResumenPeticionMiddleware','Ruta':'/api/v1/comunicacion/{**resto}'}} for service in ('Gateway','Produccion','Inventario')]
  http.verify_correlation(events,'abc',[])
  with self.assertRaises(AssertionError):http.verify_correlation(events[1:],'abc',[])
  events[0]['Properties']['Authorization']='secreto'
  with self.assertRaises(AssertionError):http.verify_correlation(events,'abc',['secreto'])
 def test_balanceo_exige_dos_instancias_sin_identidades_inventadas(self):
  http.verify_instances(['inventario-1','inventario-2'])
  for values in (['inventario-1']*6,['inventario-1','otro'],[]):
   with self.assertRaises(AssertionError):http.verify_instances(values)
 def test_mensajeria_exige_orden_y_total_exactos(self):
  http.verify_projection({'ordenId':'abc','cantidadTotal':30},'abc',30)
  for data in ({'ordenId':'otra','cantidadTotal':30},{'ordenId':'abc','cantidadTotal':0},{}):
   with self.assertRaises(AssertionError):http.verify_projection(data,'abc',30)
 def test_peticion_conserva_errores_http_y_headers_sin_seguir_location(self):
  class Handler(BaseHTTPRequestHandler):
   def do_GET(self):
    self.send_response(409);self.send_header('Content-Type','application/json');self.send_header('X-Instancia','inventario-1');self.end_headers();self.wfile.write(b'{"error":"conflicto"}')
   def log_message(self,*args):pass
  server=HTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
  body,headers=http.request(f'http://127.0.0.1:{server.server_port}','/caso',expected=409)
  self.assertEqual(body,{'error':'conflicto'});self.assertEqual(headers['x-instancia'],'inventario-1')
  self.assertEqual(http.request(f'http://127.0.0.1:{server.server_port}','/caso',expected=(404,409))[0],{'error':'conflicto'})
  with self.assertRaises(AssertionError):http.request(f'http://127.0.0.1:{server.server_port}','/caso',expected=200)
 def test_no_convierte_redireccion_post_en_un_get_exitoso(self):
  visits=[]
  class Handler(BaseHTTPRequestHandler):
   def do_POST(self):
    visits.append(('POST',self.path));self.send_response(302);self.send_header('Location','/destino');self.end_headers()
   def do_GET(self):
    visits.append(('GET',self.path));self.send_response(200);self.end_headers();self.wfile.write(b'{}')
   def log_message(self,*args):pass
  server=HTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
  self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
  with self.assertRaisesRegex(AssertionError,'302'):
   http.request(f'http://127.0.0.1:{server.server_port}','/origen','POST',{},expected=200)
  self.assertEqual(visits,[('POST','/origen')])
if __name__=='__main__':unittest.main()
