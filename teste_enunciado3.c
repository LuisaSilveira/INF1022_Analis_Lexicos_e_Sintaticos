#include <stdio.h>
#include <string.h>
#include <stdbool.h>

// Variaveis globais para observations
int movimento = 0;
int umidade = 0;
int potencia = 0;
// Funcoes auxiliares para os dispositivos
void ligar(char* namedevice) { printf("%s ligado!\n", namedevice); }
void desligar(char* namedevice) { printf("%s desligado!\n", namedevice); }
void alerta(char* namedevice, char* msg) { printf("%s recebeu o alerta: %s\n", namedevice, msg); }
void alerta_obs(char* namedevice, char* msg, int obs_val) { printf("%s recebeu o alerta: %s %d\n", namedevice, msg, obs_val); }

int main() {
    potencia = 100;
    if (umidade < 40) {
        alerta("Monitor", " Ar seco detectado ");
    }
    if (movimento == true) {
        ligar("lampada");
    }} else {{
        desligar("lampada");
    }}
    return 0;
}