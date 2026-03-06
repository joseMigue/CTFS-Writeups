#!/usr/bin/env python3
"""JSHit CTF solver - Extrae y desofusca JSFuck para obtener la flag"""

import re
import subprocess
import tempfile
import os

# Extraer código JSFuck del HTML local
with open('src/JSHit.html', 'r') as f:
    html = f.read()

jsfuck = re.search(r'<script[^>]*id="code"[^>]*>(.*?)</script>', html, re.DOTALL).group(1).strip()

# Ejecutar en Node.js con DOM mock
node_code = f'''
const document = {{
    getElementById: () => ({{ innerHTML: '', remove: () => {{}} }}),
    cookie: ''
}};

({jsfuck})();
'''

with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
    f.write(node_code)
    temp = f.name

try:
    output = subprocess.run(['node', temp], capture_output=True, text=True, timeout=5).stdout
    
    # Extraer flag del código desofuscado (también revisar stderr)
    full_output = subprocess.run(['node', temp], capture_output=True, text=True, timeout=5)
    combined = full_output.stdout + full_output.stderr + jsfuck
    
    flag = re.search(r"pascalCTF\{[^}]+\}", combined)
    print(f"Flag: {flag.group(0)}" if flag else "Flag not found in output")
finally:
    os.unlink(temp)
