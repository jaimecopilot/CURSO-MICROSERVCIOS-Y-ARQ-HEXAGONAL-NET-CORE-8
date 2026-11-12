#!/usr/bin/env python3
"""Doce diagramas exactos M08, reproducibles en SVG y PNG con CairoSVG."""
from pathlib import Path
from html import escape
import textwrap
import cairosvg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'M08_API_GATEWAY/TEORIA/IMAGENES'
W, H = 1240, 790
COLORS = {'blue': ('#22588a', '#eaf2fb'), 'teal': ('#087e8b', '#e4f5f5'),
          'green': ('#217345', '#eaf7ee'), 'gold': ('#966008', '#fff5df'),
          'red': ('#aa3545', '#ffedf0')}

def txt(x, y, text, size=19, fill='#18324c', bold=False, anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="DejaVu Sans,sans-serif" font-size="{size}" fill="{fill}" font-weight="{700 if bold else 400}">{escape(text)}</text>'

def box(x, y, title, body, tone='blue', width=330, height=170):
    color, pale = COLORS[tone]
    parts = [f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" fill="{pale}" stroke="{color}" stroke-width="2"/>']
    parts.append(txt(x+width/2, y+34, title, 21, color, True))
    lines = []
    for para in body.split('\n'):
        lines.extend(textwrap.wrap(para, width=max(18, int(width/10.5))) or [''])
    for i, line in enumerate(lines):
        parts.append(txt(x+width/2, y+68+i*25, line, 18))
    assert 68 + (len(lines)-1)*25 < height-8, (title, lines)
    return ''.join(parts)

def arrow(x1,y1,x2,y2,label='',tone='teal',side='above'):
    color=COLORS[tone][0]
    # Cada segmento une tarjetas en un corredor libre; no atraviesa otras tarjetas.
    path=f'M{x1},{y1} L{x2},{y2}' if x1==x2 or y1==y2 else f'M{x1},{y1} H{(x1+x2)/2} V{y2} H{x2}'
    content=f'<path d="{path}" fill="none" stroke="{color}" stroke-width="3" marker-end="url(#{tone})"/>'
    if label:
        x=(x1+x2)/2; y=(y1+y2)/2-14
        if x1==x2: x+=13;y+=5
        content+=txt(x,y,label,15,color,True,'start' if x1==x2 else 'middle')
    return content

def render(name,title,subtitle,rows,edges,footer):
    p=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc><defs>']
    for tone,(color,_) in COLORS.items():
        p.append(f'<marker id="{tone}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{color}"/></marker>')
    p+=['</defs>', '<rect width="1240" height="790" rx="18" fill="#f8fafc"/>', '<rect x="38" y="35" width="7" height="66" rx="3" fill="#087e8b"/>',txt(65,66,title,28,bold=True,anchor='start'), txt(65,105,subtitle,18,'#526779',anchor='start'),'<line x1="45" y1="132" x2="1195" y2="132" stroke="#cbd9e5"/>']
    for edge in edges:p.append(arrow(*edge))
    for row in rows:p.append(box(*row))
    p.append('<line x1="45" y1="680" x2="1195" y2="680" stroke="#cbd9e5"/>')
    for i,line in enumerate(textwrap.wrap(footer,110)):
        p.append(txt(60,714+i*26,line,18,'#526779',anchor='start'))
    p.append(txt(1180,770,'JAIME GALLO · M08',13,'#526779',anchor='end'))
    p.append('</svg>')
    svg=''.join(p);(OUT/f'{name}.svg').write_text(svg,encoding='utf-8')
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/f'{name}.png'),output_width=1860,output_height=1185)

