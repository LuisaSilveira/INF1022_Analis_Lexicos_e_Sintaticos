#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Variaveis globais para observations
int monitor = 0;
int celular = 0;
int temperatura = 0;
// Funcoes auxiliares para os dispositivos
void ligar(char* namedevice) { printf("%s ligado!\n", namedevice); }
void desligar(char* namedevice) { printf("%s desligado!\n", namedevice); }
void alerta(char* namedevice, char* msg) { printf("%s recebeu o alerta: %s\n", namedevice, msg); }
void alerta_obs(char* namedevice, char* msg, int obs_val) { printf("%s recebeu o alerta: %s %d\n", namedevice, msg, obs_val); }

int main() {
    temperatura = 40;
    if (temperatura > 30) {
        alerta_obs("monitor", " Temperatura em ", temperatura);
        alerta_obs("celular", " Temperatura em ", temperatura);
    }
    return 0;
}