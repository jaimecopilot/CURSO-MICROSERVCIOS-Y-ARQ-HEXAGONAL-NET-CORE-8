"""Diagramas exactos del módulo 4. Ejecutar desde cualquier carpeta con Python y CairoSVG."""
from pathlib import Path
from xml.sax.saxutils import escape
import math
import textwrap
import cairosvg

ROOT=Path(__file__).resolve().parents[2]/'M04_PATRONES_ARQUITECTURA'
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
 a.extend(['</defs>',f'<rect width="{W}" height="{H}" rx="20" fill="#F8FAFC"/>','<rect x="38" y="31" width="7" height="62" rx="3" fill="#147E92"/>',text(65,65,title,28,NAVY,True,'start'),text(65,102,subtitle,18,GRAY,False,'start'),'<line x1="45" y1="128" x2="1175" y2="128" stroke="#D3E1EB"/>'])
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
'4-1-puerto':dict(title='Repository: contrato dentro, detalle fuera',subtitle='Las flechas indican dependencias de código, no llamadas SQL.',nodes=[
 N('caso','Caso de uso','Depende del puerto',70,225,330,150,'green'),N('puerto','IOrdenTrabajoRepositorio','Contrato en Aplicación',455,225,330,150,'teal'),N('sql','Adaptador EF Core','Implementa el puerto',455,465,330,150,'gold')],edges=[('caso','puerto','usa'),('sql','puerto','implementa')],footer='El núcleo declara qué necesita. La infraestructura decide cómo acceder a SQL Server. El puerto no expone DbContext.'),
'4-1-lecturas':dict(title='Entidad y proyección responden preguntas distintas',subtitle='La forma del contrato depende de las necesidades de cada caso de uso.',nodes=[
 N('escritura','Operación de negocio','Finalizar una orden',65,195,325,150,'green'),N('entidad','OrdenHexagonal','Protege invariantes y estado',455,195,325,150,'teal'),N('lectura','Consulta de lista','Mostrar identificador y estado',65,435,325,150,'blue'),N('dto','Proyección de lectura','Solo los datos necesarios',455,435,325,150,'teal'),N('almacen','Persistencia','Consultas y mapeo internos',855,310,300,170,'gold')],edges=[('escritura','entidad','reglas'),('lectura','dto','selección'),('entidad','almacen','', 'teal'),('dto','almacen','', 'teal')],footer='Un JOIN puede servir al contrato. Una proyección de aplicación no debe depender de DTOs definidos en la API.'),
'4-1-confirmacion':dict(title='Preparar cambios y confirmarlos son pasos distintos',subtitle='M3 conserva confirmación inmediata; M4 añade un flujo de trabajo diferido.',nodes=[
 N('alta3','Repositorio heredado','AgregarAsync',80,205,300,150,'blue'),N('save3','Guardado inmediato','SaveChangesAsync',470,205,300,150,'gold'),N('alta4','Repositorio de trabajo','AgregarAsync: estado Added',80,450,300,150,'green'),N('uow','IUnitOfWork','CommitAsync',470,450,300,150,'teal'),N('save4','Guardado conjunto','Mismo contexto compartido',860,450,300,150,'gold')],edges=[('alta3','save3','confirma'),('alta4','uow','prepara'),('uow','save4','confirma')],footer='Un repositorio que confirma por su cuenta no permite coordinar cambios pendientes con la unidad de trabajo de M4.'),
'4-2-compartida':dict(title='Una unidad de trabajo requiere un contexto compartido',subtitle='Instancias del mismo ámbito de petición o de operación.',nodes=[
 N('caso','OrdenesTransaccionales','Decide cuándo confirmar',440,175,340,130,'green'),N('repo','Repositorio de trabajo','Agrega sin SaveChanges',100,355,360,120,'teal'),N('uow','EfUnitOfWork','CommitAsync',760,355,360,120,'teal'),N('ctx','HexagonalDbContext','Una instancia scoped',440,525,340,125,'gold')],edges=[('caso','repo','prepara','teal','bottom'),('caso','uow','confirma','teal','bottom'),('repo','ctx','comparte','teal','bottom'),('uow','ctx','comparte','teal','bottom')],footer='Dos contextos independientes no comparten una transacción solo porque sus clases estén registradas como scoped.'),
'4-2-transaccion':dict(title='Transacción explícita: dos salidas de persistencia',subtitle='Guardar dentro de la transacción todavía no confirma el commit final.',nodes=[
 N('inicio','BeginTransactionAsync','Abre la transacción',70,210,300,145,'blue'),N('guardar','SaveChangesAsync','Escribe dentro de la transacción',460,210,300,145,'gold'),N('commit','CommitAsync','Hace duraderos los cambios',855,210,300,145,'green'),N('error','Fallo de la operación','No anunciar éxito',460,455,300,145,'red'),N('rollback','RollbackAsync','Revierte la transacción abierta',855,455,300,145,'red')],edges=[('inicio','guardar','trabajo'),('guardar','commit','éxito'),('guardar','error','fallo','red'),('error','rollback','revertir','red')],footer='Con una sola llamada a SaveChanges suele bastar la transacción implícita relacional. Revertir SQL no restaura objetos en memoria.'),
