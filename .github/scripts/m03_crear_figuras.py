from pathlib import Path
from xml.sax.saxutils import escape
import cairosvg

BASE=Path(__file__).resolve().parents[2]/'M03_ARQUITECTURA_HEXAGONAL/TEORIA/IMAGENES'
BASE.mkdir(parents=True,exist_ok=True)
NAVY='#17314A'; BLUE='#247397'; TEAL='#147E92'; GREEN='#177D65'; GOLD='#AF752A'; GRAY='#5B7184'
PALE={'blue':'#EBF3F9','teal':'#E7F6F6','green':'#E7F6EE','gold':'#FEF5E9','gray':'#F3F6F8'}
COL={'blue':BLUE,'teal':TEAL,'green':GREEN,'gold':GOLD,'gray':GRAY}

# Every item is a named diagram with a deliberately different diagram form.
FIGURES={
'3-1-capas': ('Las capas clasifican responsabilidades','No confundas función con librería', 'column', [
 ('Presentación / API','HTTP, JSON, resultado público','blue'),('Aplicación','OrdenesCasoUso: coordina operaciones','teal'),('Dominio','OrdenHexagonal: protege reglas','green'),('Infraestructura','Repositorio SQL y configuración EF Core','gold')],
 'Un dibujo de capas explica roles; no demuestra que los .csproj respeten sus dependencias.'),
'3-1-regla': ('La regla de dependencia','El núcleo no conoce los detalles de ejecución','graph', [
 ('API','Invoca casos de uso','blue'),('Aplicación','Declara IOrdenRepositorio','teal'),('Dominio','Reglas y entidades','green'),('Infraestructura','Implementa IOrdenRepositorio','gold')],
 'Las flechas de referencia apuntan desde API/infraestructura hacia contratos internos; dominio no apunta hacia SQL.'),
'3-1-inversion': ('Inversión de dependencias','El contrato pertenece al interior','flow', [
 ('Caso de uso','Depende de interfaz','green'),('Puerto de salida','IOrdenRepositorio','teal'),('Adaptador SQL','Implementa el contrato','gold')],
 'En tiempo de ejecución se consulta SQL; en compilación la aplicación sigue dependiendo solo de una interfaz.'),
'3-2-puertos': ('Puertos y adaptadores','Dos fronteras con responsabilidades diferentes','flow', [
 ('Cliente HTTP','Envía GET / POST','blue'),('Adaptador entrada','Minimal API + DTO','blue'),('Núcleo','Caso de uso + puerto','green'),('Adaptador salida','EF Core / SQL Server','gold')],
 'El caso de uso no recibe HttpContext ni DbContext; recibe valores del negocio y un puerto de repositorio.'),
'3-2-contratos': ('Contrato estable, detalles sustituibles','Un puerto permite probar sin SQL Server','split', [
 ('Caso de uso','Recibe IOrdenRepositorio','green'),('Puerto IOrdenRepositorio','Listar / Obtener / Agregar / Guardar','teal'),('SQL Server','OrdenRepositorioSqlServer','gold'),('Doble de prueba','Memoria controlada','blue')],
 'Las dos implementaciones pueden respetar el mismo contrato y, sin embargo, tener comportamientos operativos distintos.'),
'3-2-entrada': ('Del HTTP al caso de uso','El adaptador traduce, no decide persistencia','flow', [
 ('POST JSON','Cliente + material + cantidad','blue'),('DTO de entrada','CrearOrdenHexagonalRequest','teal'),('Caso de uso','CrearAsync(...)','green'),('Puerto','AgregarAsync(OrdenHexagonal)','gold')],
 'HTTP define el protocolo de entrada; validación y persistencia pertenecen a niveles distintos de responsabilidad.'),
'3-3-proyectos': ('Referencias físicas entre proyectos','.csproj hace comprobable la dirección','graph', [
 ('AceriaApp.Api','Referencia Aplicación + Infraestructura','blue'),('Hexagonal.Aplicacion','Referencia Dominio','teal'),('Hexagonal.Dominio','Ninguna referencia externa','green'),('Hexagonal.Infraestructura','Referencia Aplicación + Dominio','gold')],
 'La dirección de ProjectReference importa: Dominio no puede referenciar AceriaApp.Api ni la infraestructura.'),
'3-3-tests': ('Una prueba por frontera','Cada test responde una pregunta distinta','split', [
 ('Dominio','¿Finalizar respeta el estado?','green'),('Aplicación','¿El caso de uso invoca el puerto?','teal'),('Infraestructura','¿EF Core guarda y recupera?','gold'),('HTTP','¿201, 400, 404 y 409 son correctos?','blue')],
 'Una prueba HTTP verde no demuestra por sí sola que todas las dependencias de compilación estén bien orientadas.'),
'3-3-despliegue': ('Capas no son microservicios','Separación de código ≠ despliegue distribuido','split', [
 ('Modular monolith','Un proceso, proyectos separados','teal'),('Microservicios','Procesos independientes + red','gold'),('Dominio','Iguales reglas en ambos','green'),('Decisión','Coste operativo y autonomía','blue')],
 'Crear cuatro proyectos .NET no genera cuatro servicios desplegados ni cuatro bases de datos.'),
'3-4-di': ('El contenedor une abstracción e implementación','Composición en el borde de la aplicación','flow', [
 ('Registro DI','AddServiciosHexagonales','blue'),('Interfaz','IOrdenRepositorio','teal'),('Implementación','OrdenRepositorioSqlServer','gold'),('Caso de uso','OrdenesCasoUso','green')],
 'Scoped asocia las dependencias de la petición; el núcleo ignora cómo se construye el adaptador SQL.'),
'3-4-recorrido': ('Un POST por toda la arquitectura','El cambio se conserva y es recuperable','flow', [
 ('HTTP POST','Validar entrada: 400 / 422','blue'),('Caso de uso','CrearAsync crea entidad','green'),('Repositorio EF','Add + SaveChanges','gold'),('HTTP 201','Location + GUID','teal')],
 'La prueba no acaba en 201: el GET de Location demuestra que el objeto creado se puede recuperar.'),
'3-4-pruebas': ('Contrato funcional y calidad de diseño','Dos tipos de evidencia complementarios','split', [
 ('E2E alumno','Construye desde el Markdown','blue'),('xUnit HTTP','Comprueba 200 / 201 / 409','teal'),('Chequeo .csproj','Verifica inversión de dependencias','green'),('PDF / SVG','Comprueba material distribuible','gold')],
 'Compilar una solución terminada no equivale a verificar que sus prácticas permiten construirla desde cero.')
}

