# Travel CTF — Wrap-up

**Clasificación:** CWE-22 — Improper Limitation of a Pathname to a Restricted Directory (Path Traversal)

## Resumen

Se encontró vulnerabilidad de Local File Inclusion (LFI) en `/api/get_json` de una app que permite acceder a canciones mediante un índice. El parámetro `index` se concatena directamente sin sanitización en la construcción del path, permitiendo path traversal para leer archivos arbitrarios.

## Flag

[Código para conseguir la flag automáticamente](./script.py)
```
pascalCTF{4ll_1_d0_1s_tr4v3ll1nG_4r0und_th3_w0rld}
```

## Proceso

### 1. Análisis

La aplicación permite seleccionar canciones (1-7) mediante POST a `/api/get_json` con el parámetro `index`.

### 2. Vector de ataque
Código vulnerable (del lado del servidor):
```python
@app.route("/api/get_json", methods=["POST"])
def get_json():
    index = request.json.get("index")
    path = f"static/{index}"  # ← Sin validación
    with open(path, "r") as file:
        return file.read(), 200
```

### 3. Explotación

Se usó path traversal mediante `../../../proc/self/cwd/flag.txt`. El backend construye `static/{index}` permitiendo subir 3 niveles desde `/home/challenge/static/` hasta `/home/challenge/`, accediendo a la flag ubicada en `/proc/self/cwd` (que apunta al directorio de trabajo).