'4-2-limites':dict(title='La transacción local tiene una frontera',subtitle='Los efectos externos necesitan garantías explícitas de entrega y recuperación.',nodes=[
 N('orden','Orden','Cambio de negocio',110,230,350,120,'green'),N('outbox','Outbox','Hecho pendiente de publicar',110,440,350,120,'teal'),N('pub','Publicador','Lee y envía lo pendiente',650,235,420,130,'blue'),N('externo','Broker o correo','Efecto fuera de SQL',650,450,420,130,'gold')],edges=[('outbox','pub','después de commit','teal'),('pub','externo','envía')],bands=[(65,175,440,435,'Transacción SQL local','green'),(600,175,530,435,'Fuera de esa transacción','gold')],footer='Una saga compensa pasos; no ofrece la misma atomicidad ACID. Una notificación MediatR tampoco es un outbox persistente.'),
'4-3-solicitud':dict(title='MediatR despacha una solicitud dentro del proceso',subtitle='El mensaje une al adaptador con un manejador sin referenciar su clase concreta.',nodes=[
 N('http','Adaptador HTTP','Crea el comando',65,205,300,150,'blue'),N('send','ISender.Send','Resuelve la solicitud',460,205,300,150,'teal'),N('handler','CrearOrdenHandler','Ejecuta el caso de uso',855,205,300,150,'green'),N('puertos','Puertos de trabajo','Repositorio + unidad',855,460,300,150,'gold')],edges=[('http','send','mensaje'),('send','handler','un handler'),('handler','puertos','coordina')],footer='Send devuelve Task<T>. Repetir el envío puede repetir efectos: MediatR no añade deduplicación ni entrega exactamente una vez.'),
'4-3-mensajes':dict(title='Solicitud y notificación tienen contratos diferentes',subtitle='Command y Query usan Send; una notificación se distribuye con Publish.',nodes=[
 N('sol','IRequest<T>','Una solicitud con respuesta',90,210,420,145,'blue'),N('hs','IRequestHandler','Un manejador apropiado',710,210,420,145,'green'),N('not','INotification','Un hecho sin respuesta tipada',90,450,420,145,'teal'),N('hn','INotificationHandler','Cero, uno o varios receptores',710,450,420,145,'gold')],edges=[('sol','hs','Send'),('not','hn','Publish')],footer='La notificación es local al proceso. La estrategia predeterminada espera a los receptores secuencialmente y puede fallar.'),
'4-3-pipeline':dict(title='El pipeline puede detener una solicitud antes del caso de uso',subtitle='Ejemplo de composición: registro, validación y manejador.',nodes=[
 N('log','LoggingBehavior','Registra inicio y resultado',55,205,300,145,'blue'),N('val','ValidationBehavior','Ejecuta validadores',460,205,300,145,'teal'),N('h','Manejador','Ejecuta reglas y persistencia',865,205,300,145,'green'),N('fail','Fallo de validación','Excepción traducida o Result tipado',460,460,300,155,'red')],edges=[('log','val','next()'),('val','h','válido'),('val','fail','inválido','red')],footer='Los comportamientos se anidan según su registro. La práctica usa logging; las variantes de validación se estudian por separado.'),
'4-4-estados':dict(title='Result representa dos estados excluyentes',subtitle='El estado determina qué información puede consumir el llamador.',nodes=[
 N('r','Result<T>','EsExito / IsSuccess',425,180,370,130,'teal'),N('ok','Éxito','Valor T accesible',110,435,420,160,'green'),N('ko','Fallo esperado','Error con tipo y descripción',690,435,420,160,'red')],edges=[('r','ok','sí','green'),('r','ko','no','red')],footer='Leer el valor de un fallo es un error de programación. Las excepciones inesperadas y la cancelación mantienen su canal propio.'),
'4-4-http':dict(title='El adaptador traduce conceptos de aplicación a HTTP',subtitle='Correspondencia de los endpoints de órdenes de la práctica final.',nodes=[
 N('val','Validación','Entrada rechazada',65,190,330,130,'red'),N('nf','No encontrado','Identidad ausente',65,375,330,130,'gold'),N('cf','Conflicto','Transición no permitida',65,550,330,100,'red'),N('400','HTTP 400','Problema de entrada',825,190,330,130,'blue'),N('404','HTTP 404','Recurso ausente',825,375,330,130,'blue'),N('409','HTTP 409','Conflicto de estado',825,550,330,100,'blue')],edges=[('val','400','traduce'),('nf','404','traduce'),('cf','409','traduce')],footer='Éxito de creación: 201 y Location. Éxito de lectura o finalización: 200. El núcleo no depende de IResult ni de números HTTP.'),
