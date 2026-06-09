# EL SIGUIENTE CODIGO TIENE EL PROPOSITO DE MOSTRAR DATOS GRAFICADOS APARTIR
# DE LAS LECTURAS DE LOS SENSORES DE TENSIÓN GSL311 Y EL CONTROL DEL DROP PARA
# EL INICIO DE LAS PRUEBAS

# MATERIA: ESTANCIA DE INVESTIGACION: PARA LA CREACION DE UN PROTOTIPO DE RODILLA.
# PROFESORES: DR. ALEJANDRO ACEVES LOPEZ, DR. MIGUEL ÁNGEL GÁLVEZ ZÚÑIGA
# DESARROLLADOR: DYLAN ANDRADE PEREZ A01753855 
# ALUMNOS: KATIA GASCA ALCANTARA AO1747365
#          MAURA ODOÑEZ VEGA A01748016
#          RUTH ABIGAIL DE LA REÑA ROSALES A01662431
#          DIEGO EMILIANO TAPIA CADENA A01754796
#          DYLAN ANDRADE PEREZ A01753855

# INSTITUTO DE ESTUDIOS SUPERIORES TECNOLOGICO DE MONTERREY

#IMPORTACIONES DE LAS LIBRERIAS NECESARIAS PARA LA INTERFAZ
from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from Interfaz import Comunicacion
from openpyxl import Workbook
import collections
import time
import os

