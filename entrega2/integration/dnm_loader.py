# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, codecs

def _pick_color(dct_or_val, default=(200, 60, 60)):
    """Normalize color from several formats.

    Acceptable inputs:
    - a mapping with key 'color' as list [r,g,b]
    - a mapping with keys 'r','g','b'
    - a plain list/tuple [r,g,b]
    - a color name string (spanish/english) like 'rojo' or 'red'
    - a hex string like '#ff0000'
    """
    # helper map
    names = {
        'rojo': (255, 0, 0), 'red': (255, 0, 0),
        'verde': (0, 255, 0), 'green': (0, 255, 0),
        'azul': (0, 0, 255), 'blue': (0, 0, 255),
        'blanco': (255, 255, 255), 'white': (255, 255, 255),
        'negro': (0, 0, 0), 'black': (0, 0, 0),
        'amarillo': (255, 255, 0), 'yellow': (255, 255, 0),
        'gris': (128, 128, 128), 'gray': (128,128,128)
    }

    # if it's a dict with color key
    if isinstance(dct_or_val, dict):
        d = dct_or_val
        if isinstance(d.get('color'), (list, tuple)):
            c = d['color']; return (int(c[0]), int(c[1]), int(c[2]))
        if isinstance(d.get('color_lpop'), (list, tuple)):
            c = d['color_lpop']; return (int(c[0]), int(c[1]), int(c[2]))
        if all(k in d for k in ('r', 'g', 'b')):
            return (int(d['r']), int(d['g']), int(d['b']))
        # maybe a named color stored as string
        if isinstance(d.get('color'), str):
            name = d.get('color').lower()
            return names.get(name, default)

    # plain list/tuple
    if isinstance(dct_or_val, (list, tuple)) and len(dct_or_val) >= 3:
        return (int(dct_or_val[0]), int(dct_or_val[1]), int(dct_or_val[2]))

    # string name or hex
    if isinstance(dct_or_val, str):
        s = dct_or_val.strip().lower()
        if s in names:
            return names[s]
        if s.startswith('#') and len(s) in (7, 4):
            try:
                if len(s) == 7:
                    return (int(s[1:3], 16), int(s[3:5], 16), int(s[5:7], 16))
                # short form #rgb
                r = int(s[1]*2, 16); g = int(s[2]*2, 16); b = int(s[3]*2, 16)
                return (r, g, b)
            except Exception:
                return default

    return default

