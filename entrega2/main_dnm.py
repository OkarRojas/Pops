import json
from analizadordnm_py2 import Tokenizer, Parser
from integration.dnm_loader import load_scene_from_ast_file
from core.engine import GameEngine
from core.window_manager import WindowManager
from rendering.renderer import Renderer
from input.input_handler import InputHandler
from core.clock import Clock
from config import *


def main():
    dnm_file = "entrega2/snake.dnm"  # Tu archivo .dnm
    
    # PASO 1: Analizar el archivo .dnm
    print("1. Analizando archivo DNM...")
    with open(dnm_file, "r") as f:
        codigo_dnm = f.read()
    
    tokenizer = Tokenizer(codigo_dnm)
    tokens = tokenizer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    print("   ✓ AST generado")
    
    # PASO 2: Guardar AST como JSON
    ast_file = "entrega2/snake_ast.json"
    with open(ast_file, "w") as f:
        json.dump(ast, f, indent=2)
    print(f"2. AST guardado en {ast_file}")
    
    # PASO 3: Cargar Scene desde el AST
    print("3. Cargando escena...")
    scene = load_scene_from_ast_file(ast_file)
    print("   ✓ Escena cargada")
    
    # PASO 4: Crear componentes del motor
    print("4. Inicializando motor...")
    window_manager = WindowManager(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    surface = window_manager.get_surface()
    renderer = Renderer(surface)
    input_handler = InputHandler()
    clock = Clock()
    print("   ✓ Componentes inicializados")
    
    # PASO 5: Crear GameEngine con la Scene cargada
    print("5. Creando GameEngine...")
    engine = GameEngine(
        window_manager, 
        renderer, 
        input_handler, 
        clock, 
        scene=scene  # ← ¡Tu Scene del .dnm va aquí!
    )
    print("   ✓ Engine listo")
    
    # PASO 6: Ejecutar el juego
    print("6. Iniciando juego...")
    engine.run()
    
    print("7. Juego cerrado")


if __name__ == "__main__":
    main()
