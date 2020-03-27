
/* #include <mbed_events.h> */
#include "mbed.h"
#include "AX12.h"

DigitalOut alivenessLED(LED1);
DigitalOut testLed(LED2);

Serial coach(D1, D0);

const float rapport_vitesse = 0.019383809*0.026315;
const float root3 = 1.7321;
AX12 myax12a (PC_4, PC_5, 2);
AX12 myax12b (PC_4, PC_5, 3);
AX12 myax12c (PC_4, PC_5, 4);

int i = 0;
char last_read;
int indice_a_modifie = 0;
char message[50];
char message_vide = 0;
float front, lat, rot, T_front, T_lat = 0;

/*typedef struct {
    float front;
    float lat;
    float rot ;
} dep;
typedef struct {
    float front;
    float lat;
} tire;*/
/*
void blinkCallback(void)
{
    alivenessLED = !alivenessLED;
}*/

void setup(){
    //eventQueue.call_every(500, blinkCallback);
    coach.baud(115200);
    myax12a.SetMode(1);
    myax12b.SetMode(1);
    myax12c.SetMode(1);
    }
    
void asser(float Vx, float Vy, float gammaz){
    float wa = rapport_vitesse*(Vx + 100 * gammaz);
    float wb = rapport_vitesse*( -0.5 * Vx - (root3 / 2) * Vy + 100 * gammaz);
    float wc = rapport_vitesse*( -0.5 * Vx + (root3 / 2) * Vy + 100 * gammaz);
    myax12a.SetCRSpeed(wa);
    myax12b.SetCRSpeed(wb);
    myax12c.SetCRSpeed(wc);
    }

void send_stat(){
    coach.printf("%f,%f,%f,%f,%f \n", front, lat, rot, front, lat );
    }

void mise_a_zero_msg(){
    for(i=0;i<50;i++){//On réinitialise la chaîne de caractères
        message[i] = message_vide;}
    indice_a_modifie = 0;
    }
    
void reception_com(){
    if (coach.readable()) {
        last_read = coach.getc();
        if (last_read == 'A') {
            indice_a_modifie = 0;
            last_read = coach.getc();
            while ((last_read != ';')){
                message[indice_a_modifie] = last_read;
                coach.printf("|%i|%s|", indice_a_modifie, message);
                indice_a_modifie ++;
                last_read = coach.getc();}
            message[indice_a_modifie] = last_read;
            sscanf(message,"%f,%f,%f,%f,%f;", &front, &lat, &rot, &front, &lat );
            mise_a_zero_msg();
            }
        if (last_read == 'S') {
            send_stat();
            }
    }}

int main(){
    setup();
    while (true){
        reception_com();
        asser(front, lat, rot);
        }

    }