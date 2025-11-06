# Small helper: parse a .dnm using the analyzer (loaded safely) and print the scene texts
import io, sys, json, os

# Ensure repo root is on sys.path so `entrega2` and `entrega1` imports resolve
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
p = os.path.join('entrega1','analizadordnm.py')
with io.open(p, 'r', encoding='utf-8') as fh:
    src = fh.read()
markers = ["\nfile_path", "\nif __name__ == '__main__'", "\nif __name__ == \"__main__\"", "\nsource_code ="]
cut = -1
for m in markers:
    idx = src.find(m)
    if idx != -1:
        cut = idx
        break
src_to_exec = src if cut == -1 else src[:cut]
module_globals = {}
exec(compile(src_to_exec, p, 'exec'), module_globals)
Tokenizer = module_globals.get('Tokenizer')
Parser = module_globals.get('Parser')
if Tokenizer is None or Parser is None:
    print('Tokenizer/Parser not found in analisadordnm.py')
    sys.exit(2)

# read target dnm
dnm_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join('entrega2','snake.dnm')
with io.open(dnm_path, 'r', encoding='utf-8') as f:
    dnm_src = f.read()

tokenizer = Tokenizer(dnm_src)
tokens = tokenizer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

from entrega2.integration.dnm_loader import ast_to_scene
scene = ast_to_scene(ast)
print(json.dumps(scene.get('texts', []), ensure_ascii=False, indent=2))
