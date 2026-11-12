"""Lectura estricta de las citas físicas del material M08, sin motores PDF."""
import re


def parse_explanation(line):
    """Devuelve (número, código) para una cita; acepta backticks anidados."""
    heading = re.match(r'- \*\*Línea (\d+):\*\* (.*)', line)
    if not heading:
        return None
    tail = heading.group(2)
    if tail.startswith('(línea vacía)'):
        return int(heading.group(1)), ''
    quote = re.match(r'(?P<fence>`+)(?P<code>.*?)(?P=fence)(?:\s|$)', tail)
    if not quote:
        raise ValueError('Explicación numerada sin una cita de código verificable: ' + line.strip())
    return int(heading.group(1)), quote.group('code').strip()
