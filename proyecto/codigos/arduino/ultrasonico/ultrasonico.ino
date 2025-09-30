// ---------------------------
// Conexiones L298N
// ---------------------------
#define ENA 5   // Velocidad motor izquierdo (PWM)
#define IN1 8   // Dirección motor izquierdo
#define IN2 9
#define ENB 6   // Velocidad motor derecho (PWM)
#define IN3 10  // Dirección motor derecho
#define IN4 11

// ---------------------------
// Conexiones Ultrasonido
// ---------------------------
#define TRIG 2
#define ECHO 3

// ---------------------------
// Conexiones TCS230
// ---------------------------
#define S0 4
#define S1 7
#define S2 A0
#define S3 A1
#define OUT 12

long duracion;
int distancia;

void setup() {
  Serial.begin(9600);

  // Motores
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Sensor ultrasonico
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  // Sensor de color
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
// Funciones de motores
// ---------------------------
void adelante() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

void parar() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}

void girarDerecha() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, 150);
  analogWrite(ENB, 150);
}

// ---------------------------
// Sensor ultrasonico
// ---------------------------
int medirDistancia() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  duracion = pulseIn(ECHO, HIGH);
  distancia = duracion * 0.034 / 2;
  return distancia;
}

// ---------------------------
// Sensor de color
// ---------------------------
int leerColor(int s2, int s3) {
  digitalWrite(S2, s2);
  digitalWrite(S3, s3);
  return pulseIn(OUT, LOW);
}

void detectarBasura() {
  int rojo = leerColor(LOW, LOW);
  int azul = leerColor(LOW, HIGH);
  int verde = leerColor(HIGH, HIGH);

  Serial.print("Rojo: "); Serial.print(rojo);
  Serial.print("  Verde: "); Serial.print(verde);
  Serial.print("  Azul: "); Serial.println(azul);

  // Clasificación simple (ejemplo, luego se calibra)
  if (rojo < azul && rojo < verde) {
    Serial.println("Detectado: Papel/Blanco");
  } else if (azul < rojo && azul < verde) {
    Serial.println("Detectado: Plastico (colores)");
  } else {
    Serial.println("Detectado: Organico");
  }
}

void loop() {
  int d = medirDistancia();
  Serial.print("Distancia: ");
  Serial.println(d);

  if (d > 20) {
    adelante();
    detectarBasura(); // Mientras avanza va leyendo el color
    delay(500);
  } else {
    parar();
    delay(300);
    girarDerecha();
    delay(600);
    parar();
  }
}