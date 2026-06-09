#include <Wire.h>
#include <HX711.h>

// Definición de los HX711
HX711 balanza1;//primer HX711
HX711 balanza2; // Segundo HX711
HX711 balanza3; // Tercer HX711
HX711 balanza4; // cuarto HX711

// Pines para los HX711
// Pines para el primer HX711
const int DT1 = 2; // mcu > HX711 dout pin
const int CLK1 = 3; // mcu > HX711 sck pin

// Pines para el segundo HX711
const int DT2 = 4;
const int CLK2 = 5;
// 3 HX711
const int DT3 = 10;
const int CLK3 = 11;
// 4 HX711  
const int DT4= 12;
const int CLK4= 13;


// Pines de salida
int SIG = 9;

// Variables para almacenar datos de las celdas de carga
float peso1, celda1;
float peso2, celda2;
float peso3, celda3;
float peso4, celda4;

// Variables para la comunicación serial
String dataString = "";
bool dataComplete = false;
int data = 0;

void setup() {
  // Configuración de pines
  pinMode(SIG, OUTPUT);
  Serial.begin(9600);

  // Inicialización de los HX711
  balanza1.begin(DT1, CLK1);
  balanza2.begin(DT2, CLK2);
  balanza3.begin(DT3, CLK3);
  balanza4.begin(DT4, CLK4);

  // Calibración inicial
  //balanza1.set_scale();
  //balanza1.tare();
  //balanza2.set_scale();
  //balanza2.tare();
  //balanza3.set_scale();
  //balanza3.tare();
  //balanza4.set_scale();
  //balanza4.tare();

  // Mensaje inicial
  Serial.println("Iniciando lectura de las celdas de carga...");
}

void loop() {
  // Verificar si hay datos completos para procesar
  if (dataComplete) {
    data = dataString.toInt();
    task();
    dataString = "";
    dataComplete = false;
  }

  // Lectura de las celdas de carga
  peso1 = balanza1.get_units(2); // Lee 10 muestras y calcula el promedio
  celda1 = ( 0.0044*peso1 + 25.928) * 9.81 / 1000; // Conversión a Newtons
  
  peso2 = balanza2.get_units(2);
  celda2 = (0.0046 * peso2 + 5.6792) * 9.81 / 1000;

  peso3 = balanza3.get_units(2);
  celda3 = (0.0046 * peso3 + 3.4384) * 9.81 / 1000;
  
  peso4 = balanza4.get_units(2);
  celda4 = (0.0043* peso4 +21.293) * 9.81 / 1000;

  // Mostrar los datos de las celdas en el Serial Monitor
  //Serial.print("CELDA 1: ");
  Serial.print(celda1);
  Serial.print(",");          
  Serial.print(celda2);
  Serial.print(",");
  Serial.print(celda3);
  Serial.print(",");
  Serial.println(celda4);
}

void serialEvent() {
  // Leer datos del puerto serial
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    dataString += inChar;
    if (inChar == '\n') {
      dataComplete = true;
    }
  }
}

void task() {
  // Control de los pines según el dato recibido
  if (data == 30) {
    digitalWrite(SIG, HIGH);
  } else {
    digitalWrite(SIG, LOW);
  }
}