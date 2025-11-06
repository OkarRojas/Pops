# -*- coding: utf-8 -*-
"""
Main entry point that integrates the DNM analyzer with the POPS game engine.

Flow:
 - Read a .dnm file (default: snake.dnm or sys.argv[1])
 - Tokenize and parse into an AST using Tokenizer/Parser
 - Save AST as JSON (utf-8)
 - Convert AST -> scene using integration.dnm_loader.load_scene_from_ast_file
 - Create window, renderer, input handler, clock and GameEngine
 - Run the engine

Designed to be compatible with Python 2.7+ and Python 3.x.
"""
from __future__ import print_function
import sys
import os
import json
import traceback
import io
import logging

# Basic logging: INFO for the main steps, DEBUG for verbose fallbacks.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Ensure repository root is on sys.path so imports like "entrega1.analizadnm"
# work when this file is executed directly (python entrega2/main.py).
# When Python runs a script, sys.path[0] is the script's directory (entrega2/),
# so sibling packages (entrega1/) are not found unless the repo root is added.
_repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)


def _import_tokenizer_parser():
    """Try multiple import paths for Tokenizer and Parser to be robust.

    Preferred: entrega1.analizadordnm
    Fallbacks: analizadordnm, analizadordnm_py2
    """
    candidates = [
        ('entrega1.analizadordnm', 'Tokenizer', 'Parser'),
        ('analizadordnm', 'Tokenizer', 'Parser'),
        ('analizadordnm_py2', 'Tokenizer', 'Parser'),
        ('entrega1.analizadordnm_py2', 'Tokenizer', 'Parser'),
    ]
    for modname, tname, pname in candidates:
        try:
            module = __import__(modname, fromlist=[tname, pname])
            Tokenizer = getattr(module, tname)
            Parser = getattr(module, pname)
            logger.info("Imported Tokenizer/Parser from %s", modname)
            return Tokenizer, Parser
        except Exception:
            continue

    # Fallback: try to load the analyzer directly from a file path using importlib
    try:
        import importlib.util
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        logger.debug('Fallback: repo_root = %s', repo_root)
        file_paths = [
            os.path.join(repo_root, 'entrega1', 'analizadordnm.py'),
            os.path.join(repo_root, 'analizadordnm.py'),
            os.path.join(repo_root, 'entrega1', 'analizadordnm_py2.py'),
            os.path.join(repo_root, 'analizadordnm_py2.py'),
        ]
        for p in file_paths:
            exists = os.path.exists(p)
            logger.debug('Fallback: checking %s -> exists=%s', p, exists)
            if not exists:
                continue
            try:
                # Read source and exec only the definitions portion to avoid
                # running any top-level demo/CLI code present in the analyzer file.
                with io.open(p, 'r', encoding='utf-8') as fh:
                    src = fh.read()

                # Try to truncate the script before common runner markers so we only
                # execute class/function definitions.
                markers = ["\nfile_path", "\nif __name__ == '__main__'", "\nif __name__ == \"__main__\"", "\nsource_code ="]
                cut_at = -1
                for m in markers:
                    idx = src.find(m)
                    if idx != -1:
                        cut_at = idx
                        break
                src_to_exec = src if cut_at == -1 else src[:cut_at]

                module_globals = {}
                exec(compile(src_to_exec, p, 'exec'), module_globals)
                if 'Tokenizer' in module_globals and 'Parser' in module_globals:
                    logger.info('Imported Tokenizer/Parser from file (truncated): %s', p)
                    return module_globals['Tokenizer'], module_globals['Parser']
                else:
                    logger.debug('Loaded (truncated) module from %s but Tokenizer/Parser not found', p)
            except Exception as e:
                logger.debug('Error loading module from %s: %s', p, e, exc_info=True)
    except Exception as e:
        logger.debug('Importlib fallback failed: %s', e, exc_info=True)

    raise ImportError("Could not import Tokenizer and Parser from known locations."
                      " Make sure 'entrega1/analizadordnm.py' (or analizadordnm.py) is available.")


def _import_components():
    """Import engine components with fallbacks where naming varies."""
    # GameEngine
    # Prefer the entrega2 package paths first (robust when running from repo root)
    try:
        from entrega2.core.engine import GameEngine
    except Exception:
        try:
            from core.engine import GameEngine
        except Exception:
            try:
                from engine import GameEngine
            except Exception:
                raise

    # WindowManager: prefer class WindowManager but many files use windows_manager
    try:
        from entrega2.core.window_manager import WindowManager
    except Exception:
        try:
            from core.window_manager import WindowManager
        except Exception:
            try:
                from core.window_manager import windows_manager as WindowManager
            except Exception:
                # fallback: try rendering.windows_manager
                try:
                    from entrega2.rendering.windows_manager import windows_manager as WindowManager
                except Exception:
                    try:
                        from rendering.windows_manager import windows_manager as WindowManager
                    except Exception:
                        raise

    # Renderer
    try:
        from entrega2.rendering.renderer import Renderer
    except Exception:
        try:
            from rendering.renderer import Renderer
        except Exception:
            try:
                from renderer import Renderer
            except Exception:
                raise

    # InputHandler
    try:
        from entrega2.input.input_handler import InputHandler
    except Exception:
        try:
            from input.input_handler import InputHandler
        except Exception:
            try:
                from input_handler import InputHandler
            except Exception:
                raise

    # Clock
    try:
        from entrega2.core.clock import Clock
    except Exception:
        try:
            from core.clock import Clock
        except Exception:
            try:
                from clock import Clock
            except Exception:
                raise

    return GameEngine, WindowManager, Renderer, InputHandler, Clock


