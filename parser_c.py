# parser_c.py
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

# Funções auxiliares em C, conforme especificado no trabalho 
c_code_helpers = [
    '// Funcoes auxiliares para os dispositivos',
    'void ligar(char* namedevice) { printf("%s ligado!\\n", namedevice); }',
    'void desligar(char* namedevice) { printf("%s desligado!\\n", namedevice); }',
    'void alerta(char* namedevice, char* msg) { printf("%s recebeu o alerta: %s\\n", namedevice, msg); }',
    'void alerta_obs(char* namedevice, char* msg, int obs_val) { printf("%s recebeu o alerta: %s %d\\n", namedevice, msg, obs_val); }\n'
]

c_code_globals = ['// Variaveis globais para observations']
c_code_main = []

# --- Regras da Gramática e Ações Semânticas ---

def p_program(p):
    'program : devices cmds'
    p[0] = "Compilado com sucesso!"

def p_devices_multiple(p):
    'devices : device devices'
    pass

def p_devices_single(p):
    'devices : device'
    pass

def p_device_simple(p):
    'device : DISPOSITIVO ":" "{" NAMEDEVICE "}"'
    dev_name = p[4]
    symbol_table['devices'][dev_name] = {'has_observation': False}

def p_device_observation(p):
    'device : DISPOSITIVO ":" "{" NAMEDEVICE "," NAMEDEVICE "}"'
    dev_name = p[4]
    obs_name = p[6]
    symbol_table['devices'][dev_name] = {'has_observation': True, 'obs_name': obs_name}
    # Toda observation não definida começa com 0 
    if obs_name not in symbol_table['observations']:
        symbol_table['observations'][obs_name] = 0
        c_code_globals.append(f'int {obs_name} = 0;')

# --- Comandos ---
def p_cmds_multiple(p):
    'cmds : cmd "." cmds'
    pass

def p_cmds_single(p):
    'cmds : cmd "."'
    pass
    
def p_cmds_empty(p):
    'cmds : '
    pass # Gramática pode terminar após a definição de devices

def p_cmd(p):
    '''cmd : attrib
           | obsact
           | act'''
    p[0] = p[1]

# ATTRIB -> set observation = VAR 
def p_attrib(p):
    'attrib : SET NAMEDEVICE "=" var'
    obs_name = p[2]
    value = p[4]
    if obs_name in symbol_table['observations']:
        symbol_table['observations'][obs_name] = value
        c_code_main.append(f'    {obs_name} = {value};')
    else:
        print(f"Erro Semântico: Observation '{obs_name}' não declarada.")

def p_var(p):
    '''var : NUM
           | BOOL'''
    if isinstance(p[1], int):
        p[0] = p[1]
    else:
        p[0] = 'true' if p[1] == 'TRUE' else 'false'

# OBSACT -> se OBS entao ACT [senao ACT]
def p_obsact_if(p):
    'obsact : SE obs ENTAO act'
    p[0] = f'if ({p[2]}) {{\n        {p[4]}\n    }}'
    c_code_main.append(p[0])

def p_obsact_if_else(p):
    'obsact : SE obs ENTAO act SENAO act'
    p[0] = f'if ({p[2]}) {{\n        {p[4]}\n    }} else {{\n        {p[6]}\n    }}'
    c_code_main.append(p[0])

# OBS -> observation oplogic VAR [&& OBS]
def p_obs_single(p):
    'obs : NAMEDEVICE oplogic var'
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_obs_multiple(p):
    'obs : NAMEDEVICE oplogic var E_LOGICO obs'
    p[0] = f'({p[1]} {p[2]} {p[3]}) && ({p[5]})'

def p_oplogic(p):
    """oplogic : GT
               | LT
               | MAIOR_IGUAL
               | MENOR_IGUAL
               | IGUAL_IGUAL
               | DIFERENTE"""
    p[0] = p[1]

# ACT -> ACTION namedevice | enviar alerta ...
def p_act_action(p):
    'act : action NAMEDEVICE'
    code = f'    {p[1]}("{p[2]}");'
    c_code_main.append(code)
    p[0] = code  # Setting p[0] is not strictly necessary but is good practice

def p_act_alerta_msg(p):
    'act : ENVIAR ALERTA "(" MSG ")" NAMEDEVICE'
    code = f'    alerta("{p[6]}", "{p[4]}");'
    c_code_main.append(code)
    p[0] = code

def p_act_alerta_obs(p):
    'act : ENVIAR ALERTA "(" MSG "," NAMEDEVICE ")" NAMEDEVICE'
    code = f'    alerta_obs("{p[8]}", "{p[4]}", {p[6]});'
    c_code_main.append(code)
    p[0] = code
    
# FUNCIONALIDADE ADICIONAL: Envio broadcast
def p_act_broadcast(p):
    'act : ENVIAR ALERTA "(" MSG ")" PARA TODOS ":" dev_list'
    msg = p[4]
    dev_list = p[9]
    # Gera uma chamada de função para cada dispositivo na lista
    for dev in dev_list:
        c_code_main.append(f'    alerta("{dev}", "{msg}");')
    p[0] = "broadcast generated" # Set p[0] to something descriptive

def p_dev_list_multiple(p):
    'dev_list : NAMEDEVICE "," dev_list'
    p[0] = [p[1]] + p[3]

def p_dev_list_single(p):
    'dev_list : NAMEDEVICE'
    p[0] = [p[1]]
    
def p_action(p):
    '''action : LIGAR
              | DESLIGAR'''
    p[0] = p[1]

# Erro de sintaxe
def p_error(p):
    if p:
        print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else:
        print("Erro de sintaxe no final do arquivo")

# Constrói o parser
parser = yacc.yacc()

# Função principal para compilar
def compile_to_c(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
    
    parser.parse(data)
    
    # Monta o arquivo C final
    final_c_code = []
    final_c_code.extend(c_code_includes)
    final_c_code.extend(c_code_globals)
    final_c_code.extend(c_code_helpers)
    final_c_code.append('int main() {')
    final_c_code.extend(c_code_main)
    final_c_code.append('    return 0;')
    final_c_code.append('}')
    
    output_filename = file_path.replace('.obsact', '.c')
    with open(output_filename, 'w') as f:
        f.write('\n'.join(final_c_code))
    
    print(f"Arquivo C '{output_filename}' gerado com sucesso!")


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        compile_to_c(sys.argv[1])
    else:
        print("Por favor, forneça o nome do arquivo .obsact")