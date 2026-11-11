"""Diagramas exactos del módulo 6. Ejecutar desde cualquier carpeta con Python y CairoSVG."""
from pathlib import Path
from xml.sax.saxutils import escape
import textwrap
import cairosvg

ROOT=Path(__file__).resolve().parents[2]/'M06_COMUNICACION_MICROSERVICIOS'
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
'6-1-espera':dict(
 title='Esperar el resultado no significa bloquear un hilo',
 subtitle='Dos niveles: dependencia del flujo de negocio y programación asíncrona de E/S.',
 nodes=[N('a','Producción solicita','Necesita el dato para continuar',65,195,310,160,'blue'),N('b','Inventario responde','Consulta su propio estado',445,195,310,160,'teal'),N('c','Producción continúa','Resultado, error o cancelación',825,195,310,160,'green'),N('await','Durante await','El hilo puede atender otro trabajo mientras espera la E/S',295,465,630,140,'gold')],
 edges=[('a','b','HTTP'),('b','c','dato')],
 footer='El acoplamiento temporal permanece. HTTP/1.1 y HTTP/2 usan TCP; HTTP/3 utiliza QUIC sobre UDP.'),
'6-1-puerto':dict(
 title='El puerto separa la necesidad de los detalles HTTP',
 subtitle='La aplicación consume un contrato local; infraestructura traduce la interacción remota.',
 nodes=[N('app','Aplicación de Producción','Solicita información de material',65,200,310,155,'green'),N('p','Puerto de salida','IClienteInventario',445,200,310,155,'teal'),N('h','Adaptador HTTP','Cliente tipado\nURL, JSON, timeout',825,200,310,155,'blue'),N('db','SQL de Inventario','Datos privados del servicio',445,465,310,150,'gold'),N('inv','Inventario.Api','200 con DTO; 404 ausencia\n500 es un fallo técnico',825,465,310,150,'blue')],
 edges=[('app','p','usa'),('p','h','adapta'),('h','inv','HTTP'),('inv','db','consulta')],
 footer='El cliente dispone HttpResponseMessage y propaga CancellationToken. El dominio no necesita conocer HttpClient.'),
'6-1-carrera':dict(
 title='Consultar existencias no reserva material',
 subtitle='Ejemplo de dos planificaciones que observan el mismo stock antes de continuar.',
 nodes=[N('a','Petición A consulta','Stock observado: 10\nNecesita: 8',65,205,310,170,'blue'),N('s','Inventario','Responde 10 a ambas\nNo reserva ni descuenta',445,205,310,170,'gold'),N('b','Petición B consulta','Stock observado: 10\nNecesita: 8',825,205,310,170,'blue'),N('r','Ambas comprobaciones son verdaderas','8 ≤ 10 en cada lectura; las dos intenciones suman 16',295,470,630,140,'red')],
 edges=[('s','a','dato'),('s','b','dato')],
 footer='Para garantizar disponibilidad se necesitaría una operación autoritativa de reserva con concurrencia, fuera del alcance.'),
'6-2-contrato':dict(
 title='Un evento comunica un hecho con identidad estable',
 subtitle='Contrato público del módulo: OrdenPlanificadaV1, validado por Inventario.',
 nodes=[N('id','EventoId','Una ocurrencia\nSe conserva al reintentar',65,215,310,180,'teal'),N('dato','OrdenId y Lineas','Identidad del agregado\nMaterial y cantidad',445,215,310,180,'green'),N('v','Version = 1','Esquema y significado\nValidación del consumidor',825,215,310,180,'blue'),N('time','OcurridoEnUtc','Diagnóstico y antigüedad; no garantiza un orden global',295,480,630,135,'gold')],
 edges=[],
 footer='El inbox comprueba identidad y huella del payload. Reutilizar un identificador con otro contenido es un conflicto.'),
'6-2-outbox':dict(
 title='Outbox: conservar el hecho antes de publicarlo',
 subtitle='La intención de integración comparte el commit local con la planificación.',
 nodes=[N('sql','Transacción SQL','Estado Planificada\n+ registro de outbox',65,200,310,170,'green'),N('pub','Publicador de fondo','Lee pendiente\nConserva EventoId',445,200,310,170,'teal'),N('broker','RabbitMQ','Mensaje persistente\nCola durable y binding',825,200,310,170,'blue'),N('done','Marcar enviado','Solo después del confirm\nSi falla, se reenviará',445,470,310,155,'gold'),N('confirm','Confirm del broker','Aceptación técnica\nNo confirma el consumidor',825,470,310,155,'blue')],
 edges=[('sql','pub','lee'),('pub','broker','envía'),('broker','confirm','confirma'),('confirm','done','actualiza')],
 footer='Una caída tras el confirm y antes de la marca SQL genera reenvío. La idempotencia del receptor cubre ese duplicado.'),
