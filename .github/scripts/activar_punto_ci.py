"""Uncomment staged lesson code in a copied workspace, only for CI tests."""
from pathlib import Path
import sys
point=Path(sys.argv[1])
for f in point.rglob('*.cs'):
    text=f.read_text(encoding='utf-8')
    if 'INICIO PASO' in text:
        lines=text.splitlines(keepends=True)
        output=[]; inside=False
        for line in lines:
            if line.startswith('// INICIO PASO '): inside=True; continue
            if line.startswith('// FIN PASO '): inside=False; continue
            if inside and line.startswith('// '): output.append(line[3:])
            elif inside and line.strip()=='//': output.append('\n')
            else: output.append(line)
        f.write_text(''.join(output),encoding='utf-8')
print('Activado:', point)
