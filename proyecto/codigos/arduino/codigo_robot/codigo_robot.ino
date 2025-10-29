#include <SoftwareSerial.h>

// ----------------------------------------------------
// PINES DE CONTROL Y SENSORES
// ----------------------------------------------------
SoftwareSerial espSerial(11, 10); // RX (11), TX (10) para ESP32

// Motores (Driver L298N/L293D)
#define ENA 5           // Velocidad Motor Izquierdo (PWM)
#define IN1 8           // Control M. Izquierdo 1
#define IN2 9           // Control M. Izquierdo 2
#define ENB 6           // Velocidad Motor Derecho (PWM)
#define IN3_MOTOR 7     // Control M. Derecho 1
#define IN4_MOTOR 12    // Control M. Derecho 2

// Sensor Ultrasónico
#define TRIG 2
#define ECHO 3

// Sensor de Color (TCS3200)
#define S0 4
#define S1 A5 
#define S2 A0
#define S3 A1
#define OUT 13

// ----------------------------------------------------
// VARIABLES GLOBALES Y CONSTANTES (AJUSTE DE CALIBRACIÓN AQUÍ)
// ----------------------------------------------------
// !!! AJUSTA ESTOS VALORES para regular la reacción y lograr que vaya recto !!!
const int VELOCIDAD_IZQUIERDA = 150; 
const int VELOCIDAD_DERECHA = 150;   

const int VELOCIDAD_PIVOTE = 180; 
const int DISTANCIA_OBSTACULO = 20; // cm para detenerse y girar

String ultimaClasificacion = "Organico"; 

// ----------------------------------------------------
// FUNCIÓN DE FRENO (DEFINICIÓN ÚNICA)
// ----------------------------------------------------
void parar() {
    // Implementación del FRENO RÁPIDO
    digitalWrite(IN1, LOW); 
    digitalWrite(IN2, LOW);
    digitalWrite(IN3_MOTOR, LOW); 
    digitalWrite(IN4_MOTOR, LOW);
    analogWrite(ENA, 0); 
    analogWrite(ENB, 0);
}

// ----------------------------------------------------
// SETUP
// ----------------------------------------------------
void setup() {
    Serial.begin(9600);
    espSerial.begin(9600); 
    
    // Configuración de Pines
    pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
    pinMode(ENB, OUTPUT); pinMode(IN3_MOTOR, OUTPUT); pinMode(IN4_MOTOR, OUTPUT);
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    pinMode(S0, OUTPUT); pinMode(S1, OUTPUT); pinMode(S2, OUTPUT);
    pinMode(S3, OUTPUT);
    pinMode(OUT, INPUT);

    // Configurar escala de frecuencia del sensor de color (20%)
    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);
    
    Serial.println("Robot Clasificador Iniciado.");
} 

// ----------------------------------------------------
// FUNCIONES DE MOVIMIENTO (adelante() MODIFICADA)
// ----------------------------------------------------

void adelante() {
    // Mover ambas ruedas adelante
    digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
    digitalWrite(IN3_MOTOR, HIGH); digitalWrite(IN4_MOTOR, LOW);
    
    //  USANDO LAS CONSTANTES SEPARADAS PARA CALIBRACIÓN 
    analogWrite(ENA, VELOCIDAD_IZQUIERDA);
    analogWrite(ENB, VELOCIDAD_DERECHA);
}

// Gira sobre la rueda derecha (Rueda derecha detenida, izquierda avanza)
void girarParaEvitar() {
    Serial.println("Obstaculo. Ejecutando Pivote.");
    
    parar(); // Usamos el freno antes de girar
    delay(300); 
    
    // Rueda Izquierda adelante (Usa VELOCIDAD_PIVOTE)
    digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
    analogWrite(ENA, VELOCIDAD_PIVOTE); 
    
    // Rueda Derecha detenida
    digitalWrite(IN3_MOTOR, LOW); digitalWrite(IN4_MOTOR, LOW); 
    analogWrite(ENB, 0); 
    
    delay(700); // Gira por 0.7 segundos
    
    parar(); // Detiene al finalizar
}

// ----------------------------------------------------
// FUNCIONES DE SENSORES Y COMUNICACIÓN
// ----------------------------------------------------

int medirDistancia() {
    // Mide y calcula distancia en cm
    digitalWrite(TRIG, LOW); delayMicroseconds(2);
    digitalWrite(TRIG, HIGH); delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    long duracion = pulseIn(ECHO, HIGH);
    int distancia = duracion * 0.034 / 2;
    return distancia;
}

int leerColor(int s2, int s3) {
    digitalWrite(S2, s2);
    digitalWrite(S3, s3);
    return pulseIn(OUT, LOW);
}

void detectarBasura() {
    // Lee las componentes de color y actualiza la variable global
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
    Serial.print("Enviando clasificación: ");
    Serial.println(ultimaClasificacion);
    espSerial.println(ultimaClasificacion); 
}

// ----------------------------------------------------
// LOOP PRINCIPAL (AVANCE POR PASOS)
// ----------------------------------------------------
void loop() { 
    
    detectarBasura(); 
    int d = medirDistancia();
    Serial.print("Distancia: "); Serial.println(d);

    if (d > DISTANCIA_OBSTACULO) {
        // MODO AVANCE LIBRE (Pasos: Avance 1s -> Freno 0.5s)
        
        // A. Avance (1 SEGUNDO)
        adelante(); // Usa velocidades calibradas
        delay(1000); 

        // B. Parar y esperar 0.5s
        parar();
        Serial.println("Esperando 0.5s para siguiente chequeo.");
        delay(500); 
        
    } else {
        // MODO OBSTÁCULO (d <= 20 cm)
        
        parar();
        delay(300);
        
        // A. Envía la clasificación del objeto detectado
        enviarClasificacion(); 
        
        // B. Gira para cambiar de dirección
        girarParaEvitar();
        
        // C. Avance corto de escape
        adelante();
        delay(400); 
        parar();
    }
}