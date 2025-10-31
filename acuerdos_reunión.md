# 10 COSAS QUE DEBEN ACORDAR ANTES DE EMPEZAR

## 🎯 Resumen Ejecutivo

## 1. ✅ INTERFACES Y CONTRATOS

**¿Qué es?** Los métodos exactos y parámetros que cada módulo tendrá.

**Por qué?** Si cada uno crea métodos diferentes, el código no funcionará junto.

### Ejemplo de lo que debemos acordar:

```python
# Persona 1 - WindowManager
class WindowManager:
    def __init__(self, width, height, title)
    def get_surface() → retorna pygame.Surface
    def is_running() → retorna bool
    def close() → retorna None

# Persona 1 - Renderer
class Renderer:
    def __init__(self, surface)
    def clear(color) → retorna None
    def draw_rect(x, y, width, height, color) → retorna None
    def draw_text(text, x, y, font_size, color) → retorna None
    def present() → retorna None

# Persona 2 - GameEngine
class GameEngine:
    def __init__()
    def run() → retorna None
    def process_events() → retorna None
    def update(delta_time) → retorna None
    def render() → retorna None

# Persona 3 - InputHandler
class InputHandler:
    def __init__()
    def update() → retorna None
    def is_key_pressed(key_name) → retorna bool
```

**Tarea**: Documentar esto en un archivo `INTERFACES.md` en el repositorio.

---

## 2. ✅ CREAR config.py COMPARTIDO

**¿Qué es?** Un único archivo con TODAS las constantes que todos usarán.

**Por qué?** Evita que alguien use 800x600 y otro 640x480, causando caos.

### Ejemplo de constantes a acordar:

```python
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
WINDOW_TITLE = "Pops Game Engine"
FPS = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Control
KEY_UP = 'w'
KEY_DOWN = 's'
KEY_LEFT = 'a'
KEY_RIGHT = 'd'
KEY_ESCAPE = 'ESCAPE'
MOVE_SPEED = 5
```

**Tarea**: Persona 2 crea el archivo, todos lo revisan.

---

## 3. ✅ ESTRUCTURA DE CARPETAS

**¿Qué es?** Todos debemos crear la misma estructura para que los imports funcionen.

### Estructura acordada:

```
entrega2/
├── cgonfi.py                       # Compartido
├── core/
│   ├── __init__.py
│   ├── window_manager.py          # Persona 1
│   ├── engine.py                  # Persona 2
│   └── clock.py                   # Persona 2
├── rendering/
│   ├── __init__.py
│   ├── renderer.py                # Persona 1
│   └── sprite.py                  # Persona 1
├── input/
│   ├── __init__.py
│   └── input_handler.py           # Persona 3
├── entities/
│   ├── __init__.py
│   └── movable_entity.py          # Persona 3
├── integration/
│   ├── __init__.py
│   └── dnm_loader.py              # Persona 2
├── demos/
│   └── brick_movement_demo.py     # Persona 3
├── main.py
├── requirements.txt
└── README.md
```

**Importante**: Todos los `__init__.py` deben existir, aunque estén vacíos.

**Tarea**: Crear esta estructura en el repositorio.

---

## 4. ✅ ESTRATEGIA DE GIT Y RAMAS

**¿Qué es?** Cómo organizar el trabajo en Git.

### Ramas a crear:

```
main                    # Rama estable, lista para entregar
develop                 # Rama principal de integración
feature/rendering       # Persona 1 trabaja aquí
feature/game-loop       # Persona 2 trabaja aquí
feature/input-system    # Persona 3 trabaja aquí

```

### Reglas de oro:

- **NUNCA trabajar directamente en `main` o `develop`**
- Cada persona trabaja en su rama `feature/`
- Solo fusionar a `develop` cuando funciona
- Fusionar a `main` solo al final para entrega

**Tarea**: Persona 2 crea todas las ramas.

---

## 5. ✅ CONVENCIÓN DE COMMITS

**¿Qué es?** Cómo escribir mensajes de commit consistentes.

### Formato acordado:

```bash
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Documentación
refactor: Cambio de código sin nueva funcionalidad
```

### Ejemplos CORRECTOS:

```bash
git commit -m "feat: implementa método draw_rect en Renderer"
git commit -m "feat: crea clase WindowManager con ventana 640x480"
git commit -m "fix: corrige error de importación en config"
git commit -m "docs: agrega docstrings a clase InputHandler"
```

### Ejemplos INCORRECTOS:

```bash
git commit -m "cambios"
git commit -m "asdf"
git commit -m "arreglo el bug"
```

**Tarea**: Documentar en `GITHUB_WORKFLOW.md`

---

## 6. ✅ CALENDARIO DE REUNIONES E INTEGRACIONES

**¿Qué es?** Cuándo se reúnen y cuándo integran el código.

## 7. ✅ RESPONSABILIDADES CLARAS

**¿Qué es?** Qué hace cada persona y en qué orden.

### Distribución:

**parte 1**
- **Persona 1**: WindowManager y Renderer básicos
- **Persona 2**: Engine y Clock básicos
- **Persona 3**: InputHandler básico

**parte 2
- **Persona 2**: Crear DNMLoader**
- **Persona 1**: Expandir Renderer (más métodos)
- **Persona 3**: Demo de movimiento

**parte 3**
- **TODOS**: Integración y debugging
- **TODOS**: Documentación técnica
- **TODOS**: Testing exhaustivo


## 8. ✅ CRITERIOS DE ÉXITO

**¿Qué es?** Cuándo saben que algo está "listo".

### Un módulo está listo cuando:

- ✓ Funciona individualmente sin errores
- ✓ Está documentado con docstrings
- ✓ Cumple las interfaces acordadas
- ✓ Se probó con datos de entrada típicos
- ✓ El código sigue las convenciones acordadas
- ✓ Se hizo commit descriptivo
- ✓ Se subió a la rama feature/
- ✓ Otro miembro del equipo lo revisó

---

### Itinerario sugerido:

**30 minutos**: Revisión de requisitos
- Leer juntos la Entrega 2
- Asegurarse de que todos entienden

**45 minutos**: Definir interfaces
- Acordar nombres de clases y métodos
- Documentar en archivo compartido

**15 minutos**: Crear config.py
- Acordar constantes
- Una persona lo crea, todos lo revisan

**15 minutos**: Crear estructura
- Acordar carpetas
- Crear en repositorio

**20 minutos**: Setup de Git
- Crear rama develop
- Crear ramas feature/... 

**10 minutos**: Comunicación
- Definir canales
- Acordar horarios de reuniones

**10 minutos**: Timeline
- Acordar fechas de integraciones
- Establecer próximas reuniones

**10 minutos**: Testing
- Cómo probar cada módulo
- Quién es responsable de integración

**5 minutos**: Documentación
- Crear README.md
- Guardar acuerdos

**5 minutos**: Verificación final
- ¿Todos entienden lo acordado?
- Asignar tareas iniciales

---

## ❌ ERRORES A EVITAR

| Error | Resultado |
|-------|-----------|
| Empezar sin acordar interfaces | Cada uno crea métodos diferentes |
| No tener config.py compartido | Tamaños de ventana inconsistentes |
| No definir división clara | Duplicación de trabajo o trabajo no hecho |
| Commits sin convención | Historial de Git ilegible |
| Integrar todo último minuto | CAOS total y bugs imposibles |
| No comunicarse | Sorpresas desagradables al integrar |
| Cambiar interfaces sin avisar | El código de otros se rompe |
| Trabajar en main directamente | El código estable se daña |

---che

## ✅ DOCUMENTO FINAL

Después de la reunión, guarden en el repositorio:

- **ACUERDOS.md**: Este documento
- **INTERFACES.md**: Interfaces exactas acordadas
- **GITHUB_WORKFLOW.md**: Cómo usar Git y ramas
- **README.md**: Cómo instalar y ejecutar el proyecto
- **requirements.txt**: Dependencias

Linken esto en el README para que todos lo tengan de referencia.