def ast_to_scene(ast_dict):
    """Convert a parsed AST (dict) into a visual scene.

    This implementation is liberal: when the AST does not contain explicit
    bricks or texts it will create a readable layout mapping each top-level
    definition into a labelled brick plus property texts. That makes the
    `.dnm` files "real" and visible in the engine for demos.
    """
    scene = {"bricks": [], "texts": [], "entities": []}
    window = None

    # If AST has explicit window info, apply it
    for name, val in ast_dict.items():
        if isinstance(val, dict) and (
            name.lower() in ('ventana', 'window') or
            set(['width', 'height']).issubset(set([k.lower() for k in val.keys()])) or
            set(['ancho', 'alto']).issubset(set([k.lower() for k in val.keys()]))):
            w = int(val.get('width', val.get('ancho', 640)))
            h = int(val.get('height', val.get('alto', 480)))
            title = val.get('title', val.get('titulo', 'Pops Game'))
            window = {"width": w, "height": h, "title": title}
            break

    # Layout parameters for auto-generated bricks
    cols = 3
    margin_x = 20
    margin_y = 20
    brick_w = 200
    brick_h = 40
    gap_x = 20
    gap_y = 30

    # Create bricks from top-level entries. If an entry already looks like a
    # brick (contains x,y and w/h) we use exact values, otherwise we place
    # items in a grid and render their properties as texts.
    idx = 0
    palette = [(200, 60, 60), (60, 160, 60), (60, 100, 200), (200, 180, 60), (160, 60, 160)]
    for name, val in ast_dict.items():
        # skip explicit window node
        if name.lower() in ('ventana', 'window'):
            continue
        # If the node declares an entity, try to instantiate it
        if isinstance(val, dict) and (
            val.get('type') == 'entity' or 'class' in val or 'entity_class' in val):
            class_name = val.get('class') or val.get('entity_class')
            # Only a simple built-in mapping for now
            try:
                if class_name == 'MovableEntity' or class_name == 'movableentity':
                    # import the class
                    try:
                        from entrega2.entities.movable_entity import MovableEntity
                    except Exception:
                        from entities.movable_entity import MovableEntity

                    # position: prefer explicit x,y else place in grid
                    if 'x' in val and 'y' in val:
                        ent_x = int(val['x'])
                        ent_y = int(val['y'])
                    else:
                        col = idx % cols
                        row = idx // cols
                        ent_x = margin_x + col * (brick_w + gap_x)
                        ent_y = margin_y + row * (brick_h + gap_y)

                    # color
                    ent_color = None
                    if 'color' in val:
                        ent_color = _pick_color(val['color'])
                    elif 'r' in val and 'g' in val and 'b' in val:
                        ent_color = _pick_color({'r': val['r'], 'g': val['g'], 'b': val['b']})
                    else:
                        ent_color = palette[idx % len(palette)]

                    instance = MovableEntity(ent_x, ent_y, ent_color)
                    scene['entities'].append(instance)
                    idx += 1
                    continue
            except Exception:
                # fallback to treating as regular node if instantiation fails
                pass

        if isinstance(val, dict) and all(k in val for k in ('x', 'y')) and (
            ('w' in val and 'h' in val) or ('width' in val and 'height' in val)):
            w = int(val.get('w', val.get('width', 16)))
            h = int(val.get('h', val.get('height', 16)))
            color = _pick_color(val)
            scene['bricks'].append({"x": int(val['x']), "y": int(val['y']), "w": w, "h": h, "color": color})
        else:
            col = idx % cols
            row = idx // cols
            x = margin_x + col * (brick_w + gap_x)
            y = margin_y + row * (brick_h + gap_y)
            # choose color: prefer a 'color' property in val, else palette
            preferred_color = None
            if isinstance(val, dict):
                # if val contains a color spec anywhere, use it
                if 'color' in val:
                    preferred_color = _pick_color(val['color'])
                elif 'color_lpop' in val:
                    preferred_color = _pick_color(val['color_lpop'])
                elif 'tipo' in val and isinstance(val['tipo'], str):
                    # small heuristic: special type -> yellow
                    if val['tipo'].lower() in ('bonus', 'especial'):
                        preferred_color = (255, 200, 0)
            color = preferred_color if preferred_color is not None else palette[idx % len(palette)]
            scene['bricks'].append({"x": x, "y": y, "w": brick_w, "h": brick_h, "color": color})

            # add title text centered on the brick
            scene['texts'].append({"text": str(name), "x": x + 8, "y": y + 8, "size": 18, "color": (255,255,255)})

            # render small property lines below the brick
            if isinstance(val, dict):
                prop_y = y + brick_h + 6

                # If the node requests specific property lines to display,
                # support several keys: 'display_only', 'print_only', 'show_only'.
                # The value may be a string (single property) or a list of keys.
                display_key = None
                for k in ('display_only', 'print_only', 'show_only'):
                    if k in val:
                        display_key = val[k]
                        break

                if display_key is not None:
                    # normalize into a list of keys to show
                    keys_to_show = [display_key] if isinstance(display_key, str) else list(display_key)
                    for key in keys_to_show:
                        # only print if that property exists in the block
                        if key in val:
                            text_line = "%s: %s" % (key, val[key])
                            scene['texts'].append({"text": text_line, "x": x + 8, "y": prop_y, "size": 14, "color": (220,220,220)})
                            prop_y += 16
                else:
                    for prop_k, prop_v in list(val.items())[:4]:
                        text_line = "%s: %s" % (prop_k, prop_v)
                        scene['texts'].append({"text": text_line, "x": x + 8, "y": prop_y, "size": 14, "color": (220,220,220)})
                        prop_y += 16

        idx += 1

    if window:
        scene['window'] = window
    return scene

def load_scene_from_ast_file(ast_path):
    with codecs.open(ast_path, 'r', 'utf-8') as f:
        ast_dict = json.load(f)
    return ast_to_scene(ast_dict)
