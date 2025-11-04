# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, codecs

def _pick_color(dct, default=(255,0,0)):
    if isinstance(dct.get('color'), list):
        c = dct['color'];   return (int(c[0]), int(c[1]), int(c[2]))
    if isinstance(dct.get('color_lpop'), list):
        c = dct['color_lpop']; return (int(c[0]), int(c[1]), int(c[2]))
    if all(k in dct for k in ('r','g','b')):
        return (int(dct['r']), int(dct['g']), int(dct['b']))
    return default

def ast_to_scene(ast_dict):
    scene = {"bricks": [], "texts": [], "entities": []}
    window = None
    for name, val in ast_dict.items():
        if isinstance(val, dict) and (name.lower() in ('ventana','window') or
            set(['width','height']).issubset(set([k.lower() for k in val.keys()])) or
            set(['ancho','alto']).issubset(set([k.lower() for k in val.keys()]))):
            w = int(val.get('width', val.get('ancho', 640)))
            h = int(val.get('height', val.get('alto', 480)))
            title = val.get('title', val.get('titulo', 'Pops Game'))
            window = {"width": w, "height": h, "title": title}
            continue
        if isinstance(val, dict) and all(k in val for k in ('x','y')) and \
           (('w' in val and 'h' in val) or ('width' in val and 'height' in val)):
            w = int(val.get('w', val.get('width', 16)))
            h = int(val.get('h', val.get('height', 16)))
            color = _pick_color(val)
            scene['bricks'].append({"x": int(val['x']), "y": int(val['y']), "w": w, "h": h, "color": color})
            continue
        if isinstance(val, dict) and ('text' in val or 'value' in val) and 'x' in val and 'y' in val:
            text = val.get('text', val.get('value', ''))
            size = int(val.get('size', 16))
            color = _pick_color(val, default=(255,255,255))
            scene['texts'].append({"text": text, "x": int(val['x']), "y": int(val['y']), "size": size, "color": color})
            continue
        if not isinstance(val, dict) and name.lower() in ('speed','velocidad','move_speed'):
            scene['speed'] = float(val)
    if window:
        scene['window'] = window
    return scene

def load_scene_from_ast_file(ast_path):
    with codecs.open(ast_path, 'r', 'utf-8') as f:
        ast_dict = json.load(f)
    return ast_to_scene(ast_dict)
