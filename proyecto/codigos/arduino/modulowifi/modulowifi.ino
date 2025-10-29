// 4. SERIAL/ESP32: Envía un mensaje de prueba al ESP32 cada 2 segundos.

#include <SoftwareSerial.h>

// Pines de SoftwareSerial
SoftwareSerial espSerial(11, 10); // RX (11), TX (10)

void setup() {
    Serial.begin(9600);
    espSerial.begin(9600); 
    
    Serial.println("INICIANDO TEST DE COMUNICACION CON ESP32");
} 

void loop() { 
    String mensaje = "Arduino-OK-" + String(millis() / 1000);
    
    // Envía por el puerto USB para depuración
    Serial.print("Enviando: ");
    Serial.println(mensaje);
    
    // Envía el mensaje al ESP32
    espSerial.println(mensaje); 
    
    delay(2000); 
}