#DECLARACION DE LA CLASE EN LA CUAL SE COLOCARAN LOS FRAMES PARA LA INTERFAZ
class Grafica(Frame):
    def __init__(self, master, *args):
        super().__init__(master, *args)
        self.datos_arduino = Comunicacion()
        self.actualizar_puertos()
        
        self.muestra = 200
        self.datos = 0.0
        self.start_time = time.time()
        
        self.excel_file='LecturasGSLpruebaEsfera_3bueno_271124.xlsx'
        self.workbook = Workbook()
        self.sheet=self.workbook.active
        self.sheet.title = "Lecturas"
        
        self.sheet.append(["Tiempo(s)", "Dato1","Dato2","Dato3","Dato4"])
        
        
        # EN ESTA SECCION DEL CODIGO SE CREAN LOS ASPECTOS NECSESARIOS PARA PODER HACER UNA GRAFICA
        # - EL FRAME DE VISUALIZACION
        # - ATRIBUTOS DE LAS LINEAS 
        # - ATRIBUTOS DE LA GRAFICA
        
        self.fig, ax = plt.subplots(facecolor='#FFFFFF', dpi = 100, figsize=(4,2))
        plt.title("Graficar Datos Arduino", color='black', size = 12, family="Arial")
        #ax.tick_params(direction='out', length=5,  width=2,
         #              colors='white', 
         #              grid_color='r', grid_alpha=0.5)
        
        # DECLARACIONES DE LAS LINEAS PARA LA GRAFICA1
        self.line, = ax.plot([], [], color='m', marker='_', 
                            linewidth = 2)
        
        self.line2, = ax.plot([], [], color='g', marker='_', 
                              linewidth=2) 
        
        self.line3, = ax.plot([], [], '-',color='b', 
                              linewidth = 2)
        
        self.line4, = ax.plot([], [], color='k', marker = '_', 
                              linewidth = 2)
        
        plt.xlim([0,2])
        plt.ylim([-5,15])#limites Dylan (-5,6)
        
        ax.set_facecolor('#6E6D7000')
        ax.spines['bottom'].set_color('black')
        ax.spines['left'].set_color('black')
        ax.spines['top'].set_color('black')
        ax.spines['right'].set_color('black')

        self.tiempo = collections.deque([0]*self.muestra, maxlen = self.muestra)
        self.datos_senal_uno = collections.deque([0]*self.muestra, maxlen=self.muestra)
        self.datos_senal_dos = collections.deque([0]*self.muestra, maxlen=self.muestra)
        self.datos_senal_tres = collections.deque([0]*self.muestra, maxlen=self.muestra)
        self.datos_senal_cuatro = collections.deque([0]*self.muestra, maxlen=self.muestra)
        
        self.image_count = 3
        self.widgets()
        
    def animate(self,i):
        
        #SECCION DONDE SE GUARDAN LOS DATOS LEIDOS POR LOS SENSORES GSL311 DESDE EL ARDUINO
        self.datos =  (self.datos_arduino.datos_recibidos.get())
        current_time = time.time() - self.start_time
        
        try: 
            dato = self.datos.split(",")
            dato1 = float(dato[0]) 
            dato2 = float(dato[1])
            dato3 = float(dato[2])
            dato4 = float(dato[3])
            
            self.tiempo.append(current_time)
            self.datos_senal_uno.append(dato1)
            self.datos_senal_dos.append(dato2)
            self.datos_senal_tres.append(dato3)
            self.datos_senal_cuatro.append(dato4)
            
            self.line.set_data(self.tiempo, self.datos_senal_uno)
            self.line2.set_data(self.tiempo, self.datos_senal_dos)
            self.line3.set_data(self.tiempo, self.datos_senal_tres)
            self.line4.set_data(self.tiempo, self.datos_senal_cuatro)
            
            plt.xlim([0, max(self.tiempo)])
            
            self.sheet.append([current_time,dato1,dato2,dato3,dato4])
            self.workbook.save(self.excel_file)
            
        except ValueError:
            print("ERROR: DATO NO NUMERICO RECIBIDO", self.datos)
            
            
    def iniciar(self,):
        dato = '0'
        self.datos_arduino.enviar_datos(dato)
        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=100,  blit=False)
        
        self.bt_graficar.config(state = 'disabled')
        self.bt_pausar.config(state = 'normal')
        self.canvas.draw()
        
    def pausar(self):
        
        self.workbook.save(self.excel_file)
        print(f"Datos guardados en {self.excel_file}")
        
        output_directory = "graficas"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            
        filename = os.path.join(output_directory, f"grafica_{self.image_count}.png")
        self.fig.savefig(filename)
        print(f"Imagen salvada como {filename}")
        
        self.image_count += 1
        self.ani.event_source.stop()
        self.bt_pausar.config(state='disabled')
        self.bt_reanudar.config(state='normal')
        
    def reanudar(self):
        self.ani.event_source.start()
        self.bt_reanudar.config(state='disabled')
        self.bt_pausar.config(state='normal')
        
    def widgets(self):
        frame = Frame(self.master, bg='gray50', bd=2)
        frame.grid(column=0, columnspan=2,row=0, sticky='snew')
        frame1=Frame(self.master, bg='black')
        frame1.grid(column=2, row=0, sticky='nsew')
        frame4 = Frame(self.master, bg='black')
        frame4.grid(column=0, row=1, sticky='nsew')
        frame2 = Frame(self.master, bg='black')
        frame2.grid(column=1, row=1, sticky='nsew')
        frame3 = Frame(self.master, bg='black')
        frame3.grid(column=2, row=1, sticky='nsew')
        
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
        self.master.columnconfigure(2, weight=1)
        self.master.rowconfigure(0, weight=5)
        self.master.rowconfigure(0, weight=1)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(padx=0, pady=0, expand=True, fill='both')
        
        self.bt_graficar = Button(frame4, 
                                  text='CALIBRAR/GRAFICA', 
                                  font=('Arial', 12, 'bold'),
                                  width=20,bg='purple4', 
                                  fg='white', 
                                  command=self.iniciar)
        
        self.bt_graficar.pack(padx = 5,
                              pady = 10, 
                              expand=1, 
                              side='left')
        
        self.bt_pausar = Button(frame4, 
                                state = 'disabled', 
                                text='GUARDAR DATOS/PAUSA', 
                                font=('Arial', 12, 'bold'),
                                width = 20, 
                                bg = 'salmon', 
                                fg = 'white', 
                                command = self.pausar)
        
        self.bt_pausar.pack(padx = 5, 
                            pady = 10, 
                            expand = 1, 
                            side='left')
        
        self.bt_reanudar = Button(frame4, 
                                  state = 'disabled', 
                                  text = 'Reanudar', 
                                  font = ('Arial', 12, 'bold'),
                                  width = 20, 
                                  bg = 'green', 
                                  fg = 'white', 
                                  command = self.reanudar)
        
        self.bt_reanudar.pack(padx = 5, 
                              pady = 10,
                              expand = 1, 
                              side='left')
        
        
        port = self.datos_arduino.puertos
        baud = self.datos_arduino.baudrates
        
        Label(frame1, text ='Puertos COM', bg = 'black', fg = 'white', font = ('Arial', 12, 'bold')).pack(padx = 5, expand = 1)
        self.combobox_port = ttk.Combobox(frame1, values = port, justify='center', width = 12, font='Arial')
        self.combobox_port.pack(pady = 0, expand = 1)
        self.combobox_port.current(0)
        
        Label(frame1, text ='Baudrates', bg = 'black', fg = 'white', font = ('Arial', 12, 'bold')).pack(pady = 0, expand = 1)
        self.combobox_baud = ttk.Combobox(frame1, values = baud, justify='center', width = 12, font='Arial')
        self.combobox_baud.pack(padx = 20, expand = 1)
        self.combobox_baud.current(3)
        
        self.bt_conectar = Button(frame1, text='Conectar', font=('Arial', 12, 'bold'), width = 12, bg = 'green2', command = self.conectar_serial)
        self.bt_conectar.pack(pady = 5, expand=1)
        
        self.bt_actualizar = Button(frame1, text='Actualizar', font=('Arial', 12, 'bold'), width = 12, bg = 'magenta', command = self.actualizar_puertos)
        self.bt_actualizar.pack(pady = 5, expand=1)
        
        self.bt_desconectar = Button(frame1, state = 'disabled', text='Desconectar', font=('Arial', 12, 'bold'), width = 12, bg = 'red2', command = self.desconectar_serial)
        self.bt_desconectar.pack(pady = 5, expand=1)
        
        Label(frame1, text = "DROP SETUP", bg = 'black', fg = 'white', font = ('Arial', 12, 'bold')).pack(padx = 5, expand = 1)
        
        self.bt_hold = Button(frame1, text='Hold', font = ('Arial', 12, 'bold'), width = 12, bg  = 'red2', command = self.hold_electro)
        self.bt_hold.pack(pady = 5, expand=1)
        
        self.bt_drop = Button(frame1, text='DROP', font = ('Arial', 12, 'bold'), width = 12, bg = 'blue', command = self.drop_electro)
        self.bt_drop.pack(pady = 5, expand=1)
        
       # Label(frame3, image = self.logo, bg = 'black').pack(pady = 5, expand = 1)
        
    def actualizar_puertos(self):
        self.datos_arduino.puertos_disponibles()
        
    def conectar_serial(self):
        self.bt_conectar.config(state='disabled')
        self.bt_desconectar.config(state='normal')
        #self.slider_uno.config(state='normal')
        #self.slider_dos.config(state='normal')
        self.bt_graficar.config(state='normal')
        self.bt_reanudar.config(state='disabled')
        
        self.datos_arduino.arduino.port = self.combobox_port.get()
        self.datos_arduino.arduino.baudrate = self.combobox_baud.get()
        self.datos_arduino.conexion_serial()
        
    def desconectar_serial(self):
        self.bt_conectar.config(state = 'normal')
        self.bt_desconectar.config(state = 'disabled')
        self.bt_pausar.config(state = 'disabled')
        #self.slider_uno.config(state = 'disabled')
        #self.slider_dos.config(state = 'disabled')
        try:
            self.ani.event_source.stop()
        except AttributeError:
            pass
        self.datos_arduino.desconectar()
        
    def hold_electro(self, *args):
        dato = '30'
        self.datos_arduino.enviar_datos(dato)
        
    def drop_electro(self, *args):
        dato = '0'
        self.datos_arduino.enviar_datos(dato)
            
            
if __name__ =="__main__":
    ventana = Tk()
    ventana.geometry('742x535')
    ventana.config(bg='gray30', bd = 4)
    ventana.wm_title('Grafica')
    ventana.minsize(width=700, height=400)
    #ventana.call('wm', 'iconphoto', ventana._w, PhotoImage(file='gtr.jpg'))
    app = Grafica(ventana)
    app.mainloop()
