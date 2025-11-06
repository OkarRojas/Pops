import sys, os
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)
print('sys.path[0]=', sys.path[0])

try:
    from entrega2.input.input_handler import InputHandler
    print('Imported entrega2.input.input_handler OK')
except Exception as e:
    import traceback as _tb
    print('entrega2.input.input_handler failed:', type(e), e)
    print(_tb.format_exc())

try:
    import entrega2.confing as confmod
    print('Imported entrega2.confing OK (path=%s)' % getattr(confmod, '__file__', '<unknown>'))
except Exception as e:
    print('entrega2.confing failed:', type(e), e)

try:
    import confing as top_conf
    print('Imported top-level confing OK (path=%s)' % getattr(top_conf, '__file__', '<unknown>'))
except Exception as e:
    print('top-level confing failed:', type(e), e)

try:
    from input.input_handler import InputHandler
    print('input.input_handler OK')
except Exception as e:
    print('input.input_handler failed:', type(e), e)

try:
    from input_handler import InputHandler
    print('input_handler OK')
except Exception as e:
    print('input_handler failed:', type(e), e)
