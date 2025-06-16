import ply.lex as lex

tokens = [
    'NAMEDEVICE', 'MSG', 'NUM',
    'MAIOR_IGUAL', 'MENOR_IGUAL', 'IGUAL_IGUAL', 'DIFERENTE',
    'E_LOGICO', 'GT', 'LT'
]

reserved = {
    'dispositivo': 'DISPOSITIVO', 'set': 'SET', 'se': 'SE', 'entao': 'ENTAO',
    'senao': 'SENAO', 'enviar': 'ENVIAR', 'alerta': 'ALERTA', 'ligar': 'LIGAR',
    'desligar': 'DESLIGAR', 'para': 'PARA', 'todos': 'TODOS',
    'TRUE': 'BOOL', 'FALSE': 'BOOL'
}

tokens = tokens + list(set(reserved.values()))

t_MAIOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_IGUAL_IGUAL = r'=='
t_DIFERENTE = r'!='
t_E_LOGICO = r'&&'
t_GT = r'>'
t_LT = r'<'
t_ignore = ' \t'
literals = ['{', '}', ',', '=', '.', '(', ')', ':']

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_MSG(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

def t_NAMEDEVICE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAMEDEVICE')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()