'4-4-composicion':dict(title='Tres operaciones para consumir y encadenar Result',subtitle='Cada transformación mantiene visible el canal de fallo.',nodes=[
 N('map','Map','T → U\nTransforma el valor de éxito',55,215,340,220,'blue'),N('bind','Bind','T → Result<U>\nEncadena otra operación',440,215,340,220,'teal'),N('match','Match','Éxito o fallo → U\nElige una salida común',825,215,340,220,'green'),N('corte','Cortocircuito del fallo','Map y Bind no ejecutan su delegado si el resultado ya es fallido.',235,500,750,120,'red')],edges=[],footer='BindAsync devuelve Task<Result<U>>. Una lambda async no es compatible con un Bind que espere un resultado síncrono.'),
'4-5-composicion':dict(title='La composición conecta contratos con implementaciones',subtitle='La API configura el grafo; el caso de uso recibe sus dependencias.',nodes=[
 N('api','AceriaApp.Api','Raíz de composición',65,215,320,150,'blue'),N('reg','AddPatronesOrdenes','Registros explícitos del módulo',455,215,320,150,'teal'),N('caso','Caso de uso','Recibe puertos por constructor',850,215,320,150,'green'),N('imp','Adaptadores de infraestructura','Repositorio de trabajo + EfUnitOfWork',455,455,320,170,'gold')],edges=[('api','reg','configura'),('reg','caso','construye'),('reg','imp','registra')],footer='Dominio ignora IServiceProvider. El código de negocio no busca servicios arbitrariamente en un contenedor global.'),
'4-5-ambitos':dict(title='Scoped: una instancia por ámbito de resolución',subtitle='Dos peticiones tienen dos contextos; dentro de cada petición se comparte el suyo.',nodes=[
 N('ra','Repositorio A','Trabajo de la petición A',95,235,390,110,'teal'),N('ua','Unidad A','Confirma trabajo de A',95,390,390,110,'teal'),N('ca','Contexto A','HexagonalDbContext A',95,540,390,110,'gold'),N('rb','Repositorio B','Trabajo de la petición B',730,235,390,110,'teal'),N('ub','Unidad B','Confirma trabajo de B',730,390,390,110,'teal'),N('cb','Contexto B','HexagonalDbContext B',730,540,390,110,'gold')],edges=[],bands=[(60,175,460,480,'Ámbito A','blue'),(695,175,460,480,'Ámbito B','green')],footer='Repositorio y unidad de A reciben Contexto A; repositorio y unidad de B reciben Contexto B. No ejecutar operaciones paralelas en uno.'),
'4-5-cautiva':dict(title='Un singleton no debe capturar un servicio scoped',subtitle='La duración del consumidor puede retener recursos fuera de su ámbito previsto.',nodes=[
 N('s','Singleton','Vive con el proveedor raíz',90,205,420,150,'red'),N('ctx','DbContext scoped','Vida prevista: una operación',710,205,420,150,'red'),N('worker','Servicio en segundo plano','Recibe IServiceScopeFactory',90,450,420,150,'blue'),N('scope','Ámbito por operación','Resuelve y libera el trabajo',710,450,420,150,'green')],edges=[('s','ctx','captura inválida','red'),('worker','scope','crea ámbito','green')],footer='ValidateScopes detecta dependencias cautivas. Un scoped sí puede depender de transient; revisa concurrencia y propiedad de recursos.')
}

for name,config in FIGURES.items():
 svg=draw(**config)
 target=OUT/(name+'.svg');target.write_text(svg,encoding='utf-8')
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(target.with_suffix('.png')))
 print(name)

# General map: five roles and their semantic relationships, not five stages of every request.
general=dict(title='Cinco patrones, cinco responsabilidades relacionadas',subtitle='Módulo 4 · ASP.NET Core 8 · AceriaApp',nodes=[
 N('di','Inyección de dependencias','Compone el grafo y sus ámbitos',60,190,330,150,'blue'),N('med','Mediator / MediatR','Despacha solicitudes y pipeline',445,190,330,150,'teal'),N('result','Result Pattern','Expresa éxito o fallo esperado',830,190,330,150,'green'),N('repo','Repository','Prepara y recupera entidades',250,465,330,150,'teal'),N('uow','Unit of Work','Confirma el trabajo compartido',640,465,330,150,'gold')],edges=[('di','med','conecta'),('med','result','responde'),('med','repo','caso de uso'),('repo','uow','commit')],footer='Los patrones colaboran dentro del proceso. La atomicidad local, los errores y la composición se verifican con pruebas distintas.')
svg=draw(**general);folder=ROOT/'GRAFICOS';folder.mkdir(parents=True,exist_ok=True)
target=folder/'patrones_arquitectura.svg';target.write_text(svg,encoding='utf-8');cairosvg.svg2png(bytestring=svg.encode(),write_to=str(target.with_suffix('.png')))
print('patrones_arquitectura')
