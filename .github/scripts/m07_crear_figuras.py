"""Diagramas exactos del módulo 7. Ejecutar desde cualquier carpeta con Python y CairoSVG."""
from pathlib import Path
from xml.sax.saxutils import escape
import textwrap
import cairosvg

ROOT=Path(__file__).resolve().parents[2]/'M07_OBSERVABILIDAD_RESILIENCIA'
OUT=ROOT/'TEORIA/IMAGENES'
OUT.mkdir(parents=True,exist_ok=True)
W,H=1220,760
COL={'blue':('#247397','#EBF3F9'),'green':('#177D65','#E7F6EE'),'gold':('#98621C','#FEF5E9'),'teal':('#147E92','#E7F6F6'),'red':('#A23D48','#FFF0F1'),'gray':('#526779','#F1F5F8')}
NAVY='#17314A';GRAY='#526779'

def text(x,y,value,size=19,color=NAVY,bold=False,anchor='middle'):
 return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>'

def lines(x,y,value,width,size=19,color=NAVY,bold=False,anchor='middle',step=27):
 # Conservative text wrapping, including code identifiers that otherwise overflow cards.
 limit=max(10,int(width/(size*.60)))
 rows=[]
 for paragraph in value.split('\n'):
  rows.extend(textwrap.wrap(paragraph,limit,break_long_words=True,break_on_hyphens=False) or [''])
 return ''.join(text(x,y+i*step,row,size,color,bold,anchor) for i,row in enumerate(rows))

def node(id,title,detail,x,y,w=330,h=130,tone='blue'):
 return {'id':id,'title':title,'detail':detail,'x':x,'y':y,'w':w,'h':h,'tone':tone}

