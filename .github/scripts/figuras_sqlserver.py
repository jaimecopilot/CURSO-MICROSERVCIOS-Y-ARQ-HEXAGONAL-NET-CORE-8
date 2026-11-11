#!/usr/bin/env python3
"""Diagramas técnicos reproducibles sobre SQL Server real en las pruebas M02–M05."""
from pathlib import Path
from xml.sax.saxutils import escape
import cairosvg
from PIL import ImageFont

ROOT = Path(__file__).resolve().parents[2]
W, H = 1220, 760
NAVY, GRAY = '#17314A', '#526779'
COLORS = {
    'blue': ('#247397', '#EBF3F9'),
    'green': ('#177D65', '#E7F6EE'),
    'gold': ('#98621C', '#FEF5E9'),
    'red': ('#A23D48', '#FFF0F1'),
    'gray': ('#526779', '#F1F5F8'),
}
FONT_DIR = Path('/usr/share/fonts/truetype/dejavu')


def measure(value, size, bold=False):
    filename = 'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'
    return ImageFont.truetype(str(FONT_DIR / filename), size).getlength(value)


def rows(value, width, size, bold=False):
    output = []
    for paragraph in value.split('\n'):
        line = ''
        for word in paragraph.split():
            candidate = f'{line} {word}'.strip()
            if measure(candidate, size, bold) > width and line:
                output.append(line)
                line = word
            else:
                line = candidate
        output.append(line)
    assert all(measure(line, size, bold) <= width for line in output), output
    return output


def text(x, y, value, size=19, color=NAVY, bold=False, anchor='middle'):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
            f'font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" '
            f'font-weight="{700 if bold else 400}" fill="{color}">{escape(value)}</text>')


def card(x, y, title, detail, tone='blue', w=330, h=155):
    color, pale = COLORS[tone]
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="15" '
             f'fill="{pale}" stroke="{color}" stroke-width="2"/>']
    cursor = y + 33
    title_size = 21
    while any(measure(word, title_size, True) > w - 28 for word in title.split()):
        title_size -= 1
        assert title_size >= 17, title
    for row in rows(title, w - 28, title_size, True):
        parts.append(text(x + w / 2, cursor, row, title_size, color, True))
        cursor += 27
    cursor += 9
    for row in rows(detail, w - 30, 18):
        parts.append(text(x + w / 2, cursor, row, 18))
        cursor += 25
    assert cursor - 25 < y + h - 12, (title, cursor, y + h)
    return ''.join(parts)


def arrow(points, label='', tone='blue', dashed=False, label_pos=None):
    color = COLORS[tone][0]
    path = 'M' + ' L'.join(f'{x},{y}' for x, y in points)
    parts = [f'<path d="{path}" stroke="{color}" stroke-width="3" fill="none" '
             f'marker-end="url(#{tone})"' + (' stroke-dasharray="7 6"' if dashed else '') + '/>']
    if label:
        x, y = label_pos or ((points[0][0] + points[-1][0]) / 2,
                             (points[0][1] + points[-1][1]) / 2 - 10)
        width = measure(label, 16) + 16
        parts.append(f'<rect x="{x-width/2}" y="{y-19}" width="{width}" height="26" rx="5" fill="#F8FAFC"/>')
        parts.append(text(x, y, label, 16, color))
    return ''.join(parts)


def canvas(title, subtitle):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc><defs>']
    for name, (color, _) in COLORS.items():
        parts.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" '
                     f'markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="{color}"/></marker>')
    parts.extend(['</defs>', f'<rect width="{W}" height="{H}" rx="20" fill="#F8FAFC"/>',
                  '<rect x="38" y="31" width="7" height="62" rx="3" fill="#247397"/>',
                  text(65, 65, title, 27, NAVY, True, 'start'),
                  text(65, 103, subtitle, 18, GRAY, anchor='start'),
                  '<line x1="45" y1="130" x2="1175" y2="130" stroke="#D3E1EB"/>'])
    assert measure(title, 27, True) < W - 110
    assert measure(subtitle, 18) < W - 110
    return parts