def main():
    # Determine DNM file path
    default_file = os.path.join(os.path.dirname(__file__), 'snake.dnm')
    dnm_path = sys.argv[1] if len(sys.argv) > 1 else default_file
    logger.info('DNM file: %s', dnm_path)

    # Step 1: import Tokenizer, Parser
    try:
        Tokenizer, Parser = _import_tokenizer_parser()
    except Exception as e:
        logger.error("ERROR importing Tokenizer/Parser: %s", e)
        logger.debug('Traceback:', exc_info=True)
        sys.exit(2)

    # Step 2: read DNM
    try:
        with io.open(dnm_path, 'r', encoding='utf-8') as f:
            dnm_source = f.read()
    except Exception as e:
        logger.error("ERROR reading DNM file '%s': %s", dnm_path, e)
        logger.debug('Traceback:', exc_info=True)
        sys.exit(3)

    # Step 3: Tokenize and parse
    logger.info("Analizando DNM...")
    try:
        tokenizer = Tokenizer(dnm_source)
        tokens = tokenizer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
    except Exception as e:
        logger.error("ERROR during tokenization/parsing: %s", e)
        logger.debug('Traceback:', exc_info=True)
        sys.exit(4)

    # Step 4: Save AST as JSON
    ast_filename = os.path.splitext(os.path.basename(dnm_path))[0] + '_ast.json'
    ast_path = os.path.join(os.path.dirname(__file__), ast_filename)
    try:
        with io.open(ast_path, 'w', encoding='utf-8') as f:
            # ensure non-ascii is preserved; fallback to str() for non-serializable
            json.dump(ast, f, indent=2, ensure_ascii=False, default=lambda o: str(o))
        logger.info("AST guardado en %s", ast_path)
    except Exception as e:
        logger.error("ERROR saving AST to JSON '%s': %s", ast_path, e)
        logger.debug('Traceback:', exc_info=True)
        sys.exit(5)

    # Step 5: convert AST -> scene using loader
    logger.info("Cargando escena desde AST JSON...")
    try:
        # import loader relative
        from integration.dnm_loader import load_scene_from_ast_file
        scene = load_scene_from_ast_file(ast_path)
        logger.info("Escena cargada.")
    except Exception as e:
        logger.error("ERROR loading scene from AST: %s", e)
        logger.debug('Traceback:', exc_info=True)
        sys.exit(6)

    # Step 6: Import engine components
    try:
        GameEngine, WindowManager, Renderer, InputHandler, Clock = _import_components()
    except Exception as e:
        logger.error('ERROR importing engine components: %s', e)
        logger.debug('Traceback:', exc_info=True)
        sys.exit(7)

    # Step 7: Create components and run engine
    try:
        # window size/title may be overridden by scene['window'] if present
        win_cfg = scene.get('window') if isinstance(scene, dict) else None
        if win_cfg and all(k in win_cfg for k in ('width', 'height')):
            width = int(win_cfg.get('width'))
            height = int(win_cfg.get('height'))
            title = win_cfg.get('title', None)
            try:
                window_manager = WindowManager(width, height, title)
            except TypeError:
                # some implementations don't accept title
                window_manager = WindowManager(width, height)
        else:
            # use defaults from config
            try:
                # try local config import
                from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
            except Exception:
                try:
                    from entrega2.config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
                except Exception:
                    WINDOW_WIDTH = 640; WINDOW_HEIGHT = 480; WINDOW_TITLE = 'Pops Game'
            try:
                window_manager = WindowManager(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
            except TypeError:
                window_manager = WindowManager(WINDOW_WIDTH, WINDOW_HEIGHT)

        surface = window_manager.get_surface()
        renderer = Renderer(surface)
        input_handler = InputHandler()
        clock = Clock()

        engine = GameEngine(window_manager, renderer, input_handler, clock, scene=scene)
        logger.info('Iniciando GameEngine...')
        engine.run()
        logger.info('GameEngine finalizó correctamente.')
    except Exception as e:
        logger.error('ERROR running engine: %s', e)
        logger.debug('Traceback:', exc_info=True)
        try:
            # attempt graceful shutdown
            window_manager.close()
        except Exception:
            pass
        sys.exit(8)


if __name__ == '__main__':
    main()
