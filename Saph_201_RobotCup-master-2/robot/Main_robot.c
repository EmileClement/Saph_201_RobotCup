
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
int indice_a_modifie = 1;
char message_0[50];
char message_1[50];
char message_vide = '0';
float front, lat, rot, T_front, T_lat = 0;
int flag_msg = 0;
int flag_a_traite = 0;

void asser(float Vx, float Vy, float gammaz)
{
    float wa = rapport_vitesse*(Vx + 100 * gammaz);
    float wb = rapport_vitesse*( -0.5 * Vx - (root3 / 2) * Vy + 100 * gammaz);
    float wc = rapport_vitesse*( -0.5 * Vx + (root3 / 2) * Vy + 100 * gammaz);
    myax12a.SetCRSpeed(wa);
    myax12b.SetCRSpeed(wb);
    myax12c.SetCRSpeed(wc);
}

void send_stat()
{
    coach.printf("S%f,%f,%f,%f,%f \n", front, lat, rot, T_front, T_lat );
}

void mise_a_zero_msg_0()
{
    for(i=0; i<50; i++) { //On réinitialise la chaîne de caractères
        message_0[i] = message_vide;
    }
}


void mise_a_zero_msg_1()
{
    for(i=0; i<50; i++) { //On réinitialise la chaîne de caractères
        message_1[i] = message_vide;
    }
}

void callback_serial()
{
    last_read = coach.getc();
    if (last_read == 'S') {
        send_stat();
    } else if (last_read == ';') {
        coach.puts("EOL");
        if (flag_msg == 0) {
            mise_a_zero_msg_1();
            flag_msg = 1;
        } else {
            mise_a_zero_msg_0();
            flag_msg = 0;
        }
        flag_a_traite = 1;
        indice_a_modifie = 0;
    } else {
        if (flag_msg == 0) {
            message_0[indice_a_modifie] = last_read;
        } else {
            message_1[indice_a_modifie] = last_read;
        }
        indice_a_modifie++;
    }
}

void reception_com()
{
    if (flag_a_traite == 1) {
        coach.puts("tratement");
        if (flag_msg == 0) {
            sscanf(message_1,"%f,%f,%f,%f,%f;", &front, &lat, &rot, &front, &lat );
        } else {
            sscanf(message_0,"%f,%f,%f,%f,%f;", &front, &lat, &rot, &front, &lat );
        }
        flag_a_traite = 0;
    }
}

void setup()
{
    coach.baud(115200);
    myax12a.SetMode(1);
    myax12b.SetMode(1);
    myax12c.SetMode(1);
    coach.puts("stl");
    coach.attach(&callback_serial);
}

int main()
{
    setup();
    while (true) {
        reception_com();
        asser(front, lat, rot);
    }

}