def save(module, filename, title, subtitle, content, footer):
    parts = canvas(title, subtitle) + content
    parts.append('<line x1="45" y1="655" x2="1175" y2="655" stroke="#D3E1EB"/>')
    for index, row in enumerate(rows(footer, 1090, 18)):
        parts.append(text(65, 692 + index * 25, row, 18, GRAY, anchor='start'))
    parts.append('</svg>')
    target = ROOT / module / 'TEORIA' / 'IMAGENES' / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    svg = ''.join(parts)
    target.with_suffix('.svg').write_text(svg, encoding='utf-8')
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(target.with_suffix('.png')), scale=1.5)
    print(target.relative_to(ROOT))


def main():
    save('M02_APIS_REST_ASPNET_CORE', '2-1-sqlserver-docker',
         'La imagen se convierte en un servidor SQL real',
         'Docker ejecuta el motor; Testcontainers prepara su ciclo de vida para la prueba.', [
             card(55, 175, 'Imagen de Microsoft', 'Paquete con SQL Server 2022\nEtiqueta CU14 fijada', 'gray'),
             card(445, 175, 'Docker Engine', 'Crea un proceso aislado\nUsa contenedores Linux', 'blue'),
             card(835, 175, 'Contenedor SQL Server', 'Motor en ejecución\nEdición Express', 'green'),
             arrow([(385, 252), (445, 252)]), arrow([(775, 252), (835, 252)]),
             card(55, 440, 'Proceso de pruebas .NET', 'API de prueba + EF Core\nUseSqlServer', 'blue'),
             card(445, 440, 'Puerto del host', 'Asignación dinámica\nCadena de conexión real', 'gold'),
             card(835, 440, 'Puerto del contenedor', 'SQL escucha en 1433\nBase aislada por caso', 'green'),
             arrow([(385, 517), (445, 517)]), arrow([(775, 517), (835, 517)]),
             arrow([(1000, 330), (1000, 440)], 'escucha', label_pos=(1000, 393)),
             text(610, 387, 'Testcontainers obtiene la dirección; el test no adivina el puerto.', 19, GRAY),
         ], 'LocalDB sigue siendo el entorno de la API del alumno. El contenedor pertenece a la ejecución de tests; no emula SQL Server.')

    save('M02_APIS_REST_ASPNET_CORE', '2-1-sqlserver-aislamiento',
         'Servidor compartido, datos aislados por prueba',
         'BaseSqlServer.Crear() elige el servidor y reserva una base con nombre único.', [
             card(55, 175, 'ACERIA_TEST_SQLSERVER', 'Conexión a master\nLocalDB o servidor de CI', 'gold'),
             card(55, 430, 'Sin variable de entorno', 'Testcontainers inicia\nSQL Server con Docker', 'blue'),
             card(445, 300, 'Servidor SQL disponible', 'Motor real y conexión válida\nSi falla, falla la prueba', 'green', h=165),
             card(835, 175, 'Caso de prueba A', 'Base con GUID A\nEsquema y datos propios', 'blue'),
             card(835, 430, 'Caso de prueba B', 'Base con GUID B\nEsquema y datos propios', 'blue'),
             arrow([(385, 252), (415, 252), (415, 340), (445, 340)]),
             arrow([(385, 507), (415, 507), (415, 425), (445, 425)]),
             arrow([(775, 340), (805, 340), (805, 252), (835, 252)]),
             arrow([(775, 425), (805, 425), (805, 507), (835, 507)]),
         ], 'Cada caso elimina su propia base al terminar. Una base del curso o del alumno nunca se utiliza como destino de estas pruebas.')

    save('M03_ARQUITECTURA_HEXAGONAL', '3-4-sqlserver-adaptadores',
         'Puerto, adaptador, proveedor y motor son piezas distintas',
         'La dependencia de código apunta al puerto; la ejecución llega hasta SQL Server.', [
             card(55, 175, 'Caso de uso', 'OrdenesCasoUso\nDecide y coordina', 'green'),
             card(445, 175, 'Puerto de salida', 'IOrdenRepositorio\nContrato de aplicación', 'green'),
             card(835, 175, 'Adaptador de salida', 'OrdenRepositorioSqlServer\nImplementa el contrato', 'blue'),
             arrow([(385, 252), (445, 252)]),
             arrow([(835, 252), (775, 252)], tone='blue', dashed=True),
             text(805, 158, 'implementa', 16, GRAY),
             card(55, 440, 'Entrada HTTP', 'Endpoint Minimal API\nTraduce petición y respuesta', 'gold'),
             card(445, 440, 'Proveedor EF Core', 'UseSqlServer\nTraduce LINQ y mapeos', 'blue'),
             card(835, 440, 'Motor SQL Server', 'Ejecuta SQL y restricciones\nLocalDB o contenedor', 'gray'),
             arrow([(220, 440), (220, 330)], 'invoca', label_pos=(220, 392)),
             arrow([(1000, 330), (1000, 380), (610, 380), (610, 440)], 'usa', label_pos=(805, 372)),
             arrow([(775, 517), (835, 517)]),
         ], 'Cambiar el servidor de una prueba cambia la conexión. Se conservan el puerto, el adaptador EF y el proveedor SQL Server.')

    save('M04_PATRONES_ARQUITECTURA', '4-2-sqlserver-rollback',
         'Una prueba de rollback necesita una escritura previa',
         'El control negativo permite comprobar que el test detecta una persistencia parcial.', [
             card(55, 175, 'Preparar dos altas', 'Mismo DbContext\nUn SaveChangesAsync', 'blue'),
             card(445, 175, 'Primera escritura', 'El motor la ejecuta\nEl test registra el hecho', 'gold'),
             card(835, 175, 'Fallo posterior', 'Se fuerza el error\nantes de la segunda alta', 'red'),
             arrow([(385, 252), (445, 252)]), arrow([(775, 252), (835, 252)]),
             card(55, 440, 'Nuevo contexto lector', 'Consulta fuera del contexto\nque sufrió la excepción', 'blue'),
             card(445, 440, 'Con transacción', 'Se revierte el lote\nCero filas persistidas', 'green'),
             card(835, 440, 'Control sin transacción', 'Sobrevive la primera alta\nUna fila persistida', 'red'),
             arrow([(1000, 330), (1000, 440)]),
             arrow([(1000, 380), (610, 380), (610, 440)], tone='green'),
             arrow([(445, 517), (385, 517)], tone='green'),
             arrow([(1000, 595), (1000, 625), (220, 625), (220, 595)], tone='red'),
         ], 'El test controla el batching para observar cada INSERT. No se desactiva la transacción de la aplicación: solo se crea una contraprueba.')

    save('M05_DDD_CQRS', '5-4-sqlserver-cqrs',
         'CQRS: dos responsabilidades, una base SQL Server',
         'La consulta posterior verifica datos confirmados desde un contexto nuevo.', [
             card(55, 175, 'Command', 'Crear o modificar la orden\nHandler y caso de uso', 'gold'),
             card(445, 175, 'Agregado', 'Orden y líneas\nProtege las invariantes', 'green'),
             card(835, 175, 'Confirmación', 'SaveChangesAsync\nTransacción local', 'blue'),
             arrow([(385, 252), (445, 252)]), arrow([(775, 252), (835, 252)]),
             card(55, 440, 'DTO de respuesta', 'Datos de lectura\nNo modifica el agregado', 'green'),
             card(445, 440, 'Query', 'Contexto nuevo\nProyección sin tracking', 'gold'),
             card(835, 440, 'Base de Producción', 'SQL Server real\nÓrdenes y líneas persistidas', 'gray'),
             arrow([(1000, 330), (1000, 440)], 'commit', label_pos=(1000, 392)),
             arrow([(835, 517), (775, 517)]), arrow([(445, 517), (385, 517)]),
         ], 'El test espera a que termine el command y después lee la misma base. Esta variante no añade una réplica ni una proyección asíncrona.')


if __name__ == '__main__':
    main()
