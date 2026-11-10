"""Diagramas exactos del módulo 5. Ejecutar desde cualquier carpeta con Python y CairoSVG."""
from pathlib import Path
from xml.sax.saxutils import escape
import math
import textwrap
import cairosvg

ROOT=Path(__file__).resolve().parents[2]/'M05_DDD_CQRS'
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
'5-1-lenguaje':dict(title='DDD conecta vocabulario, reglas y ejemplos',subtitle='El modelo se refina con las observaciones del negocio.',nodes=[
 N('neg','Expertos de Producción','Explican qué significa planificar',65,205,310,160,'blue'),N('leng','Lenguaje ubicuo','Orden, línea, capacidad, estado',445,205,310,160,'teal'),N('mod','Modelo de dominio','Métodos y reglas con esos nombres',825,205,310,160,'green'),N('prueba','Ejemplos verificables','Borrador no puede finalizarse directamente',445,460,310,160,'gold')],edges=[('neg','leng','acuerdan'),('leng','mod','expresa'),('mod','prueba','verifica','teal','bottom')],footer='La comprensión del negocio precede a los detalles de persistencia. Una prueba de catálogo no sustituye una regla ejecutada.'),
'5-1-contextos':dict(title='Una palabra puede tener significados distintos',subtitle='Contextos delimitados: fronteras de lenguaje y de modelo.',nodes=[
 N('p','Producción','Orden = fabricación\nImplementado en M5',70,230,310,220,'green'),N('a','Aprovisionamiento','Orden = compra\nMapa conceptual',445,230,310,220,'gold'),N('c','Clientes','Cliente = expediente comercial\nMapa conceptual',820,230,310,220,'blue')],edges=[],bands=[(45,175,1130,400,'Acería: no existe un único modelo compartido de Orden','gray')],footer='Los contratos entre contextos se diseñan explícitamente. Nombrar un contexto no significa que exista un servicio desplegado.'),
'5-1-despliegue':dict(title='Contexto y despliegue son decisiones diferentes',subtitle='DDD no exige un microservicio por contexto.',nodes=[
 N('fr','Frontera de Producción','Modelo y reglas propios',430,175,360,140,'teal'),N('mono','Módulo dentro de una API','Proyectos propios\nOpción del curso',80,430,460,180,'green'),N('svc','Servicio independiente','Contrato de red y operación propia\nAlternativa futura',680,430,460,180,'gold')],edges=[('fr','mono','posible','green','bottom'),('fr','svc','posible','gold','bottom')],footer='La necesidad de autonomía de despliegue debe compensar latencia, fallos de red, seguridad y costes de operación.'),
'5-2-identidad-valor':dict(title='Identidad de entidad e igualdad por valor',subtitle='La frecuencia de cambio no decide por sí sola el tipo de objeto.',nodes=[
 N('e1','Orden · identidad A','Borrador\nTotal 20',80,205,440,155,'green'),N('e2','Orden · identidad A','Planificada\nTotal 20',700,205,440,155,'green'),N('v1','CantidadProduccion(20)','Instancia uno',80,455,440,155,'blue'),N('v2','CantidadProduccion(20)','Instancia dos\nValor equivalente',700,455,440,155,'teal')],edges=[('e1','e2','conserva identidad'),('v1','v2','igualdad por valor')],footer='Una entidad puede tener representación inmutable. Un value object no tiene identidad independiente y se reemplaza por otro valor.'),
'5-2-invariantes':dict(title='La raíz protege las reglas del conjunto',subtitle='Una línea válida no basta si el total de la orden supera su capacidad.',nodes=[
 N('op','Añadir una línea','Cantidad solicitada: 40',65,195,325,150,'blue'),N('reg','OrdenProduccion','Estado permitido\nTotal actual: 480',445,195,325,150,'teal'),N('ko','Rechazo sin mutación','480 + 40 supera 500',825,195,325,150,'red'),N('val','Entrada alternativa','Cantidad solicitada: 20',65,450,325,150,'blue'),N('ok','Nuevo estado válido','480 + 20 = 500\nLa raíz incorpora la línea',445,450,325,150,'green')],edges=[('op','reg','intención'),('reg','ko','rechaza','red'),('val','ok','acepta','green')],footer='La capacidad de 500 es una regla didáctica. La validación debe ocurrir antes de modificar la colección o anunciar éxito.'),
'5-2-persistencia':dict(title='El mapeo preserva el modelo sin definirlo',subtitle='Entidad no equivale a tabla; value object no equivale a tipo owned.',nodes=[
 N('dom','Dominio','OrdenProduccion\nLíneas y value objects',70,205,310,170,'green'),N('map','Mapeo EF Core 8','Claves, conversores\ny relaciones',445,205,310,170,'teal'),N('sql','Persistencia relacional','Tablas de orden y líneas\nColumnas de valores',820,205,310,170,'gold'),N('back','Nueva carga','Reconstruye identidad,\nvalores y relaciones',445,470,310,150,'blue')],edges=[('dom','map','traduce'),('map','sql','guarda'),('sql','back','consulta','teal','bottom')],footer='Verificar en un contexto nuevo demuestra el mapeo. La configuración de EF pertenece a infraestructura, no al dominio.'),
