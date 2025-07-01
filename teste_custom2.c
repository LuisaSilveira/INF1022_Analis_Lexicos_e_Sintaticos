#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Variaveis globais para observations
int temperatura = 0;
int aberta = 0;
// Funcoes auxiliares para os dispositivos
void ligar(char* namedevice) { printf("%s ligado!\n", namedevice); }
void desligar(char* namedevice) { printf("%s desligado!\n", namedevice); }
void alerta(char* namedevice, char* msg) { printf("%s recebeu o alerta: %s\n", namedevice, msg); }
void alerta_obs(char* namedevice, char* msg, int obs_val) { printf("%s recebeu o alerta: %s %d\n", namedevice, msg, obs_val); }

int main() {
    temperatura = 15;
    aberta = false;
    if ((temperatura < 18) && (aberta == false)) {
        ligar("aquecedor");
    } else {
        if (temperatura > 25) {
            ligar("ar_condicionado");
        } else {
            alerta("Monitor", "Temperatura Confortavel");
        }
    }
    return 0;
}