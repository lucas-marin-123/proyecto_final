#include <WiFi.h>
#include <WiFiClient.h>

// ---------------------------
// Configuración Wi-Fi
// ---------------------------
const char* ssid = "Conectividad Cordoba";
const char* password = ""; // Contraseña de tu red, si tiene

// IP y Puerto del servidor Python en tu PC
const char* host = "172.17.0.93"; // ¡Verifica que esta sea la IP correcta de tu PC!
const int port = 8888;

// ---------------------------
// FUNCIÓN WI-FI: Envía datos al servidor Python
// ---------------------------
void enviarDato(String data_to_send) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi desconectado.");
        return;
    }
    
    WiFiClient client;
    if (!client.connect(host, port)) {
        Serial.println("Fallo la conexión al servidor Python!");
        return;
    }
    
    client.println(data_to_send); 
    client.stop();
}


// ---------------------------
// SETUP ESP32-S
// ---------------------------
void setup() {
    // Usamos el Serial 0 del ESP32 para comunicarnos con el Arduino
    Serial.begin(9600); 

    // --- Inicialización de Wi-Fi ---
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nESP32: WiFi conectado.");
}

// ---------------------------
// LOOP ESP32-S
// ---------------------------
void loop() {
    // Verificar si hay datos del Arduino disponibles para leer
    if (Serial.available()) {
        // Leer la línea completa (la clasificación) enviada por el Arduino
        String clasificacion = Serial.readStringUntil('\n');
        clasificacion.trim(); 

        if (clasificacion.length() > 0) {
            enviarDato(clasificacion); // Enviar el dato por Wi-Fi
        }
    }
    delay(100);
}