'6-2-inbox':dict(
 title='Inbox: confirmar SQL antes de reconocer la entrega',
 subtitle='El ack manual permite reentrega; la transacción local evita repetir el efecto.',
 nodes=[N('msg','Mensaje recibido','BasicGetAsync\nValidar contrato',65,195,310,165,'blue'),N('sql','Commit de Inventario','Inbox + proyección\nUnicidad y huella',445,195,310,165,'green'),N('ack','Ack manual','Después del commit\nEn el canal receptor',825,195,310,165,'teal'),N('dup','Si llega otra vez','Evento ya aplicado: reconocer sin duplicar la proyección',65,475,500,145,'gold'),N('error','Tratamiento de errores','Formato o versión inválidos: DLQ\nFallo técnico: requeue',655,475,500,145,'red')],
 edges=[('msg','sql','válido'),('sql','ack','commit')],
 footer='Un commit correcto seguido de ack perdido es recuperable. La proyección registra planificación y no modifica stock.'),
'6-3-fronteras':dict(
 title='Dos transacciones locales, una propagación eventual',
 subtitle='El transporte no extiende automáticamente la atomicidad de SQL a otros servicios.',
 nodes=[N('p','SQL de Producción','Orden Planificada\n+ outbox',80,240,310,210,'green'),N('bus','Mensajería','Publicador, broker\ny receptor',455,240,310,210,'teal'),N('i','SQL de Inventario','Inbox\n+ proyección',830,240,310,210,'blue')],
 edges=[('p','bus','propaga'),('bus','i','aplica')],
 bands=[(50,180,370,400,'Transacción local A','green'),(800,180,370,400,'Transacción local B','blue')],
 footer='Saga coordina transacciones y compensaciones; no aporta atomicidad ACID global. Consultar stock tampoco reserva.'),
'6-3-hibrido':dict(
 title='Flujo híbrido: aceptación local y resultado diferido',
 subtitle='El endpoint de planificación combina una observación HTTP con un hecho que se propaga.',
 nodes=[N('q','1 · Consulta HTTP','Disponibilidad informativa\nPuede fallar o caducar',65,190,310,165,'blue'),N('save','2 · Commit local','Planificación + outbox\nTransacción de Producción',445,190,310,165,'green'),N('ret','3 · Respuesta 202','Referencia a la orden\nNo acredita consumo remoto',825,190,310,165,'blue'),N('pr','4 · Publicación de fondo','RabbitMQ con confirms\nReenvíos posibles',445,465,310,165,'teal'),N('i','5 · Proyección eventual','Inbox y efecto local\nLectura HTTP posterior',825,465,310,165,'gold')],
 edges=[('q','save','sigue'),('save','ret','202'),('save','pr','pendiente'),('pr','i','propaga')],
 footer='202 se emite tras guardar el trabajo. El flujo no implementa reserva, descuento de stock, facturación ni Event Sourcing.'),
'6-3-decision':dict(
 title='Decidir por interacción y con condiciones explícitas',
 subtitle='El ADR documenta la necesidad, la frontera y la recuperación antes de elegir un transporte.',
 nodes=[N('need','Respuesta necesaria','¿Resultado ahora\no aceptación duradera?',65,200,310,175,'blue'),N('inv','Regla de negocio','¿Qué datos deben\ncambiar juntos?',445,200,310,175,'green'),N('fail','Recuperación','¿Qué se conserva,\nreintenta y observa?',825,200,310,175,'gold'),N('adr','Decisión trazable','HTTP, eventos o flujo híbrido; plazos, contratos y criterio de revisión',295,475,630,145,'teal')],
 edges=[('need','adr','plazo','teal','bottom'),('inv','adr','frontera','teal','bottom'),('fail','adr','fallos','teal','bottom')],
 footer='No hay equivalencias automáticas: HTTP ≠ consistencia fuerte; eventos ≠ baja criticidad; frecuencia ≠ protocolo.')
}

GENERAL=dict(
 title='Comunicación entre Producción e Inventario',
 subtitle='Módulo 6 · .NET 8 · SQL Server · HTTP informativo y eventos de planificación',
 nodes=[N('p','Producción','Dominio y API heredados\nPlanificar la orden',65,185,310,170,'green'),N('http','Consulta HTTP','IClienteInventario\nStock informativo',445,185,310,170,'blue'),N('i','Inventario.Api','Catálogo propio\nNo reserva material',825,185,310,170,'blue'),N('out','Estado + outbox','Un commit SQL local\nPublicador de fondo',65,465,310,170,'green'),N('bus','RabbitMQ','Cola durable, persistencia\ny publisher confirms',445,465,310,170,'teal'),N('in','Inbox + proyección','Otro commit SQL local\nAck después de guardar',825,465,310,170,'gold')],
 edges=[('p','http','solicita'),('http','i','HTTP'),('p','out','confirma'),('out','bus','publica'),('bus','in','consume')],
 footer='OrdenPlanificadaV1 conserva EventoId. La proyección es eventual; duplicados seguros no significan entrega exactamente una vez.')


def save(name,config,folder):
    folder.mkdir(parents=True,exist_ok=True)
    svg=draw(**config)
    target=folder/(name+'.svg')
    target.write_text(svg,encoding='utf-8')
    cairosvg.svg2png(bytestring=svg.encode('utf-8'),write_to=str(target.with_suffix('.png')))
    print(target.relative_to(ROOT))


if __name__=='__main__':
    for name,config in FIGURES.items():
        save(name,config,OUT)
    save('comunicacion_microservicios',GENERAL,ROOT/'GRAFICOS')