# Tres columnas con corredores horizontales y dos niveles con corredores verticales.
A,B,C=55,455,855
Y1,Y2=190,470
FIGURES=[
('8-1-topologia','Un contrato público, dos servicios autónomos','Los clientes usan 5100; los destinos de backend son configuración del operador.',
 [(A,Y1,'Cliente','URL pública\nhttp://localhost:5100','blue'),(B,Y1,'Gateway YARP','Selecciona ruta y cluster\nNo decide stock ni negocio','teal'),(C,Y1,'Producción · 5105','Órdenes y producción\nCasos de uso propios','green'),(B,Y2,'Inventario · 5106','Materiales y planificaciones\nPersistencia propia','green'),(A,Y2,'SQL Server / AMQP','Dependencias internas\nSin acceso desde gateway','gold')],
 [(385,275,455,275,'HTTP'),(785,275,855,275,'ruta'),(620,360,620,470,'otra ruta'),(455,555,385,555,'SQL','gold')],
 'Clientes es un ejemplo conceptual de catálogo. La ocultación de direcciones no restringe por sí sola el acceso de red.'),
('8-1-responsabilidades','La entrada técnica conserva los límites del dominio','El gateway y los servicios cooperan sin compartir las reglas del negocio.',
 [(A,Y1,'Gateway','Enrutamiento\nCorrelación y resumen HTTP','teal'),(B,Y1,'Servicio','Validación y caso de uso\nResult y contrato HTTP','green'),(C,Y1,'Infraestructura','SQL Server, RabbitMQ\nOutbox e inbox de M06','blue'),(A,Y2,'Políticas posibles','Autenticación y cuotas\nRequieren implementación','gold'),(B,Y2,'Reglas de negocio','Planificar, consultar stock\nPersistir cambios válidos','green'),(C,Y2,'Independencia','Gateway sin referencias\na dominio ni persistencia','teal')],
 [(385,275,455,275,'envía'),(785,275,855,275,'adapta'),(620,360,620,470,'ejecuta')],
 'Los indicadores del catálogo no instalan políticas. La API conserva sus decisiones aunque la petición cruce un proxy.'),
('8-1-contrato','El borde también debe conservar los resultados','Una respuesta válida mantiene estado, cuerpo, identidad y enlace al recurso.',
 [(A,Y1,'Petición','Método + cuerpo + query\nCorrelación validada','blue'),(B,Y1,'Gateway','Dirección interna fija\nUna petición al backend','teal'),(C,Y1,'API responsable','201 / 400 / 404 / 409 / 422\nSegún el caso de uso','green'),(C,Y2,'Respuesta de backend','Cuerpo del resultado\nLocation cuando procede','green'),(B,Y2,'Traducción del borde','Location accesible\nEstado y cuerpo coherentes','teal'),(A,Y2,'Cliente','Sigue el recurso publicado\nDistingue fallo y ausencia','blue')],
 [(385,275,455,275),(785,275,855,275),(1020,360,1020,470),(855,555,785,555),(455,555,385,555)],
 'Un error de transporte no equivale a stock cero. El gateway no reintenta automáticamente las escrituras.'),
('8-2-ruta-cluster','Ruta, cluster y destino responden preguntas distintas','Varias rutas pueden referirse al mismo cluster mediante ClusterId.',
 [(A,Y1,'Ruta materiales','Coincidencia de URL\n/api/v1/materiales/...','blue'),(A,Y2,'Ruta planificaciones','Coincidencia de URL\n/api/v1/planificaciones/...','blue'),(B,Y1,'Cluster inventario','Grupo de destinos\nPolíticas y destinos','teal'),(C,Y1,'Destino inventario-1','URI de backend\nhttp://127.0.0.1:5106/','green'),(B,Y2,'Referencia ClusterId','Las rutas no contienen\nel algoritmo de balanceo','gold'),(C,Y2,'Destino inventario-2','En la etapa 8.4\nhttp://127.0.0.1:5107/','green')],
 [(385,275,455,275,'ref.'),(385,555,455,310),(785,275,855,275,'destino'),(785,310,855,555)],
 'Añadir un destino no modifica el contrato público. El cluster debe existir y todas las direcciones deben ser válidas.'),
('8-2-pipeline','Registro y ejecución tienen momentos diferentes','La configuración construye endpoints; cada petición recorre el pipeline.',
 [(A,Y1,'Arranque','AddReverseProxy\nLoadFromConfig','blue'),(B,Y1,'Configuración','ReverseProxy\nRoutes y Clusters','teal'),(C,Y1,'Endpoints','MapReverseProxy\nPatrones publicados','green'),(C,Y2,'Petición entrante','Correlación y errores\nCoincidencia de ruta','blue'),(B,Y2,'Proxy','Destinos disponibles\nBalanceo y transformaciones','teal'),(A,Y2,'Backend','Recibe HTTP\nResponde el caso de uso','green')],
 [(385,275,455,275),(785,275,855,275),(1020,360,1020,470),(855,555,785,555),(455,555,385,555)],
 'MapReverseProxy sin argumentos incluye middleware estándar. Una sobrecarga con pipeline personalizado exige atención al orden.'),
('8-2-entornos','La topología cambia sin reescribir el contrato','Las rutas públicas pueden conservarse mientras los destinos varían por entorno.',
 [(A,Y1,'Rutas compartidas','Órdenes, materiales\ny planificaciones','blue'),(B,Y1,'Desarrollo local','127.0.0.1:5105\n127.0.0.1:5106','green'),(C,Y1,'Red de contenedores','Nombres DNS ASCII\nPuertos de la red interna','teal'),(A,Y2,'Control de cambios','JSON versionado\nADR y revisión','gold'),(B,Y2,'Validación','Arranque y configuración\nPrueba HTTP real','green'),(C,Y2,'Límite','No aceptar un destino\nelegido por el cliente','red')],
 [(385,275,455,275,'config.'),(785,275,855,275,'varía'),(220,470,220,360,'documenta'),(620,360,620,470,'verifica')],
 'localhost dentro de un contenedor identifica ese contenedor. Versionar configuración no autoriza a guardar credenciales.'),
('8-3-coincidencia','La selección usa criterios, no la posición del JSON','Order y la especificidad se combinan con método, host, cabeceras y query.',
 [(A,Y1,'Petición','Path y método\nValores de coincidencia','blue'),(B,Y1,'Candidatas','Patrón específico\nOtras condiciones Match','teal'),(C,Y1,'Selección','Order menor primero\nDesempate por precedencia','green'),(A,Y2,'Sin coincidencia','Ruta no publicada\nNo se envía al backend','gold'),(B,Y2,'Empate ambiguo','Configuración defectuosa\nRequiere corregir reglas','red'),(C,Y2,'Ruta elegida','Cluster y transformaciones\nDespués de seleccionar','green')],
 [(385,275,455,275),(785,275,855,275),(1020,360,1020,470,'continúa')],
 'Un entero negativo es válido para Order en YARP. El catálogo didáctico restringe sus propios valores a no negativos.'),
('8-3-transformaciones','Un alias conserva el recurso y adapta el camino','Ejemplo docente: /inventario/api/v1/materiales?pagina=1.',
 [(A,Y1,'Entrada pública','/inventario/api/v1/materiales\n?pagina=1','blue'),(B,Y1,'PathRemovePrefix','Elimina /inventario\nConserva /api/v1/materiales','teal'),(C,Y1,'RequestHeader','X-Canal = Gateway\nValor literal explícito','green'),(C,Y2,'QueryValueParameter','canal = gateway\nConserva pagina=1','gold'),(B,Y2,'Destino de Inventario','/api/v1/materiales\n?pagina=1&canal=gateway','green'),(A,Y2,'Correlación','Validada en middleware\nSin literal generated','teal')],
 [(385,275,455,275),(785,275,855,275),(1020,360,1020,470),(855,555,785,555)],
 'Las transformaciones se aplican según la lista configurada. Una cabecera fija de canal no identifica ni autentica al cliente.'),
('8-3-contrato-http','Publicar una ruta implica preservar su significado','La respuesta se contrasta con el backend, incluidos los caminos de error.',
 [(A,Y1,'Operación válida','Crear y consultar\n201 y recurso publicado','green'),(B,Y1,'Errores de contrato','400 / 404 / 409 / 422\nCuerpo original coherente','gold'),(C,Y1,'Fallo de transporte','502 u otro error técnico\nNunca éxito inventado','red'),(A,Y2,'Location','Al seguir el enlace\nse alcanza el recurso','green'),(B,Y2,'Correlación','Mismo identificador válido\nEntre gateway y servicios','teal'),(C,Y2,'Métodos y superficie','No publicar diagnósticos\nNi destinos arbitrarios','blue')],
 [(220,360,220,470,'comprueba'),(620,360,620,470,'relaciona'),(1020,360,1020,470,'delimita')],
 'Una prueba de catálogo verifica datos declarados. Un servidor real verifica la petición y respuesta que realmente circularon.'),
('8-4-balanceo','RoundRobin reparte entre destinos disponibles','Una petición se asigna a una instancia; no se envía simultáneamente a todas.',
 [(A,Y1,'Peticiones nuevas','Misma URL pública\nMismo contrato funcional','blue'),(B,Y1,'Cluster Inventario','LoadBalancingPolicy\nRoundRobin explícito','teal'),(C,Y1,'Inventario 1 · 5106','Instancia disponible\nIdentidad observable','green'),(C,Y2,'Inventario 2 · 5107','Instancia disponible\nMismos datos compartidos','green'),(B,Y2,'Persistencia','SQL Server real\nNo memoria por instancia','blue'),(A,Y2,'Capacidad','Dos procesos de Inventario\nUna dependencia compartida','gold')],
 [(385,275,455,275),(785,275,855,275,'elige'),(785,310,855,555)],
 'RoundRobin no mide CPU ni garantiza que dos solicitudes concurrentes terminen en el mismo orden en que se asignaron.'),
('8-4-salud','La salud cambia el conjunto de destinos elegibles','Sonda activa /health/ready: intervalo 1 s, timeout 1 s y umbral de 2 fallos.',
 [(A,Y1,'Disponible','Readiness satisfactoria\nPuede recibir tráfico','green'),(B,Y1,'Fallo detectado','Acumula dos fallos\nRetira el destino','red'),(C,Y1,'Recuperado','Sonda satisfactoria\nReincorpora el destino','green'),(A,Y2,'Ventana de detección','Solicitudes en curso\ntodavía pueden fallar','gold'),(B,Y2,'Ningún elegible','HealthyAndUnknown\nDevuelve 503 sin destino','red'),(C,Y2,'Vuelve el reparto','Solo peticiones nuevas\nNo repite escrituras','teal')],
 [(385,275,455,275,'falla'),(785,275,855,275,'vuelve'),(220,360,220,470,'hay demora'),(620,360,620,470,'si caen todos'),(1020,360,1020,470,'habilita')],
 'HealthyOrPanic permite volver a intentar todos si ninguno queda sano. La etapa docente evita esa política de reserva.'),
('8-4-escalado','Más réplicas no eliminan todos los límites','La arquitectura distingue el reparto HTTP de los recursos compartidos.',
 [(A,Y1,'Horizontal','Añadir instancias\nRequiere repartir tráfico','green'),(B,Y1,'Vertical','Más CPU o memoria\nCon límite de una máquina','blue'),(C,Y1,'Automático','Métricas y umbrales\nCon tiempo de reacción','teal'),(A,Y2,'Estado de aplicación','Sin sesión local exclusiva\nEscrituras consistentes','gold'),(B,Y2,'SQL y RabbitMQ','Pueden ser el cuello\nde botella compartido','gold'),(C,Y2,'Operación','Gateway redundante\nRed y capacidad verificadas','gold')],
 [(220,360,220,470),(620,360,620,470),(1020,360,1020,470)],
 'El laboratorio no despliega Kubernetes ni autoscaling. Dos instancias locales prueban reparto y recuperación, no alta disponibilidad global.')
]

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    for fig in FIGURES:render(*fig)
    print(f'{len(FIGURES)} figuras SVG y {len(FIGURES)} PNG en {OUT}')

if __name__=='__main__':main()