def card(n):
 x,y,w,h=(n[k] for k in ('x','y','w','h'));color,pale=COL[n['tone']]
 title_rows=textwrap.wrap(n['title'],max(10,int((w-30)/12)),break_long_words=True,break_on_hyphens=False)
 a=[f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" fill="{pale}" stroke="{color}" stroke-width="2"/>',f'<rect x="{x}" y="{y}" width="7" height="{h}" rx="3" fill="{color}"/>']
 for i,row in enumerate(title_rows):a.append(text(x+w/2,y+32+i*25,row,20,color,True))
 detail_y=y+37+len(title_rows)*25
 a.append(lines(x+w/2,detail_y,n['detail'],w-35,17,NAVY,step=24))
 return ''.join(a)

def connector(ns,src,dst,label='',color='teal',side=None,dash=False):
 a,b=ns[src],ns[dst]
 ax,ay=a['x']+a['w']/2,a['y']+a['h']/2
 bx,by=b['x']+b['w']/2,b['y']+b['h']/2
 if side=='bottom' or abs(by-ay)>abs(bx-ax)*.65:
  x1=ax;y1=a['y']+a['h'] if by>ay else a['y'];x2=bx;y2=b['y'] if by>ay else b['y']+b['h']
  mid=(y1+y2)/2;path=f'M{x1},{y1} V{mid} H{x2} V{y2}'
  lx=(x1+x2)/2;ly=mid-9
 else:
  x1=a['x']+a['w'] if bx>ax else a['x'];y1=ay;x2=b['x'] if bx>ax else b['x']+b['w'];y2=by
  mid=(x1+x2)/2;path=f'M{x1},{y1} H{mid} V{y2} H{x2}'
  lx=mid;ly=(y1+y2)/2-10
 stroke=COL[color][0]
 s=f'<path d="{path}" fill="none" stroke="{stroke}" stroke-width="3" marker-end="url(#{color})"'+(' stroke-dasharray="8 6"' if dash else '')+'/>'
 if label:
  s+=f'<rect x="{lx-len(label)*3.8-6}" y="{ly-17}" width="{len(label)*7.6+12}" height="23" rx="5" fill="#F8FAFC"/>'
  s+=text(lx,ly,label,13,stroke)
 return s

def canvas(title,subtitle):
 a=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc><defs>']
 for name,(color,_) in COL.items():a.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{color}"/></marker>')
 a.extend(['</defs>',f'<rect width="{W}" height="{H}" fill="white"/>',f'<rect width="{W}" height="{H}" rx="20" fill="#F8FAFC"/>','<rect x="38" y="31" width="7" height="62" rx="3" fill="#147E92"/>',text(65,65,title,28,NAVY,True,'start'),text(65,102,subtitle,18,GRAY,False,'start'),'<line x1="45" y1="128" x2="1175" y2="128" stroke="#D3E1EB"/>'])
 return a

def draw(title,subtitle,nodes,edges,footer,bands=()):
 a=canvas(title,subtitle)
 for x,y,w,h,label,tone in bands:
  color,pale=COL[tone]
  a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="19" fill="{pale}" fill-opacity="0.45" stroke="{color}" stroke-width="1.5" stroke-dasharray="6 5"/>')
  a.append(text(x+18,y+27,label,17,color,True,'start'))
 ns={n['id']:n for n in nodes}
 for edge in edges:a.append(connector(ns,*edge))
 for n in nodes:a.append(card(n))
 a.extend(['<line x1="45" y1="670" x2="1175" y2="670" stroke="#D3E1EB"/>',lines(60,701,footer,1100,17,GRAY,anchor='start',step=25),'</svg>'])
 return ''.join(a)

def N(id,title,detail,x,y,w=330,h=130,tone='blue'):return node(id,title,detail,x,y,w,h,tone)

FIGURES={
'7-1-estructurado':dict(
 title='Un evento conserva plantilla, valores y contexto',
 subtitle='Las propiedades se pueden consultar sin reconstruirlas desde una frase.',
 nodes=[N('template','Plantilla estable','Orden {OrdenId} creada con {CantidadLineas} líneas',65,195,310,175,'blue'),N('values','Valores tipados','OrdenId: identidad técnica\nCantidadLineas: número',445,195,310,175,'teal'),N('event','Evento JSON','Nivel + plantilla\nPropiedades + contexto',825,195,310,175,'green'),N('query','Pregunta operativa','Buscar una orden, filtrar un nivel o comparar una duración',295,465,630,145,'gold')],
 edges=[('template','values','asocia'),('values','event','serializa'),('event','query','consulta')],
 footer='La interpolación previa pierde campos estructurados. El JSON no justifica copiar objetos completos o datos privados.'),
'7-1-correlacion':dict(
 title='Validar antes de propagar la correlación',
 subtitle='Cada petición conserva un alcance independiente, incluso cuando hay concurrencia.',
 nodes=[N('input','Cabecera de entrada','Un único valor\nX-Correlation-ID',65,190,310,170,'blue'),N('valid','Validación','1–64 caracteres ASCII\nLetras, dígitos, - y _',445,190,310,170,'gold'),N('scope','Contexto de petición','Válido: conservar\nInválido: generar nuevo',825,190,310,170,'green'),N('response','Respuesta y logs','Usan el identificador efectivo de ese contexto',65,465,310,160,'teal'),N('handler','Handler HTTP','Añade el valor validado a la llamada de Inventario',825,465,310,160,'blue'),N('remote','Inventario','Recibe el identificador y crea su propio alcance',445,465,310,160,'teal')],
 edges=[('input','valid','lee'),('valid','scope','decide'),('scope','handler','propaga'),('handler','remote','HTTP')],
 footer='El handler usa el contexto validado: no usa una cabecera arbitraria ni un campo estático compartido.'),
'7-1-datos':dict(
 title='El resumen HTTP selecciona información suficiente',
 subtitle='Una lista explícita de campos conserva diagnóstico sin copiar la petición completa.',
 nodes=[N('request','Petición HTTP','Método, ruta, cabeceras, query y cuerpo',65,220,310,200,'blue'),N('safe','Campos permitidos','Servicio y correlación\nTraceId, método, plantilla\nEstado y duración',445,220,310,200,'green'),N('log','Salida JSON','Evento final seguro\nPropiedades consultables',825,220,310,200,'teal'),N('deny','Campos excluidos','Cuerpos, query strings, Authorization y mensajes libres de excepciones',295,485,630,135,'red')],
 edges=[('request','safe','selecciona'),('safe','log','registra')],
 footer='CamposHttpSeguros elimina RequestPath del scope. Los logs heredados de workers M6 y EF no se auditan aquí.'),
'7-2-sondas':dict(
 title='Tres preguntas operativas diferentes',
 subtitle='Los nombres de las rutas no sustituyen la selección de comprobaciones y sus umbrales.',
 nodes=[N('live','Liveness','¿Responde el proceso?\nSin SQL ni RabbitMQ',65,205,310,180,'green'),N('ready','Readiness','¿Accede a dependencias críticas habilitadas?',445,205,310,180,'blue'),N('start','Startup','¿Terminó el arranque?\nMargen con límite de fallos',825,205,310,180,'gold'),N('restart','Reinicio','Acción posible de la plataforma ante fallo de live',65,465,310,155,'green'),N('traffic','Tráfico','Retirar o reincorporar instancia según ready',445,465,310,155,'blue'),N('delay','Arranque','Retrasar otras sondas; reiniciar si agota el umbral',825,465,310,155,'gold')],
 edges=[('live','restart','política'),('ready','traffic','política'),('start','delay','política')],
 footer='En el curso se implementan live y ready. Una caída de SQL degrada ready sin hacer fallar live.'),
'7-2-dependencias':dict(
 title='Readiness comprueba recursos reales y acotados',
 subtitle='RabbitMQ forma parte de la comprobación cuando están habilitados los workers.',
 nodes=[N('ready','/health/ready','Selecciona checks de disponibilidad',445,165,310,140,'blue'),N('sql','SQL Server','Abrir conexión\nConsulta real\nTimeout y cancelación',65,370,310,200,'green'),N('amqp','RabbitMQ habilitado','Abrir conexión AMQP\nLiberar recursos\nTimeout y cancelación',825,370,310,200,'teal'),N('public','Respuesta pública','Estado, componente y duración\nSin detalles internos ni secretos',445,455,310,170,'gold')],
 edges=[('ready','sql','siempre'),('ready','amqp','workers activos')],
 footer='Acceso a dependencias no equivale a vaciar outbox o inbox. La respuesta aplica una lista de campos permitidos.'),
'7-2-balanceador':dict(
 title='Readiness guía nuevas asignaciones de tráfico',
 subtitle='El balanceador aplica su intervalo y umbrales; la transición no es instantánea.',
 nodes=[N('lb','Balanceador','Consulta cada instancia\nAplica umbrales',65,330,310,175,'blue'),N('one','Instancia A: 200','Lista para el tráfico según sus comprobaciones',445,180,310,165,'green'),N('two','Instancia B: 503','Viva, pero no lista\nDependencia inaccesible',445,455,310,165,'red'),N('yes','Recibe tráfico','Tras cumplir el criterio de disponibilidad',825,180,310,165,'green'),N('no','Se retira del grupo','Peticiones en curso todavía pueden fallar',825,455,310,165,'gold')],
 edges=[('lb','one','sondea'),('lb','two','sondea'),('one','yes','admite'),('two','no','retira')],
 footer='Una dependencia compartida puede afectar a todas las instancias. Las sondas no crean capacidad ni recuperan SQL.'),
'7-3-clasificacion':dict(
 title='Clasificar antes de traducir a HTTP',
 subtitle='El estado público refleja el significado del resultado y conserva los contratos existentes.',
 nodes=[N('result','Resultado esperado','Validación, ausencia\nConflicto o regla de negocio',65,200,310,185,'green'),N('remote','Indisponibilidad remota','Sin dato fiable de Inventario\nContrato técnico conocido',445,200,310,185,'gold'),N('unknown','Fallo inesperado','Excepción del flujo HTTP\nSin respuesta iniciada',825,200,310,185,'red'),N('known','Result → HTTP','400 / 404 / 409 / 422\nSegún contrato de la API',65,465,310,155,'green'),N('unavailable','HTTP 503','No significa ausencia\nNi stock igual a cero',445,465,310,155,'gold'),N('problem','HTTP 500','ProblemDetails genérico\nCon correlación',825,465,310,155,'red')],
 edges=[('result','known','traduce'),('remote','unavailable','traduce'),('unknown','problem','gestiona')],
 footer='Cancelación del usuario y respuesta ya iniciada tienen tratamiento específico: no se fabrica otro 500.'),
'7-3-pipeline':dict(
 title='Un límite HTTP puede gestionar lo que lo atraviesa',
 subtitle='La correlación precede al manejador; solo se escribe un documento de respuesta.',
 nodes=[N('corr','Correlación','Valida y establece el identificador de petición',65,195,310,175,'teal'),N('handler','UseExceptionHandler','Usa IExceptionHandler\nObserva fallos posteriores',445,195,310,175,'blue'),N('endpoint','Endpoint','Ejecuta el caso de uso\nPuede devolver Result',825,195,310,175,'green'),N('started','Si ya empezó la respuesta','No reemplazar cabeceras ni anexar otro documento JSON',65,465,500,155,'red'),N('write','Si puede responder','Error genérico, estado y correlación; sin detalles internos',655,465,500,155,'gold')],
 edges=[('corr','handler','entra'),('handler','endpoint','continúa'),('endpoint','write','si falla')],
 footer='El manejador no repara un proceso terminado ni revierte por sí solo un commit que ya se realizó.'),
'7-3-problem':dict(
 title='El error público y el diagnóstico tienen límites',
 subtitle='ProblemDetails sigue RFC 9457 y debe concordar con el estado HTTP del transporte.',
 nodes=[N('http','Respuesta HTTP','500\napplication/problem+json',65,205,310,190,'blue'),N('body','Campos públicos','type y title\nstatus = 500\ncorrelationId / traceId',445,205,310,190,'green'),N('team','Diagnóstico interno','Buscar por correlación\nTipo de fallo permitido',825,205,310,190,'teal'),N('private','Información excluida','Mensaje arbitrario, stack trace, credenciales, SQL y rutas internas',295,485,630,135,'red')],
 edges=[('http','body','incluye'),('body','team','relaciona')],
 footer='detail e instance son opcionales. Un título público genérico no impide localizar el incidente por su identidad.'),
'7-4-decision':dict(
 title='Reintentar requiere método seguro y fallo transitorio',
 subtitle='La clasificación preserva cancelación, respuestas definitivas y el límite de intentos.',
 nodes=[N('method','¿Consulta admitida?','El curso usa GET\nMutantes: no retry',65,195,310,175,'blue'),N('failure','¿Fallo transitorio?','408 / 429 / 5xx\nTransporte o timeout de intento',445,195,310,175,'gold'),N('budget','¿Queda presupuesto?','Máximo dos reintentos\nTotal de seis segundos',825,195,310,175,'teal'),N('stop','Terminar sin otro envío','400 / 401 / 403 / 404, cancelación, circuito abierto o límite agotado',65,465,500,155,'red'),N('retry','Nuevo intento','Espera exponencial con jitter\nEl destino puede haberse recuperado',655,465,500,155,'green')],
 edges=[('method','failure','sí'),('failure','budget','sí'),('budget','retry','sí'),('method','stop','no')],
 footer='Los criterios son acumulativos: un fallo transitorio no autoriza repetir una escritura ni ignorar la cancelación.')
}

def arrow(path,label,x,y,tone='teal'):
 color=COL[tone][0]
 return f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#{tone})"/>'+text(x,y,label,17,color,True)

def circuit():
 a=canvas('El circuito conserva estado entre peticiones','Ventana: 10 s · Mínimo: 4 muestras · Ratio de fallo: 0,5 · Apertura: 5 s')
 for n in [N('closed','Cerrado','Permite intentos\nCuenta resultados',65,230,310,170,'green'),N('open','Abierto','Rechaza sin envío\nFalla rápido',445,230,310,170,'red'),N('half','Semiabierto','Una llamada prueba si el destino se recuperó',825,230,310,170,'gold')]:a.append(card(n))
 a.append(arrow('M375,275 H445','umbral',410,255,'red'))
 a.append(arrow('M755,275 H825','5 s + llamada',790,215,'gold'))
 a.append(arrow('M980,400 V470 H600 V400','Prueba falla: vuelve a abrir',790,500,'red'))
 a.append(arrow('M1060,400 V575 H220 V400','Prueba correcta: vuelve a cerrar',630,605,'green'))
 a.append(text(610,160,'Ejemplo de apertura: 200, 503, 200, 503 dentro de la ventana',20,NAVY,True))
 a.extend(['<line x1="45" y1="670" x2="1175" y2="670" stroke="#D3E1EB"/>',text(60,703,'Esperar cinco segundos no envía una sonda por sí solo; hace falta una nueva llamada.',17,GRAY,False,'start'),'</svg>'])
 return ''.join(a)

def budget():
 a=canvas('Un presupuesto exterior contiene intentos y esperas','Orden Polly v8: total → retry → circuito → intento → transporte HTTP')
 boxes=[(60,160,1100,465,'Timeout total: 6 segundos','blue'),(105,230,1010,355,'Retry: 2 reintentos · 200 ms base · exponencial + jitter','teal'),(150,300,920,245,'Circuito compartido: decide si admite cada intento','gold'),(195,370,830,135,'Timeout de intento: 1 segundo','green')]
 for x,y,w,h,label,tone in boxes:
  color,pale=COL[tone]
  a.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{pale}" stroke="{color}" stroke-width="2"/>')
  a.append(text(x+23,y+35,label,20,color,True,'start'))
 a.append(text(610,467,'HttpClient usa el token recibido para la operación de E/S',20,NAVY))
 a.extend(['<line x1="45" y1="670" x2="1175" y2="670" stroke="#D3E1EB"/>',lines(60,701,'El total limita también Retry-After. Cancelación del usuario termina antes; los timeouts requieren cooperación del trabajo.',1100,17,GRAY,anchor='start',step=25),'</svg>'])
 return ''.join(a)

def main():
 sources={key:draw(**spec) for key,spec in FIGURES.items()}
 sources['7-4-circuito']=circuit();sources['7-4-presupuesto']=budget()
 assert len(sources)==12
 for name,svg in sources.items():
  (OUT/f'{name}.svg').write_text(svg,encoding='utf-8')
  cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/f'{name}.png'),output_width=W,output_height=H)
 print(f'{len(sources)} diagramas SVG y {len(sources)} PNG generados en {OUT}')

if __name__=='__main__':main()