'5-3-orquestacion':dict(title='El caso de uso coordina y espera el commit',subtitle='Crear la entidad y añadirla al seguimiento todavía no significa guardarla.',nodes=[
 N('in','Intención de crear','Datos y CancellationToken',65,190,310,145,'blue'),N('cu','Caso de uso','Construye el agregado válido',445,190,310,145,'green'),N('repo','Repositorio','Prepara el alta',825,190,310,145,'teal'),N('ok','Resultado de éxito','Solo después del commit',445,450,310,150,'green'),N('uow','Unidad de trabajo','Confirma cambios pendientes',825,450,310,150,'gold')],edges=[('in','cu','entrada'),('cu','repo','prepara'),('repo','uow','mismo contexto'),('uow','ok','éxito')],footer='La cancelación se propaga a los puertos. Un fallo técnico de confirmación no debe transformarse en un éxito de negocio.'),
'5-3-validacion':dict(title='Tres responsabilidades de validación',subtitle='Cada nivel valida lo que conoce y el dominio mantiene su propia defensa.',nodes=[
 N('http','Adaptador HTTP','JSON y tipos\nIdentidad en la ruta',65,210,310,190,'blue'),N('app','Aplicación','Forma de la entrada\nExistencia y coordinación',445,210,310,190,'teal'),N('dom','Dominio','Capacidad total\nTransiciones válidas',825,210,310,190,'green'),N('cons','Persistencia','Restricciones y concurrencia requieren políticas adicionales',295,485,630,125,'gold')],edges=[('http','app','solicitud'),('app','dom','operación')],footer='FluentValidation ayuda con la entrada. Una validación previa no elimina las carreras ni sustituye la protección del agregado.'),
'5-3-transaccion':dict(title='Preparar cambios no abre una transacción SQL',subtitle='Alcance local de una confirmación con EF Core y proveedor relacional.',nodes=[
 N('mem','Antes del commit','Cargar, modificar y seguir\nla orden en memoria',70,220,310,185,'blue'),N('save','CommitAsync','SaveChangesAsync\nOrden y líneas',445,220,310,185,'teal'),N('db','Confirmado','Cambios duraderos\nen la base de Producción',820,220,310,185,'green'),N('out','Fuera de esta garantía','Lecturas previas y servicios remotos no quedan cubiertos automáticamente',295,485,630,125,'gold')],edges=[('mem','save','solicita'),('save','db','éxito')],footer='Si se necesitan varios guardados atómicos, hay que definir una transacción explícita. Revertir SQL no restaura objetos en memoria.'),
'5-4-caminos':dict(title='CQRS: dos modelos lógicos, un almacén posible',subtitle='La separación está en contratos, comportamiento y forma de los datos.',nodes=[
 N('cmd','Command','Intención de cambio',65,195,310,145,'blue'),N('agg','Escritura','Agregado e invariantes',445,195,310,145,'green'),N('query','Query','Solicitud de información',65,450,310,145,'blue'),N('dto','Lectura','Proyección a DTO',445,450,310,145,'teal'),N('db','Base de Producción','Mismas tablas\nSin réplica asíncrona',840,320,320,180,'gold')],edges=[('cmd','agg','maneja'),('query','dto','maneja'),('agg','db','commit'),('dto','db','consulta')],footer='CQRS no exige dos bases, Event Sourcing ni MediatR. Compartir almacén no obliga a exponer entidades como respuestas HTTP.'),
'5-4-lectura':dict(title='La consulta devuelve datos sin cambiar el negocio',subtitle='El puerto de lectura expresa una pregunta; infraestructura la proyecta.',nodes=[
 N('q','Query handler','Detalle o lista de órdenes',65,205,310,160,'blue'),N('p','Puerto de lectura','IOrdenProduccionLecturas',445,205,310,160,'teal'),N('sql','Adaptador EF Core','AsNoTracking\nProyección de columnas',825,205,310,160,'gold'),N('dto','DTO de aplicación','Identidad, estado y datos\nsegún el contrato',445,470,310,150,'green')],edges=[('q','p','invoca'),('p','sql','consulta'),('sql','dto','devuelve','teal','bottom')],footer='No se llama a commit. AsNoTracking facilita la lectura, pero la ausencia de escrituras se verifica con contrato y pruebas.'),
