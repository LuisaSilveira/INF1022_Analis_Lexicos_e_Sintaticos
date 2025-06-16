import ply.yacc as yacc
from lexer import tokens

# Tabela de Símbolos para armazenar variáveis e dispositivos
symbol_table = {
    'devices': {},
    'observations': {}
}

# --- Geração de Código C ---
# Vamos usar listas para montar o código C
c_code_includes = [
    '#include <stdio.h>',
    '#include <string.h>',
    '#include <stdbool.h>\n'
]