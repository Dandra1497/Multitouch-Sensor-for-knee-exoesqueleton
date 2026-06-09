import processing.serial.*;
import java.io.PrintWriter;

int maxValue = 0;                      // Valor máximo leído
ArrayList<Integer> maxValues = new ArrayList<Integer>(); // Almacena valores máximos
ArrayList<Integer> timestamps = new ArrayList<Integer>(); // Almacena tiempos relativos
int graphWidth = 960;                  // Ancho de la gráfica
int graphHeight = 600;                 // Altura de la gráfica

Serial myPort;                         // Puerto serial
int[] serialInArray = new int[225];
int serialCount = 0;                   // Contador de bytes recibidos
boolean firstContact = false;          // Si hay contacto inicial con el microcontrolador
int tiempoInicio;                      // Marca de tiempo inicial

PrintWriter output;                    // Para guardar en CSV

void settings() {
  size(graphWidth, graphHeight); // Tamaño de la ventana
}

void setup() {
  noFill();
  println(Serial.list());
  myPort = new Serial(this, Serial.list()[4], 115200);
  tiempoInicio = millis(); // Guarda el tiempo inicial
  
  // Crear archivo CSV
  output = createWriter("PruebaFuerza2.csv");
  output.println("Tiempo (ms),Valor Maximo"); // Encabezados de las columnas
}

void draw() {
  background(0); // Fondo negro
  stroke(255);   // Color de las líneas (blanco)

  // Dibuja los ejes
  strokeWeight(1);
  line(50, height - 50, width - 50, height - 50); // Eje X
  line(50, height - 50, 50, 50);                 // Eje Y

  // Etiquetas de los ejes
  fill(255);
  textAlign(CENTER);
  text("Tiempo (s)", width / 2, height - 10);
  textAlign(RIGHT);
  text("Valor Máximo", 40, height / 2);

  // Calcula el tiempo total transcurrido
  int totalTime = timestamps.size() > 0 ? timestamps.get(timestamps.size() - 1) / 1000 : 0;

  // Determina el intervalo de las etiquetas del eje X
  float xInterval = totalTime <= 5 ? 1.0 : 2.5; // Paso: 1s para ≤5s, 2.5s para >5s

  // Etiquetas numéricas del eje X
  for (float t = 0; t <= totalTime; t += xInterval) {
    float x = map(t, 0, totalTime, 50, width - 50);
    if (x >= 50 && x <= width - 50) {
      line(x, height - 50, x, height - 45);
      textAlign(CENTER);
      text(nf(t, 0, 1), x, height - 30); // Formato con un decimal
    }
  }

  // Etiquetas numéricas del eje Y
  for (int y = 0; y <= 255; y += 50) {
    float yPos = map(y, 0, 255, height - 50, 50);
    line(50, yPos, 55, yPos);
    textAlign(RIGHT);
    text(y, 45, yPos + 5);
  }

  // Dibuja la gráfica si hay datos
  if (maxValues.size() > 1) {
    noFill();
    stroke(255, 0, 0); // Color rojo para la gráfica
    strokeWeight(2);
    beginShape();
    for (int i = 0; i < maxValues.size(); i++) {
      float x = map(timestamps.get(i) / 1000.0, 0, totalTime, 50, width - 50);
      float y = map(maxValues.get(i), 0, 255, height - 50, 50);
      vertex(x, y);
    }
    endShape();
  }
}

void serialEvent(Serial myPort) {
  int inByte = myPort.read();
  if (!firstContact) {
    if (inByte == 'A') {
      myPort.clear();
      firstContact = true;
      myPort.write('A');
    }
  } else {
    serialInArray[serialCount] = inByte;
    serialCount++;

    if (serialCount > 224) {
      maxValue = 0;

      // Encuentra el valor máximo
      for (int i = 0; i < 225; i++) {
        if (serialInArray[i] > maxValue) {
          maxValue = serialInArray[i];
        }
      }

      // Agrega valor máximo y el tiempo relativo
      int currentTime = millis() - tiempoInicio;
      maxValues.add(maxValue);
      timestamps.add(currentTime);

      // Escribe los datos en el archivo CSV, asegurando separación por columnas
      output.println(currentTime + "," + maxValue);

      println("Tiempo: " + currentTime + " ms, Máximo: " + maxValue);

      myPort.write('A'); // Solicita nuevos datos
      serialCount = 0;
    }
  }
}

void keyPressed() {
  if (key == 's' || key == 'S') {
    String timestamp = nf(year(), 4) + nf(month(), 2) + nf(day(), 2) + "_" + nf(hour(), 2) + nf(minute(), 2) + nf(second(), 2);
    saveFrame("grafica_" + timestamp + ".png");
    println("Imagen guardada: grafica_" + timestamp + ".png");
  }
}

// Cierra el archivo CSV al salir
void exit() {
  output.flush();  // Asegura que se escriban todos los datos
  output.close();  // Cierra el archivo
  super.exit();
}
