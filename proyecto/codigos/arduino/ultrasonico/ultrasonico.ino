#include <SoftwareSerial.h>

// Configuración de Comunicación Serial con el ESP32
SoftwareSerial espSerial(11, 10); // RX (11), TX (10)

// ---------------------------
// Conexiones de Pines
// ---------------------------
#define ENA 5
#define IN1 8
#define IN2 9
#define ENB 6
#define IN3_MOTOR 7
#define IN4_MOTOR 12

#define TRIG 2
#define ECHO 3

#define S0 4
#define S1 A5
#define S2 A0
#define S3 A1
#define OUT 13

long duracion;
int distancia;
String ultimaClasificacion = "Organico";

// ---------------------------
// SETUP ARDUINO
// ---------------------------
void setup() {
    Serial.begin(9600);
    espSerial.begin(9600); // Inicia la comunicación con el ESP32

    // Inicialización de Pines...
    pinMode(ENA, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(ENB, OUTPUT);
    pinMode(IN3_MOTOR, OUTPUT);
    pinMode(IN4_MOTOR, OUTPUT);
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    pinMode(S0, OUTPUT);
    pinMode(S1, OUTPUT);
    pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(OUT, INPUT);

    // Configurar escala de frecuencia (20%)
    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);
}

// ---------------------------
// Funciones de motores, sensores, y envio serial...
// ---------------------------
void adelante() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3_MOTOR, HIGH);
    digitalWrite(IN4_MOTOR, LOW);
    analogWrite(ENA, 150);
    analogWrite(ENB, 150);
}

void parar() {
    digitalWrite(IN1, LOW);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3_MOTOR, LOW);
    digitalWrite(IN4_MOTOR, LOW);
}

void girarDerecha() {
    digitalWrite(IN1, HIGH);
    digitalWrite(IN2, LOW);
    digitalWrite(IN3_MOTOR, LOW);
    digitalWrite(IN4_MOTOR, HIGH);
    analogWrite(ENA, 150);
    analogWrite(ENB, 150);
}

int medirDistancia() {
    digitalWrite(TRIG, LOW); delayMicroseconds(2);
    digitalWrite(TRIG, HIGH); delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    long duracion = pulseIn(ECHO, HIGH);
    distancia = duracion * 0.034 / 2;
    return distancia;
}

int leerColor(int s2, int s3) {
    digitalWrite(S2, s2);
    digitalWrite(S3, s3);
    return pulseIn(OUT, LOW);
}

void detectarBasura() {
    int rojo = leerColor(LOW, LOW);
    int azul = leerColor(LOW, HIGH);
    int verde = leerColor(HIGH, HIGH);

    if (rojo < azul && rojo < verde) {
        ultimaClasificacion = "Papel";
    } else if (azul < rojo && azul < verde) {
        ultimaClasificacion = "Plastico";
    } else {
        ultimaClasificacion = "Organico";
    }
}

void enviarClasificacion() {
    espSerial.println(ultimaClasificacion); 
}

// ---------------------------
// LOOP ARDUINO
// ---------------------------
void loop() {
    int d = medirDistancia();

    if (d > 20) {
        adelante();
        detectarBasura(); 
        delay(500);
    } else {
        parar();
        delay(300);
        
        // El Arduino envía la clasificación al ESP32
        enviarClasificacion(); 
        
        girarDerecha();
        delay(600);
        parar();
    }
}
