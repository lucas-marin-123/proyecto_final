// 1. MOTORES: Avanza y se detiene cada 2 segundos.

// Pines de Motores (Misma configuracion de tu proyecto)
#define ENA 5           // Velocidad Motor Izquierdo
#define IN1 8           // Control M. Izquierdo 1
#define IN2 9           // Control M. Izquierdo 2
#define ENB 6           // Velocidad Motor Derecho
#define IN3_MOTOR 7     // Control M. Derecho 1
#define IN4_MOTOR 12    // Control M. Derecho 2

void setup() {
    Serial.begin(9600);
    Serial.println("INICIANDO TEST DE MOTORES");
    
    // Configuración de Pines como Salida
    pinMode(ENA, OUTPUT); pinMode(IN1, OUTPUT); pinMode(IN2, OUTPUT);
    pinMode(ENB, OUTPUT); pinMode(IN3_MOTOR, OUTPUT); pinMode(IN4_MOTOR, OUTPUT);
} 

void adelante() {
    // Motor Izquierdo Adelante
    digitalWrite(IN1, HIGH); 
    digitalWrite(IN2, LOW);
    // Motor Derecho Adelante
    digitalWrite(IN3_MOTOR, HIGH); 
    digitalWrite(IN4_MOTOR, LOW);
    // Velocidad
    analogWrite(ENA, 180);
    analogWrite(ENB, 180);
}

void parar() {
    digitalWrite(IN1, LOW); 
    digitalWrite(IN2, LOW);
    digitalWrite(IN3_MOTOR, LOW); 
    digitalWrite(IN4_MOTOR, LOW);
    analogWrite(ENA, 0); 
    analogWrite(ENB, 0);
}

void loop() { 
    Serial.println("AVANZANDO...");
    adelante();
    delay(2000); 

    Serial.println("DETENIDO...");
    parar();
    delay(2000); 
}