def header(title,subtitle):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="620" viewBox="0 0 1200 620" role="img" aria-label="{escape(title)}">',
 '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10z" fill="#147E92"/></marker></defs>',
 '<rect width="1200" height="620" rx="22" fill="#F8FAFC"/>',
 '<rect x="36" y="32" width="7" height="56" rx="3" fill="#147E92"/>',
 f'<text x="62" y="64" font-family="DejaVu Sans,Arial" font-size="29" font-weight="700" fill="{NAVY}">{escape(title)}</text>',
 f'<text x="63" y="99" font-family="DejaVu Sans,Arial" font-size="18" fill="{GRAY}">{escape(subtitle)}</text>',
 '<line x1="44" y1="120" x2="1155" y2="120" stroke="#D8E6EF" stroke-width="2"/>']

def text(x,y,s,size=18,color=NAVY,weight=400,anchor='middle'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="DejaVu Sans,Arial" font-weight="{weight}" font-size="{size}" text-anchor="{anchor}">{escape(s)}</text>'

def box(x,y,w,h,title,detail,tone):
 clr=COL[tone]
 return ''.join([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="17" fill="#FFFFFF" stroke="#B7C9D5" stroke-width="1.6"/>',
 f'<rect x="{x}" y="{y}" width="{w}" height="10" rx="5" fill="{clr}"/>',
 f'<rect x="{x+10}" y="{y+22}" width="{w-20}" height="{h-39}" rx="12" fill="{PALE[tone]}"/>',
 text(x+w/2,y+64,title,19,clr,700),
 text(x+w/2,y+103,detail,15,clr,400)])

def arrow(x1,y1,x2,y2):
 return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TEAL}" stroke-width="4" marker-end="url(#arrow)"/>'

def draw(config):
 title,subtitle,kind,nodes,footer=config
 a=header(title,subtitle)
 if kind=='flow':
  count=len(nodes);gap=32;w=(1100-(count-1)*gap)/count
  for i,(h,d,tone) in enumerate(nodes):
   x=50+i*(w+gap)
   a.append(box(x,195,w,245,h,d,tone))
   if i>0:a.append(arrow(x-27,318,x-5,318))
 elif kind=='column':
  w=780;x=210;ys=[151,255,359,463]
  for i,((h,d,tone),y) in enumerate(zip(nodes,ys)):
   a.append(box(x,y,w,91,h,d,tone))
   # Cover tall card's text with custom positions to avoid overlap (replace below)
  # Alternative stacked diagrams are rendered with rows outside the prior 4 boxes
  a=header(title,subtitle)
  for i,(h,d,tone) in enumerate(nodes):
   x=180;y=150+i*104;col=COL[tone]
   a.extend([f'<rect x="{x}" y="{y}" width="850" height="88" rx="15" fill="{PALE[tone]}" stroke="{col}" stroke-width="2"/>',
     text(x+270,y+33,h,22,col,700),text(x+460,y+66,d,17,NAVY,400)])
   if i<3:a.append(arrow(605,y+89,605,y+100))
 elif kind=='split':
  w=512;h=165
  for i,(label,detail,tone) in enumerate(nodes):
   x=65+(i%2)*545;y=155+(i//2)*203
   a.append(box(x,y,w,h,label,detail,tone))
  a.append(f'<path d="M 600 343 V 372" stroke="#9CB5C5" stroke-width="3" stroke-dasharray="7 8"/>')
 elif kind=='graph':
  positions=[(65,174),(662,174),(65,382),(662,382)]
  for (label,detail,tone),(x,y) in zip(nodes,positions):a.append(box(x,y,465,166,label,detail,tone))
  a.extend([arrow(540,255,652,255), arrow(710,345,530,414), arrow(895,382,895,347)])
 else:raise ValueError(kind)
 a.extend(['<line x1="48" y1="561" x2="1152" y2="561" stroke="#D8E6EF" stroke-width="1.6"/>',
 text(60,591,footer,15,GRAY,400,anchor='start'),'</svg>'])
 svg=''.join(a)
 if len(footer)>132:print('Long footer',title,len(footer))
 return svg
for key,config in FIGURES.items():
 svg=draw(config)
 path=BASE/(key+'.svg');path.write_text(svg,encoding='utf8')
 cairosvg.svg2png(bytestring=svg.encode(),write_to=str(path.with_suffix('.png')))
 print(key,path.stat().st_size,path.with_suffix('.png').stat().st_size)
