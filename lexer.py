import ply.lex as lex

# Lista de nomes dos tokens. Isso é obrigatório.
tokens = [
    'NAMEDEVICE', 'OBSERVATION', 'MSG', 'NUM', 'BOOL',
    'MAIOR_IGUAL', 'MENOR_IGUAL', 'IGUAL_IGUAL', 'DIFERENTE',
    'E_LOGICO',
]

# Palavras-chave reservadas
# These are otherwise known as terminal symbols
reserved = {
    'dispositivo': 'DISPOSITIVO',
    'set': 'SET',
    'se': 'SE',
    'entao': 'ENTAO',
    'senao': 'SENAO',
    'enviar': 'ENVIAR',
    'alerta': 'ALERTA',
    'ligar': 'LIGAR',
    'desligar': 'DESLIGAR',
    'para': 'PARA',
    'todos': 'TODOS',
    'TRUE': 'BOOL',
    'FALSE': 'BOOL'
}

# Expressões regulares simples para tokens
t_MAIOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_IGUAL_IGUAL = r'=='
t_DIFERENTE = r'!='
t_E_LOGICO = r'&&'
t_ignore = ' \t' # Ignorar espaços e tabs

# Literais de um único caractere
literals = ['{', '}', ',', '=', '>', '<', '.', '(', ')', ':']

# Regra para números inteiros não negativos
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regra para MSG (strings entre aspas)
def t_MSG(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1] # Remove as aspas
    return t

# Regra para NAMEDEVICE e OBSERVATION (e palavras-chave)
# namedevice só pode conter letras 
# observation é uma string 
def t_NAMEDEVICE(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAMEDEVICE') # Checa por palavras reservadas
    if t.type == 'NAMEDEVICE':
        # Na gramática, 'observation' tem a mesma forma de um identificador.
        # Vamos tratar ambos como NAMEDEVICE por enquanto e diferenciar no parser.
        # Para simplificar, podemos renomear este token para IDENTIFIER se preferir.
        pass
    return t

# Regra para lidar com novas linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regra para tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Constrói o lexer
lexer = lex.lex()