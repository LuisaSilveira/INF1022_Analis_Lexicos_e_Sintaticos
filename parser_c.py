import ply.yacc as yacc
from lexer import tokens, lexer

# --- Global variables for code generation ---
symbol_table = { 'devices': {}, 'observations': {} }
c_code_includes = ['#include <stdio.h>', '#include <string.h>', '#include <stdbool.h>\n']
c_code_helpers = [
    '// Funcoes auxiliares para os dispositivos',
    'void ligar(char* namedevice) { printf("%s ligado!\\n", namedevice); }',
    'void desligar(char* namedevice) { printf("%s desligado!\\n", namedevice); }',
    'void alerta(char* namedevice, char* msg) { printf("%s recebeu o alerta: %s\\n", namedevice, msg); }',
    'void alerta_obs(char* namedevice, char* msg, int obs_val) { printf("%s recebeu o alerta: %s %d\\n", namedevice, msg, obs_val); }\n'
]
c_code_globals = ['// Variaveis globais para observations']
c_code_main_body = []

# --- Grammar Rules ---

def p_program(p):
    'program : devices cmds'
    global c_code_main_body
    c_code_main_body = p[2]

def p_devices_list(p):
    'devices : device devices'
    # This rule is for structure, no specific action needed here.
    pass

def p_devices_single(p):
    'devices : device'
    # This rule is for structure, no specific action needed here.
    pass

def p_device_simple(p):
    'device : DISPOSITIVO ":" "{" NAMEDEVICE "}"'
    symbol_table['devices'][p[4]] = {'has_observation': False}
def p_device_observation(p):
    'device : DISPOSITIVO ":" "{" NAMEDEVICE "," NAMEDEVICE "}"'
    dev_name, obs_name = p[4], p[6]
    symbol_table['devices'][dev_name] = {'has_observation': True, 'obs_name': obs_name}
    if obs_name not in symbol_table['observations']:
        symbol_table['observations'][obs_name] = 0
        c_code_globals.append(f'int {obs_name} = 0;')

def p_cmds_list(p):
    'cmds : cmd "." cmds'
    p[0] = p[1] + p[3]
def p_cmds_empty(p):
    'cmds : '
    p[0] = []

# --- Rules for 'cmd' (replaces 'cmd : attrib | obsact | act') ---
def p_cmd_attrib(p):
    'cmd : attrib'
    p[0] = p[1]

def p_cmd_obsact(p):
    'cmd : obsact'
    p[0] = p[1]

def p_cmd_act(p):
    'cmd : act'
    p[0] = p[1]

# Mude esta função em parser_c.py
def p_attrib(p):
    'attrib : SET NAMEDEVICE "=" var'
    obs_name, value = p[2], p[4]
    if obs_name in symbol_table['observations']:
        symbol_table['observations'][obs_name] = value
        # ANTES: retornava uma string
        # AGORA: retorna uma LISTA
        p[0] = [f'    {obs_name} = {value};']
    else: 
        print(f"Erro Semântico: Observation '{obs_name}' não declarada.")
        p[0] = ['']

# --- Rules for 'var' (replaces 'var : NUM | BOOL') ---
def p_var_num(p):
    'var : NUM'
    p[0] = p[1]
def p_var_bool(p):
    'var : BOOL'
    p[0] = 'true' if p[1] == 'TRUE' else 'false'

# Mude estas duas funções em parser_c.py

def p_obsact_if(p):
    'obsact : SE obs ENTAO act'
    # ANTES: retornava uma string
    # AGORA: Envolve a string em colchetes para retornar uma LISTA
    p[0] = [f'    if ({p[2]}) {{\n' + '\n'.join(p[4]) + '\n    }']

def p_obsact_if_else(p):
    'obsact : SE obs ENTAO act SENAO act'
    # ANTES: retornava uma string
    # AGORA: Envolve a string em colchetes para retornar uma LISTA
    p[0] = [f'    if ({p[2]}) {{\n' + '\n'.join(p[4]) + '\n    }} else {{\n' + '\n'.join(p[6]) + '\n    }}']

def p_obs(p):
    'obs : NAMEDEVICE oplogic var'
    p[0] = f'{p[1]} {p[2]} {p[3]}'
def p_obs_multiple(p):
    'obs : NAMEDEVICE oplogic var E_LOGICO obs'
    p[0] = f'({p[1]} {p[2]} {p[3]}) && ({p[5]})'

# --- Rules for 'oplogic' (replaces rules with |) ---
def p_oplogic_gt(p): 'oplogic : GT'; p[0] = p[1]
def p_oplogic_lt(p): 'oplogic : LT'; p[0] = p[1]
def p_oplogic_ge(p): 'oplogic : MAIOR_IGUAL'; p[0] = p[1]
def p_oplogic_le(p): 'oplogic : MENOR_IGUAL'; p[0] = p[1]
def p_oplogic_eq(p): 'oplogic : IGUAL_IGUAL'; p[0] = p[1]
def p_oplogic_ne(p): 'oplogic : DIFERENTE'; p[0] = p[1]

def p_act_action(p):
    'act : action NAMEDEVICE'
    p[0] = [f'        {p[1]}("{p[2]}");']
def p_act_alerta_msg(p):
    'act : ENVIAR ALERTA "(" MSG ")" NAMEDEVICE'
    p[0] = [f'        alerta("{p[6]}", "{p[4]}");']
def p_act_alerta_obs(p):
    'act : ENVIAR ALERTA "(" MSG "," NAMEDEVICE ")" NAMEDEVICE'
    p[0] = [f'        alerta_obs("{p[8]}", "{p[4]}", {p[6]});']
def p_act_broadcast(p):
    'act : ENVIAR ALERTA "(" MSG ")" PARA TODOS ":" dev_list'
    p[0] = [f'        alerta("{dev}", "{p[4]}");' for dev in p[9]]
def p_act_broadcast_with_obs(p):
    'act : ENVIAR ALERTA "(" MSG "," NAMEDEVICE ")" PARA TODOS ":" dev_list'
    p[0] = [f'        alerta_obs("{dev}", "{p[4]}", {p[6]});' for dev in p[11]]

def p_dev_list_multiple(p): 'dev_list : NAMEDEVICE "," dev_list'; p[0] = [p[1]] + p[3]
def p_dev_list_single(p): 'dev_list : NAMEDEVICE'; p[0] = [p[1]]

def p_action_ligar(p): 'action : LIGAR'; p[0] = p[1]
def p_action_desligar(p): 'action : DESLIGAR'; p[0] = p[1]

def p_error(p):
    if p: print(f"Erro de sintaxe em '{p.value}' na linha {p.lineno}")
    else: print("Erro de sintaxe no final do arquivo")

parser = yacc.yacc()

def compile_to_c(file_path):
    with open(file_path, 'r') as f: data = f.read()
    parser.parse(data, lexer=lexer)
    final_c_code = c_code_includes + c_code_globals + c_code_helpers + \
                   ['int main() {'] + c_code_main_body + ['    return 0;', '}']
    output_filename = file_path.replace('.obsact', '.c')
    with open(output_filename, 'w') as f: f.write('\n'.join(final_c_code))
    print(f"Arquivo C '{output_filename}' gerado com sucesso!")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1: compile_to_c(sys.argv[1])
    else: print("Por favor, forneça o nome do arquivo .obsact")