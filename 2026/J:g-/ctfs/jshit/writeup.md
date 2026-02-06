# CTF JSHit — Wrap-up

**Clasificación**: CWE-506 — Embedded Malicious Code

## Resumen

Se identificó y explotó JavaScript ofuscado (JSFuck) en una página web. El script ofuscado contenía la flag hardcodeada.

## Flag

[Código para conseguir la flag automáticamente](./script.py)
```
pascalCTF{1_h4t3_j4v4scr1pt_s0o0o0o0_much}
```

## Proceso

### 1. Inspección inicial desde el navegador

Se accedió al sitio `https://jshit.ctf.pascalctf.it` y al usar el inspector de elementos no se observó código JavaScript.

Esto se puede comprobar si se abre [el sitio localmente](./src/JSHit.html)

### 2. Ejecución de código sin script visible

Se accedió a la consola y se observó el mensaje "where's the page gone?". Esto evidencia que hubo una ejecución de código en algún momento.

### 3. Observación de la response sin "procesar" por el navegador

Se hizo la petición mediante `curl` para analizar el contenido que llega desde el servidor sin que haya intervención del navegador:
```bash
curl https://jshit.ctf.pascalctf.it > src/index.html
```
Se observó que el html tiene un elemento `<script id="code">` que contiene caracteres especiales ofuscados mediante JSFuck.

### 4. Desofuscación

Se desofuscó el código JSFuck. Se trata de una función que el navegador ejecuta al acceder al sitio. La función escribe el mensaje en consola anteriormente mencionado y elimina el propio bloque de script.

[Código desofuscado](./res/deofuscated.js)

### 5. Extracción de la flag

Dentro del código desofuscado se encontraba la flag en texto plano:
```
pascalCTF{1_h4t3_j4v4scr1pt_s0o0o0o0_much}
```
