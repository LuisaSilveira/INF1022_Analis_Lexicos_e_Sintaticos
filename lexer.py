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