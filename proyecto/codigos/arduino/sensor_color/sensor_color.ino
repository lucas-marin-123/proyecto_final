// 3. COLOR: Muestra los valores RAW (frecuencia) de los canales RGB.

// Pines de Sensor de Color (TCS3200)
#define S0 4
#define S1 A5 
#define S2 A0
#define S3 A1
#define OUT 13

void setup() {
    Serial.begin(9600);
    Serial.println("INICIANDO TEST DE SENSOR DE COLOR (TCS3200)");
    
    // Configuración de Pines
    pinMode(S0, OUTPUT); pinMode(S1, OUTPUT); 
    pinMode(S2, OUTPUT); pinMode(S3, OUTPUT);
    pinMode(OUT, INPUT);

    // Configurar escala de frecuencia (20%)
    digitalWrite(S0, HIGH);
    digitalWrite(S1, LOW);
} 

int leerColor(int s2, int s3) {
    digitalWrite(S2, s2);
    digitalWrite(S3, s3);
    // pulseIn lee el tiempo que el pin pasa en LOW, proporcional a la frecuencia.
    return pulseIn(OUT, LOW);
}

void loop() { 
    int rojo = leerColor(LOW, LOW);   // Rojo
    int azul = leerColor(LOW, HIGH);  // Azul
    int verde = leerColor(HIGH, HIGH);// Verde

    // Los valores más BAJOS indican que se detectó más de ese color (menos tiempo en LOW)
    Serial.print("R: "); Serial.print(rojo);
    Serial.print(" G: "); Serial.print(verde);
    Serial.print(" B: "); Serial.println(azul);
    
    delay(500);
}