'5-4-dos-almacenes':dict(title='Variante conceptual: proyección asíncrona',subtitle='Este módulo no implementa outbox ni un segundo almacén de lectura.',nodes=[
 N('wr','Escritura local','Orden + evento pendiente\nen una transacción',70,205,310,180,'green'),N('pub','Publicador','Lee outbox\ny reintenta entrega',445,205,310,180,'teal'),N('rd','Proyección de lectura','Consume con idempotencia\ny actualiza la vista',820,205,310,180,'blue'),N('cost','Ventana de retraso','La lectura puede ir por detrás; observar versión y recuperar fallos',295,480,630,130,'gold')],edges=[('wr','pub','envía'),('pub','rd','propaga')],footer='Dos almacenes no mejoran un sistema por sí solos. Deben diseñarse duplicados, orden, reconstrucción y retraso tolerable.'),
'5-5-estados':dict(title='Estados reales de la orden del ejercicio',subtitle='La secuencia expresa transiciones permitidas, no un control físico de planta.',nodes=[
 N('b','Borrador','La orden nace con\nuna primera línea',65,210,310,180,'blue'),N('p','Planificada','Planificación aceptada\npor el agregado',445,210,310,180,'teal'),N('f','Finalizada','Transición final aceptada',825,210,310,180,'green'),N('ko','Transición incompatible','Se rechaza sin cambiar la orden; HTTP 409 en el adaptador',295,485,630,125,'red')],edges=[('b','p','Planificar'),('p','f','Finalizar')],footer='Finalizar un borrador directamente es inválido. Añadir líneas y sus límites también se validan mediante la raíz.'),
'5-5-agregado':dict(title='OrdenProduccion es la frontera de invariantes',subtitle='La raíz gobierna los cambios; las líneas se exponen para lectura.',nodes=[
 N('api','Caso de uso','Solicita añadir línea',60,260,300,170,'blue'),N('raiz','OrdenProduccion','Identidad, estado\ny capacidad total',450,225,310,170,'green'),N('li','LineaDeOrden','Identidad propia\nCantidad y material',450,455,310,160,'teal'),N('vo','Value objects','NombreMaterial\nCantidadProduccion',840,455,300,160,'gold')],edges=[('api','raiz','método'),('raiz','li','controla'),('li','vo','compone')],bands=[(405,165,775,475,'Agregado: total máximo didáctico de 500','green')],footer='No se modifican hijos saltándose la raíz. La relación con otros contextos se diseña con referencias y contratos explícitos.'),
'5-5-flujo':dict(title='Un recorrido vertical verificable de Producción',subtitle='DDD protege reglas; hexagonal separa dependencias; CQRS separa modelos.',nodes=[
 N('http','API de Producción','Crear, añadir línea\ny cambiar estado',65,185,310,155,'blue'),N('app','Aplicación','Casos de uso\ny commands',445,185,310,155,'teal'),N('dom','Dominio','Orden y líneas\nInvariantes',825,185,310,155,'green'),N('lect','Consulta posterior','Query y DTO\nsin seguimiento',65,455,310,155,'blue'),N('db','Infraestructura','Repositorio y unidad\nBase de Producción',445,455,310,155,'gold')],edges=[('http','app','intención'),('app','dom','reglas'),('app','db','confirma'),('lect','db','lee')],footer='La prueba HTTP verifica 201, lectura del recurso y fallos 400/404/409. Los catálogos describen, el flujo ejecutado comprueba.')
}

for name,config in FIGURES.items():
 svg=draw(**config)
 target=OUT/(name+'.svg');target.write_text(svg,encoding='utf-8')
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(target.with_suffix('.png')))
 print(name)

general=dict(title='DDD, arquitectura hexagonal y CQRS en Producción',subtitle='Módulo 5 · .NET 8 · Un contexto implementado dentro de una API compartida',nodes=[
 N('ddd','DDD estratégico','Frontera y lenguaje\ndel contexto',60,190,310,160,'blue'),N('app','Aplicación hexagonal','Casos de uso y puertos\nCommands y queries',445,190,310,160,'teal'),N('dom','DDD táctico','Agregado, entidades\nvalue objects e invariantes',830,190,310,160,'green'),N('read','Modelo de lectura','DTOs y proyecciones\nsin seguimiento',250,460,310,160,'blue'),N('infra','Persistencia local','EF Core y unidad de trabajo\nMismo almacén para CQRS',640,460,310,160,'gold')],edges=[('ddd','app','orienta'),('app','dom','coordina'),('app','read','consulta'),('infra','dom','mapea','teal','bottom'),('read','infra','lee')],footer='Borrador → Planificada → Finalizada. La raíz controla líneas y capacidad. Otros contextos e integración distribuida son conceptuales.')
svg=draw(**general);folder=ROOT/'GRAFICOS';folder.mkdir(parents=True,exist_ok=True)
target=folder/'ddd_cqrs.svg';target.write_text(svg,encoding='utf-8')
cairosvg.svg2png(bytestring=svg.encode(),write_to=str(target.with_suffix('.png')))
print('ddd_cqrs')
