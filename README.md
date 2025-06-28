# INF1022 - Analisadores Léxicos e Sintáticos

Trabalho Final da Matéria Analisadores Léxicos e Sintáticos da Universidade PUC-Rio

## Descrição do Projeto

Este projeto implementa um compilador para a linguagem **ObsAct** (Observation-Action), que permite definir dispositivos IoT e suas regras de comportamento. O compilador traduz código ObsAct para código C executável.

## Setup do Código

### Pré-requisitos

- Python 3.7+
- GCC (para compilar o código C gerado)

### Instalação

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv/Scripts/activate

# Instalar dependências
pip install -r requirements.txt
```

## Como Usar

### 1. Compilar arquivo .obsact para C

```bash
python parser_c.py arquivo.obsact
```

### 2. Compilar e executar o código C

```bash
gcc arquivo.c -o arquivo.exe
./arquivo.exe
```

### 3. Exemplo completo

```bash
python parser_c.py teste_enunciado1.obsact
gcc teste_enunciado1.c -o teste_enunciado1.exe
./teste_enunciado1.exe
```

## Sintaxe da Linguagem ObsAct

### Declaração de Dispositivos

```
dispositivo : { NomeDispositivo }                    // Dispositivo simples
dispositivo : { NomeDispositivo, observacao }        // Dispositivo com observação
```

### Atribuição de Valores

```
set observacao = valor .
```

### Estruturas Condicionais

```
se condicao entao acao .
se condicao entao acao senao acao .
```

### Ações

```
ligar dispositivo .
desligar dispositivo .
enviar alerta ("mensagem") dispositivo .
enviar alerta ("mensagem", observacao) dispositivo .
enviar alerta ("mensagem") para todos : dispositivo1, dispositivo2 .
```

## Arquivos de Teste

- `teste_enunciado1.obsact` - Exemplo básico com termômetro e ventilador
- `teste_enunciado2.obsact` - Exemplo com broadcast de alertas
- `teste_enunciado3.obsact` - Exemplo com múltiplas condições

## Estrutura do Projeto

- `lexer.py` - Analisador léxico
- `parser_c.py` - Analisador sintático e gerador de código C
- `requirements.txt` - Dependências do projeto
