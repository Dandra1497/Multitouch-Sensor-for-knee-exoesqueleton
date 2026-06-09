import serial
import time
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

# Configuración inicial
plt.style.use('ggplot')
serialArduino = serial.Serial("COM13", 9600)
time.sleep(1)

# Listas para almacenar los datos de tiempo y valores
x_data = []
HX1_data = []
HX2_data = []
HX3_data = []
HX4_data = []
y_data = []

# Configuración de la figura
figure = pyplot.figure()
line, = pyplot.plot_date(x_data, HX1_data, '-')
line2, = pyplot.plot_date(x_data, HX2_data, '-')
line3, = pyplot.plot_date(x_data, HX3_data, '-')
#line4, = pyplot.plot_date(x_data, HX4_data, '-')

start_time = time.time()

# Función de actualización de la gráfica
def grafica3(frame):
    cad = serialArduino.readline().decode('ascii').strip()  # Decodifica y elimina \r\n
    try:
        # Convierte el dato a un número (int o float)
        sensor_values = cad.split(',')
        sensor1 = float(sensor_values[0])
        sensor2 = float(sensor_values[1])
        #sensor3 = float(sensor_values[2])
        #sensor4 = float(sensor_values[3])
        
        current_time = time.time()-start_time
        # Almacena la marca de tiempo y el valor
        x_data.append(current_time)
        HX1_data.append(sensor1)
        HX2_data.append(sensor2)
        #HX3_data.append(sensor3)
        #HX4_data.append(sensor4)
        
        # Actualiza los datos de la gráfica
        line.set_data(x_data, HX1_data)
        line2.set_data(x_data, HX2_data)
        #line3.set_data(x_data, HX3_data)
        #line4.set_data(x_data, HX4_data)
        
        # Ajusta los límites de la gráfica automáticamente
        figure.gca().relim()
        figure.gca().autoscale_view()
    except ValueError:
        print("Error: Dato no numérico recibido", cad)
    return line, line2,

# Crea la animación de la gráfica en tiempo real
animacion3 = FuncAnimation(     figure, grafica3, interval=30, frames=40)
pyplot.show()
