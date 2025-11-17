// --- Definición de Pines de Motor (L298N) ---
// Motor A (Izquierdo)
const int enA = 9;   // Pin PWM para la velocidad
const int in1 = 8;   // Dirección 1
const int in2 = 7;   // Dirección 2
// Motor B (Derecho)
const int enB = 6;   // Pin PWM para la velocidad
const int in3 = 5;   // Dirección 1
const int in4 = 4;   // Dirección 2


// --- Definición de Pines de Sensor Ultrasónico (HC-SR04) ---
const int trigPin = 11; // Pin de Disparo
const int echoPin = 10; // Pin de Eco


// --- Definición de Pines de Sensor de Color (TCS3200) ---
// (Nota: Estos pines son solo para configuración. Se requerirá lógica adicional para leer el color)
const int s0 = A0; // Frecuencia Out (No usado en este ejemplo simplificado)
const int s1 = A1; // Control de Escala (No usado en este ejemplo simplificado)
const int s2 = A2; // Filtro de color (Rojo/Claro)
const int s3 = A3; // Filtro de color (Verde/Azul)
const int outPin = 12; // Salida de Frecuencia (Usado para leer el color)


// =======================================================
// === AJUSTES DE CALIBRACIÓN Y LÓGICA ===
// =======================================================
const int VELOCIDAD_BASE = 150; // Velocidad de avance (0-255)

// Offset para compensar el motor que arranca más tarde/es más lento
const int OFFSET_MOTOR_A = 5; // Aumentar si Motor A es más lento (EJEMPLO)
const int OFFSET_MOTOR_B = 0; // Aumentar si Motor B es más lento (EJEMPLO)

// Distancia en cm para que el robot frene y esquive.
const int DISTANCIA_OBSTACULO = 20; 
// =======================================================

// Variable global para la distancia
long duracion;
int distancia_cm;

// --- Configuración Inicial ---
void setup() {
  // Pines de Motor
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);

  // Pines de Ultrasónico
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Pines de Color (Configuración simplificada)
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);
  pinMode(outPin, INPUT);
  
  // Establecer la escala de frecuencia del sensor de color a 20%
  digitalWrite(s0, HIGH);
  digitalWrite(s1, LOW);
  
  // Comunicación Serial (esencial para ver distancias y mensajes)
  Serial.begin(9600);
}

// -------------------------------------------------------------------
// 2. 🧠 BUCLE PRINCIPAL (Lógica de Evasión)
// -------------------------------------------------------------------
void loop() {
  // 1. Leer distancia actual
  distancia_cm = leerDistanciaCM();

  // 2. Imprimir datos (opcional, para depuración)
  Serial.print("Distancia: ");
  Serial.print(distancia_cm);
  Serial.println(" cm");

  // 3. Lógica de Evasión
  if (distancia_cm > 0 && distancia_cm <= DISTANCIA_OBSTACULO) {
    // A. Obstáculo detectado: ¡FRENAR!
    Serial.println("¡OBSTÁCULO! FRENANDO...");
    frenarMotores(); 
    delay(500); // Frenar por medio segundo

    // B. ESQUIVAR (Giro simple a la derecha)
    Serial.println("Esquivando (Derecha)...");
    girarDerecha(VELOCIDAD_BASE);
    delay(1000); // Girar por un segundo

    // C. Después de esquivar, parar y reevaluar
    frenarMotores(); 
    delay(500);

  } else {
    // No hay obstáculo, AVANZAR
    moverAdelante(VELOCIDAD_BASE);
  }

  // 4. Leer el color (Ejecución constante o al detectar residuo)
  // int color_leido = leerColor(); 
  // Aquí iría la lógica de clasificación de residuos basada en el color.

  delay(100); // Pequeña pausa para evitar lecturas inestables
}

// -------------------------------------------------------------------
// 3. 🛠️ FUNCIONES DE SENSORES
// -------------------------------------------------------------------

/**
 * Mide la distancia en centímetros usando el sensor ultrasónico HC-SR04.
 */
int leerDistanciaCM() {
  // Limpiar el Trigger
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Enviar pulso de 10us para medir
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Medir el tiempo que tarda el eco en regresar
  duracion = pulseIn(echoPin, HIGH);
  
  // Convertir a distancia (cm)
  // Velocidad del sonido (343 m/s) -> 0.0343 cm/µs
  // Distancia = (Duración * 0.0343) / 2
  return duracion * 0.0344 / 2; 
}

/**
 * Función de ejemplo para leer el sensor de color.
 * (La lógica de lectura real es más compleja, esta es una base)
 */
long leerColor() {
  // Seleccionar el filtro de color (ejemplo: Rojo)
  digitalWrite(s2, LOW);
  digitalWrite(s3, LOW);
  
  // Leer la frecuencia de salida (proporcional a la intensidad del rojo)
  // El valor real a usar para la clasificación es 'pulseIn' o 'frequency'.
  long frecuencia = pulseIn(outPin, LOW); 
  return frecuencia; 
}


// -------------------------------------------------------------------
// 4. 🚀 FUNCIONES DE MOVIMIENTO
// -------------------------------------------------------------------

/**
 * Mueve ambos motores hacia adelante aplicando el OFFSET individual.
 */
void moverAdelante(int velocidad) {
  // Aplicar OFFSET y limitar a 255
  int velocidad_A = min(velocidad + OFFSET_MOTOR_A, 255);
  int velocidad_B = min(velocidad + OFFSET_MOTOR_B, 255);
  
  // Motor A: Adelante
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);  
  analogWrite(enA, velocidad_A); 

  // Motor B: Adelante
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, velocidad_B); 
}

/**
 * Detiene los motores activando un frenado activo (freno electromagnético).
 * ¡Frena de golpe!
 */
void frenarMotores() {
  analogWrite(enA, 0); 
  analogWrite(enB, 0); 
  
  // FRENADO ACTIVO: Cortocircuito (HIGH, HIGH)
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, HIGH); 
  
  digitalWrite(in3, HIGH);
  digitalWrite(in4, HIGH); 
}

/**
 * Gira a la derecha (Motor A Adelante, Motor B Atrás).
 */
void girarDerecha(int velocidad) {
  int velocidad_A = min(velocidad + OFFSET_MOTOR_A, 255);
  int velocidad_B = min(velocidad + OFFSET_MOTOR_B, 255);
  
  // Motor A (Izquierdo): Adelante
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);  
  analogWrite(enA, velocidad_A); 

  // Motor B (Derecho): Atrás
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB, velocidad_B); 
}

/**
 * Gira a la izquierda (Motor A Atrás, Motor B Adelante).
 */
void girarIzquierda(int velocidad) {
  int velocidad_A = min(velocidad + OFFSET_MOTOR_A, 255);
  int velocidad_B = min(velocidad + OFFSET_MOTOR_B, 255);

  // Motor A (Izquierdo): Atrás
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH);  
  analogWrite(enA, velocidad_A); 

  // Motor B (Derecho): Adelante
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, velocidad_B); 
}