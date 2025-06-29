#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Variaveis globais para observations
int temperatura = 0;
int status = 0;
int modo = 0;
// Funcoes auxiliares para os dispositivos
void ligar(char* namedevice) { printf("%s ligado!\n", namedevice); }
void desligar(char* namedevice) { printf("%s desligado!\n", namedevice); }
void alerta(char* namedevice, char* msg) { printf("%s recebeu o alerta: %s\n", namedevice, msg); }
void alerta_obs(char* namedevice, char* msg, int obs_val) { printf("%s recebeu o alerta: %s %d\n", namedevice, msg, obs_val); }

int main() {
    temperatura = 32;
    status = false;
    modo = 0;
    if (temperatura > 25) {
        if (status == true) {
            modo = 1;
        } else {
            modo = 2;
        }
    } else {
        alerta("Monitor", "Temperatura agradavel.");
    }
    return 0;
}