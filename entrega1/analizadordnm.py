"""
Implementado en python 3.0
@author: dnm Team
"""

import json
import re   
import os

class Tokenizer:
    def __init__(self, source_code):
        self.source = source_code
        self.tokens = []

    def tokenize(self):
        lines = self.source.splitlines()
        for line in lines:
            line = line.strip()
            if not line or line.startswith('...'):
                continue
            
            regex_tokens = re.findall(r'"([^"]*)"|(\d+\.?\d*)|(<|>|\¿|\?|\(|\)|=|,|:)|(\w+)', line)
            
            for group in regex_tokens:
                if group[0]:  # Es cadena de texto
                    self.tokens.append(('STRING', group[0]))
                elif group[1]:  # Es un numero
                    if '.' in group[1]:
                        self.tokens.append(('NUMBER', float(group[1])))
                    else:
                        self.tokens.append(('NUMBER', int(group[1])))
                elif group[2]:  # Es un operador o delimitador
                    self.tokens.append(('OPERATOR', group[2]))
                elif group[3]:  # Es un identificador
                    if group[3] in ('fpop', 'wpop', 'lpop', 'dpop', 'pops'):
                        self.tokens.append(('KEYWORD', group[3]))
                    else:
                        self.tokens.append(('IDENTIFIER', group[3]))
        
        return self.tokens
    
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.symbol_table = {}

    def parse(self):
        while self.current_token_index < len(self.tokens):
            if self.peek_token() is None:
                break

            key_token = self.peek_token()  #no consumir todavía

            # Caso: diccionarios
            if key_token[0] == 'KEYWORD' and key_token[1] == 'dpop':
                # Necesitamos obtener el identificador que sigue después de dpop
                if self.current_token_index + 1 < len(self.tokens):
                    ident_token = self.tokens[self.current_token_index + 1]
                    if ident_token[0] == 'IDENTIFIER':
                        self.get_token()  # consumir 'dpop'
                        ident = self.get_token()[1]  # consumir identificador
                        value = self.parse_block()
                        self.symbol_table[ident] = value
                        continue
                    else:
                        raise SyntaxError(f"Error de sintaxis: Se esperaba un identificador después de 'dpop', se encontró {ident_token}")
                else:
                    raise SyntaxError("Error de sintaxis: Se esperaba un identificador después de 'dpop'")

            # Caso: bucles
            if key_token[0] == 'KEYWORD' and key_token[1] in ('fpop', 'wpop'):
                self.get_token()  # consumir la palabra clave
                value = self.parse_bucle()
                self.symbol_table[f'{key_token[1]}_{self.current_token_index}'] = value
                continue

            # Caso: funciones
            if key_token[0] == 'KEYWORD' and key_token[1] == 'pops':
                self.get_token()
                value = self.parse_fonction()
                self.symbol_table[f'function_{self.current_token_index}'] = value
                continue

            # Caso: arrays
            if key_token[0] == 'KEYWORD' and key_token[1] == 'lpop':
                self.get_token()
                value = self.parse_array()
                self.symbol_table[f'array_{self.current_token_index}'] = value
                continue



            # Caso: definiciones de figuras (IDENTIFIER seguido de ¿)
            if key_token[0] == 'IDENTIFIER':
                # Mirar el siguiente token para ver si es ¿
                next_token = None
                if self.current_token_index + 1 < len(self.tokens):
                    next_token = self.tokens[self.current_token_index + 1]
                
                if next_token and next_token[1] == '¿':
                    # Es una definición de figura
                    ident = self.get_token()[1]  # consumir identificador
                    value = self.parse_figure()
                    self.symbol_table[ident] = value
                    continue
                else:
                    # Es una asignación normal
                    ident = self.get_token()[1]  # consumir identificador
                    value = self.parse_value()
                    self.symbol_table[ident] = value
                    continue

            # Si no es identificador ni keyword conocida, error
            raise SyntaxError(f"Error de sintaxis: Token inesperado {key_token}")
        return self.symbol_table

    def get_token(self):
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.current_token_index += 1
            return token
        return None 

    def peek_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    
    def parse_value(self):
        token = self.peek_token()
        if token is None:
            raise SyntaxError("Error de sintaxis: Se esperaba un valor, pero no hay mas tokens")
        
        token_type, token_value = token

        if token_type == 'STRING' or token_type == 'NUMBER':
            self.current_token_index += 1
            return token_value
        elif token_type == 'KEYWORD' and token_value == 'dpop':
           return self.parse_block()
        elif token_type == 'KEYWORD' and token_value == 'lpop':
            return self.parse_array()
        elif token_type == 'KEYWORD' and token_value in ('fpop', 'wpop'):
            return self.parse_bucle()
        elif token_type == 'KEYWORD' and token_value == 'pops':
            return self.parse_fonction()
        elif token_type == 'OPERATOR' and token_value == '(':
            return self.parse_value()
        elif token_type == 'OPERATOR' and token_value == ')':
            return self.parse_value()
        else:
            raise SyntaxError(f"Error de sintaxis: Valor no conocido '{token_value}'")
        
    def parse_block(self):
        if self.peek_token() is None or self.peek_token()[1] != '<':
            raise SyntaxError("Error de sintaxis: Se esperaba '<' para iniciar un diccionario") 
        self.get_token() # Consumir '<' 

        block = {}
        while self.peek_token() and self.peek_token()[1] != '>':
            # Saltar comas si hay alguna al inicio
            if self.peek_token()[1] == ',':
                self.get_token()
                continue
                
            key_token = self.get_token()
            if key_token[0] != 'IDENTIFIER':
                raise SyntaxError(f"Error de sintaxis en bloque: Se esperaba un identificador, se encontro {key_token[1]}")
            
            eq_token = self.get_token()
            if eq_token[1] != ':':
                raise SyntaxError(f"Error de sintaxis en bloque: Se esperaba ':', se encontro {eq_token[1]}")
            
            value = self.parse_value()
            block[key_token[1]] = value
            
            # Consumir coma opcional
            if self.peek_token() and self.peek_token()[1] == ',':
                self.get_token()

        self.get_token() # Consumir '>'
        return block 
    
    def parse_array(self):
        if self.peek_token() is None or self.peek_token()[1] != 'lpop':
            raise SyntaxError("Error de sintaxis: Se esperaba 'lpop' para iniciar un array")
        self.get_token() # Consumir 'lpop'
        if self.peek_token() is None or self.peek_token()[1] != '¿':
            raise SyntaxError("Error de sintaxis: Se esperaba '¿' para iniciar un array")
        self.get_token() # Consumir '¿'

        array = []
        while self.peek_token() and self.peek_token()[1] != '?':
            token_type, token_value = self.peek_token()

            if token_type == 'IDENTIFIER':
                self.get_token()
                if token_value not in self.symbol_table:
                    raise NameError(f"Error de nombre: Identificador '{token_value}' no definido")
                array.append(self.symbol_table[token_value])
            else:
                item = self.parse_value()
                array.append(item)

            if self.peek_token() and self.peek_token()[1] == ',':
                self.get_token() # Consumir ','
             
        self.get_token() # Consumir '?'
        return array
    
    def parse_bucle(self):
        if self.tokens[self.current_token_index - 1][1] == 'fpop':
            if self.peek_token() and self.peek_token()[0] == 'NUMBER':
                start = int(self.get_token()[1])  # Consumir número inicial
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un numero")

            if self.peek_token() and self.peek_token()[1] == '(':
                self.get_token()  # Consumir '('
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '('")

            if self.peek_token() and self.peek_token()[0] == 'NUMBER':
                end = int(self.get_token()[1])  # Consumir número final
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un numero")

            if self.peek_token() and self.peek_token()[1] == ')':
                self.get_token()  # Consumir ')'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba ')'")

            if self.peek_token() and self.peek_token()[1] == '¿':
                self.get_token()  # Consumir '¿'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '¿'")

            body = []
            while self.peek_token() and self.peek_token()[1] != '?':
                body.append(self.get_token())  # Consumir instrucciones

            if self.peek_token() and self.peek_token()[1] == '?':
                self.get_token()  # Consumir '?'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '?'")

            return ('for', start, end, body)

        elif self.tokens[self.current_token_index - 1][1] == 'wpop':
            if self.peek_token() and self.peek_token()[1] == '(':
                self.get_token()  # Consumir '('
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '('")

            if self.peek_token() and self.peek_token()[0] == 'NUMBER':
                count = int(self.get_token()[1])  # Consumir número de repeticiones
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un numero")

            if self.peek_token() and self.peek_token()[1] == ')':
                self.get_token()  # Consumir ')'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba ')'")

            if self.peek_token() and self.peek_token()[1] == '¿':
                self.get_token()  # Consumir '¿'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '¿'")

            body = []
            while self.peek_token() and self.peek_token()[1] != '?':
                body.append(self.get_token())  # Consumir instrucciones

            if self.peek_token() and self.peek_token()[1] == '?':
                self.get_token()  # Consumir '?'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '?'")

            return ('while', count, body)

        return None


    def parse_fonction(self):
        if self.peek_token() and self.peek_token()[0] == 'pops':
            self.get_token() # Consumir 'pops'
            if self.peek_token() and self.peek_token()[0] == 'IDENTIFIER':
                func_name = self.get_token()[1] # Consumir nombre de la funcion
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba un nombre de funcion")
            
            if self.peek_token() and self.peek_token()[1] == '¿':
                self.get_token() # Consumir apertura '¿'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '¿'")
            
            args = []
            while self.peek_token() and self.peek_token()[1] != '?':
                arg = self.parse_value()
                args.append(arg)
                if self.peek_token() and self.peek_token()[1] == ',':
                    self.get_token() # Consumir ','
            
            if self.peek_token() and self.peek_token()[1] == '?':
                self.get_token() # Consumir '?'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '?'")
            
            if self.peek_token() and self.peek_token()[1] == '<':
                self.get_token() # Consumir apertura '<'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '<'")

            body = []
            while self.peek_token() and self.peek_token()[1] != '>':
                body.append(self.get_token()) # Consumir el bloque de instrucciones

            if self.peek_token() and self.peek_token()[1] == '>':
                self.get_token() # Consumir cierre '>'
            else:
                raise SyntaxError("Error de sintaxis: Se esperaba '>'")        

            return ('function_def', func_name, args, body), ('function_name', args, body)
        
        return None
    
    def parse_figure(self):
        """Parsea una definición de figura: IDENTIFIER¿ contenido ?"""
        if self.peek_token() is None or self.peek_token()[1] != '¿':
            raise SyntaxError("Error de sintaxis: Se esperaba '¿' para iniciar una figura")
        self.get_token()  # Consumir '¿'
        
        figure_content = {}
        
        while self.peek_token() and self.peek_token()[1] != '?':
            token = self.peek_token()
            
            # Manejar asignaciones dentro de la figura
            if token[0] == 'IDENTIFIER':
                # Verificar si es una asignación (IDENTIFIER = value)
                if (self.current_token_index + 1 < len(self.tokens) and 
                    self.tokens[self.current_token_index + 1][1] == '='):
                    
                    key = self.get_token()[1]  # consumir identificador
                    self.get_token()  # consumir '='
                    value = self.parse_value()
                    figure_content[key] = value
                    
                    # Consumir coma opcional
                    if self.peek_token() and self.peek_token()[1] == ',':
                        self.get_token()
                        
                # Verificar si es IDENTIFIER seguido de ¿ (como POPS forma ¿)
                elif (self.current_token_index + 2 < len(self.tokens) and 
                      self.tokens[self.current_token_index + 2][1] == '¿'):
                    
                    key1 = self.get_token()[1]  # primer identificador (ej: POPS)
                    key2 = self.get_token()[1]  # segundo identificador (ej: forma)
                    
                    # Parsear como array
                    value = self.parse_array_inline()
                    figure_content[f"{key1}_{key2}"] = value
                    
                    # Consumir coma opcional
                    if self.peek_token() and self.peek_token()[1] == ',':
                        self.get_token()
                else:
                    # Es un identificador sin asignación, lo guardamos como tal
                    key = self.get_token()[1]
                    if key not in figure_content:
                        figure_content[key] = None
            else:
                # Cualquier otro token, lo saltamos por ahora
                self.get_token()
        
        if self.peek_token() and self.peek_token()[1] == '?':
            self.get_token()  # Consumir '?' de cierre
        else:
            raise SyntaxError("Error de sintaxis: Se esperaba '?' para cerrar la figura")
            
        return figure_content
    
    def parse_array_inline(self):
        """Parsea un array inline sin la palabra clave lpop: ¿...?"""
        if self.peek_token() is None or self.peek_token()[1] != '¿':
            raise SyntaxError("Error de sintaxis: Se esperaba '¿' para iniciar un array inline")
        self.get_token() # Consumir '¿'

        array = []
        while self.peek_token() and self.peek_token()[1] != '?':
            token_type, token_value = self.peek_token()

            if token_type == 'IDENTIFIER':
                self.get_token()
                if token_value not in self.symbol_table:
                    # Si no está en la tabla de símbolos, lo tratamos como un literal
                    array.append(token_value)
                else:
                    array.append(self.symbol_table[token_value])
            elif token_type == 'OPERATOR' and token_value == '¿':
                # Array anidado
                sub_array = self.parse_array_inline()
                array.append(sub_array)
            else:
                item = self.parse_value()
                array.append(item)

            if self.peek_token() and self.peek_token()[1] == ',':
                self.get_token() # Consumir ','
             
        self.get_token() # Consumir '?'
        return array

def load_source_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: El archivo {file_path} no existe.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
    
def save_ast_to_file(ast, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(ast, file, indent=4)
        print(f"AST guardado en {file_path}")

    except Exception as e:   
        print(f"Error al guardar el AST: {e}")

file_path = 'snake.dnm'
ast_file_path = 'arboldnm.ast'

source_code = load_source_file(file_path)

if source_code:
    print("Lexer")
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    print("Tokens reconocidos:")
    for token in tokens:
        print(token)

    print("\n Parser")
    parser = Parser(tokens)
    try:
        ast_and_symbol_table = parser.parse()
        print("Sintaxis correcta. Se ha construido el Arbol de Sintaxis Abstracta (AST) / Tabla de Simbolos.")
        print("Contenido del AST:")
        print(json.dumps(ast_and_symbol_table, indent=4))
        
        save_ast_to_file(ast_and_symbol_table, ast_file_path)
        
    except (SyntaxError, NameError) as e:
        print(f"Error en la sintaxis: {e}")
