
# Formato DNM -> Scene (guía de conversión)

Este documento describe cómo el loader `entrega2/integration/dnm_loader.py` convierte
el AST (resultado del parser DNM) en la `scene` que utiliza el motor POPS.

El objetivo del loader es ser tolerante: si el AST no contiene objetos gráficos
explícitos, el loader genera una representación visual (ladrillos y textos)
para que los archivos `.dnm` sean inmediatamente visibles en la escena.

## Resultado final (`scene`)
El loader produce un diccionario Python con, como mínimo, estas claves:

- `bricks`: lista de rectángulos a dibujar. Cada brick tiene la forma:
  ```python
  {"x": int, "y": int, "w": int, "h": int, "color": (r,g,b)}
  ```
- `texts`: lista de textos a dibujar. Cada texto tiene la forma:
  ```python
  {"text": str, "x": int, "y": int, "size": int, "color": (r,g,b)}
  ```
- `entities`: lista (vacía por defecto). Actualmente el loader no instancia
  entidades con comportamiento; se deja como gancho para implementar fábricas.
- `window` (opcional): si está presente, contiene `width`, `height`, `title`.

## Reglas de mapeo (cómo se crean los rectángulos y textos)

1. Nodo `window` / `ventana`:
   - Si existe un nodo top-level llamado `ventana` o `window`, o cualquier nodo
     que contenga las claves `width` y `height` (o `ancho`/`alto`), el loader
     crea `scene['window'] = {"width":..., "height":..., "title":...}`.

2. Bricks explícitos (posición definida):
   - Si un nodo top-level es un diccionario que contiene `x` y `y` y también
     `w`/`h` (o `width`/`height`), el loader lo interpreta como un brick
     explícito y lo añade tal cual a `scene['bricks']` usando el color
     especificado si existe.

   - Ejemplo AST (brick explícito):
     ```json
     "bloque1": { "x": 100, "y": 50, "w": 32, "h": 16, "color": [255,0,0] }
     ```
     → `scene['bricks']` recibirá {"x":100,"y":50,"w":32,"h":16,"color":(255,0,0)}

3. Bricks automáticos (cuando no hay x/y):
   - Para nodos top-level que no contienen `x`/`y`, el loader crea automáticamente
     un brick en una cuadrícula de columnas (por defecto 3 columnas). Cada
     elemento ocupa un rectángulo ancho (por defecto 200×40) y se posiciona
     con márgenes y separación para que se vean ordenados.
   - Esto convierte reglas o definiciones (como `regla_movimiento_snake`) en
     bloques visuales para inspección rápida.

4. Textos automáticos:
   - Para cada brick automático se añade un texto con el `name` (clave top-level)
     posicionado dentro del ladrillo (tamaño por defecto 18) y hasta 4 líneas
     adicionales con propiedades (p. ej. `velocidad_inicial: 1`) dibujadas
     inmediatamente debajo del brick (tamaño por defecto 14).

5. Colores — formatos aceptados
   - El loader acepta varios formatos para especificar color:
     - Lista o tupla: `[r, g, b]` o `(r, g, b)` (valores 0-255).
     - Diccionario con claves `r`, `g`, `b`.
     - Nombre de color (español o inglés): `"rojo"`, `"green"`, `"azul"`.
     - Hex string: `"#ff0000"` o `"#f00"`.
     - Clave específica `color_lpop` (legacy) con lista de 3 números.
   - Si no se encuentra color, el loader usa una paleta por defecto.

   Ejemplos:
   ```json
   { "color": [255,0,0] }         // rojo
   { "r":255, "g":200, "b":0 } // amarillo
   { "color": "rojo" }          // nombre
   { "color": "#00ff00" }       // hex
   ```

6. Textos explícitos:
   - Si un nodo tiene `text` (o `value`) **y** `x` y `y`, se interpretará
     como un texto explícito y se añadirá a `scene['texts']` con el color y
     tamaño indicados (por defecto size=16 y color blanco).

   Ejemplo AST (texto explícito):
   ```json
   "label1": { "text": "Puntos: 0", "x": 10, "y": 10, "size": 20 }
   ```

7. Propiedades numéricas generales:
   - Propiedades top-level sencillas (no dicts) con nombres como `speed`,
     `velocidad` o `move_speed` se copian a `scene['speed']` como flotante.

## Limitaciones actuales

- El loader no instancia por defecto entidades con lógica (p. ej. una clase
  `Snake` con movimiento). `scene['entities']` queda vacío. Para crear
  entidades con comportamiento hay que implementar una fábrica que mapee
  nodos AST a objetos de `entrega2/entities/`.
- El layout automático usa tamaños fijos (200×40) útiles para visualizar
  definiciones, no es un diseño final para un juego.

## Ejemplo práctico (con `snake_ast.json` generado)

El AST de `snake.dnm` (resumen) contiene varias reglas top-level como
`regla_movimiento_snake`, `regla_comida`, `regla_fin_juego`, etc. Dado que
ninguna de estas definiciones contiene coordenadas `x,y`, el loader generará
un brick por cada regla y añadirá textos con el nombre y algunas propiedades.

Resultado (fragmento de `scene` generado):

```python
{
  'bricks': [
     {'x':20,'y':20,'w':200,'h':40,'color':(200,60,60)},
     {'x':240,'y':20,'w':200,'h':40,'color':(60,160,60)},
     # ...
  ],
  'texts': [
     {'text':'regla_movimiento_snake','x':28,'y':28,'size':18,'color':(255,255,255)},
     {'text':'direccion_inicial: derecha','x':28,'y':68,'size':14,'color':(220,220,220)},
     # ...
  ]
}
```

## Cómo definir un brick o texto explícito en tu `.dnm`

- Para un brick explícito, crea una definición que al parsearse produzca
  un diccionario con `x`, `y`, `w` y `h`.

- Para un texto explícito, produce un diccionario con `text`, `x` y `y`.

Si necesitas que ciertas reglas generen entidades jugables (Snake, Food, etc.)
podemos definir una convención: por ejemplo incluir `"type": "entity"` y
`"class": "SnakeHead"` en la definición, y entonces ampliar el loader para
instanciar la clase `entrega2/entities/snake.py` mediante una fábrica.

---

Si quieres, puedo:

- Añadir ejemplos de `.dnm` concretos que mapeen a bricks/texts (te los genero).
- Implementar una fábrica básica de entidades que reconozca `type: entity` y
  cree instancias de las clases en `entrega2/entities/`.

Dime qué prefieres y lo implemento.
