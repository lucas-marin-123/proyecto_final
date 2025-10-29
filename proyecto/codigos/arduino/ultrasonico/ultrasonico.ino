// 2. ULTRASÓNICO: Muestra la distancia medida continuamente.

// Pines de Ultrasónico
#define TRIG 2
#define ECHO 3

void setup() {
    Serial.begin(9600);
    Serial.println("INICIANDO TEST DE ULTRASONICO");
    
    // Configuración de Pines
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
} 

int medirDistancia() {
    // Envía pulso
    digitalWrite(TRIG, LOW); delayMicroseconds(2);
    digitalWrite(TRIG, HIGH); delayMicroseconds(10);
    digitalWrite(TRIG, LOW);
    
    // Mide y calcula distancia en cm
    long duracion = pulseIn(ECHO, HIGH);
    int distancia = duracion * 0.034 / 2;
    return distancia;
}

void loop() { 
    int d = medirDistancia();
    
    Serial.print("Distancia: ");
    Serial.print(d);
    Serial.println(" cm");

    delay(300); 
}