# Ejecutar en Windows XP (Athlon XP) y objetivo: disquete

Este documento explica las opciones realistas para ejecutar tu programa en un equipo con Windows XP (Athlon XP) y la restricción adicional de que todo quepa en un disquete de 1,44 MB.

## Resumen rápido
- Python recomendado para compatibilidad con Windows XP: Python 2.7.18 (última de la rama 2.7)
- pygame que históricamente funciona bien en XP: pygame 1.9.2 (o 1.9.x)
- Realidad del disquete: Es virtualmente imposible empaquetar Python + pygame + tu juego en 1,44 MB. Incluso una instalación mínima de Python 2.7 y pygame excede ampliamente ese tamaño.

## Opciones prácticas (elige la que prefieras)

1) Entorno clásico (recomendado si quieres compatibilidad completa)
   - Instalación objetivo: Python 2.7.18 + pygame 1.9.2 (instaladores binarios para Windows XP).
   - Ventajas: alta probabilidad de que el juego funcione sin reescribir mucho código si adaptas el código a Python 2.7.
   - Pasos básicos (en la máquina Windows XP):
     1. Descargar Python 2.7.18 (instalador MSI o EXE). Busca archives o mirrors oficiales.
     2. Descargar pygame 1.9.2 para Python 2.7 (binarios Windows). Instalar con el instalador o `pip` si está disponible.
     3. Ejecutar tu script con `python mygame.py`.

2) Distribución como EXE (congelado) para Windows XP
   - Usa py2exe (funciona con Python 2.7) para crear un EXE de tu juego. Comprime el ejecutable con UPX.
   - Suele reducir la dependencia de Python instalado, pero el EXE final con librerías SDL y pygame seguirá ocupando múltiples megabytes.

3) Si la restricción del disquete es inviolable
   - Opciones realistas:
     - Reescribir el juego en C o ensamblador y reducir recursos al mínimo (extremo, complejo).
     - Usar un intérprete muy mínimo/embedded (no hay soluciones Python+SDL modernas que quepan en 1,44 MB).
   - Conclusión: no viable mantener Python+pygame en 1,44 MB.

## Consejos para reducir tamaño (si la meta es minimizar distribución)
- Eliminar archivos de documentación, tests y locales del intérprete.
- Distribuir solo archivos .pyo/.pyc (bytecode) en vez del código fuente si usas Python 2.7.
- Comprimir ejecutable con UPX (no siempre permitida por antivirus).
- Usar imágenes y sonidos muy pequeños o generarlos algorítmicamente.

## Pasos recomendados que puedo automatizar o preparar para ti
1. Revisar tu código y señalar incompatibilidades con Python 2.7 (print, bytes/str, f-strings, etc.).
2. Preparar un `py2exe` o guía paso a paso para crear un EXE en Python 2.7.
3. Crear un paquete lo más pequeño posible y documentar los pasos para usar UPX.

## Enlaces útiles
Busca mirrors si los oficiales ya no alojan estos binarios:
- Python 2.7.18 Windows installer (busca "Python 2.7.18 windows installer archive")
- pygame 1.9.2 Windows binaries (buscar "pygame-1.9.2.win32-py2.7")

## Notas finales
Si quieres, puedo:
  - Analizar tu código actual en `entrega2/` y generar una lista de cambios necesarios para que funcione bajo Python 2.7.
  - Preparar un `setup.py` de `py2exe` y un procedimiento paso a paso para construir el EXE en un entorno Windows moderno o en la propia máquina XP.
  - Intentar empaquetar una versión mínimamente comprimida y decir exactamente cuánto ocuparía.

Indícame qué opción prefieres: 1 (instalar Python 2.7 + pygame 1.9.2), 2 (crear EXE con py2exe), 3 (intentar máxima compresión / evaluar viabilidad de 1,44 MB), o 4 (que analice y adapte tu código para Python 2.7).
