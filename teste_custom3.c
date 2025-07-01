#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Variaveis globais para observations
int hora = 0;
int dia_util = 0;
int pronta = 0;
// Funcoes auxiliares para os dispositivos
void ligar(char* namedevice) { printf("%s ligado!\n", namedevice); }
void desligar(char* namedevice) { printf("%s desligado!\n", namedevice); }
void alerta(char* namedevice, char* msg) { printf("%s recebeu o alerta: %s\n", namedevice, msg); }
void alerta_obs(char* namedevice, char* msg, int obs_val) { printf("%s recebeu o alerta: %s %d\n", namedevice, msg, obs_val); }

int main() {
    hora = 7;
    dia_util = true;
    pronta = true;
    if ((hora == 7) && (dia_util == true)) {
        alerta("Celular", "Hora de acordar!");
        alerta("assistente_voz", "Hora de acordar!");
    }
    if (pronta == true) {
        alerta("Monitor", "Cafe esta pronto!");
    }
    ligar("luzes_quarto");
    return 0;
}