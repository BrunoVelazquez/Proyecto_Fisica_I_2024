import cv2
import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
import json

DIR = ''
FILE1 = 'vid1.mov'
FILE2 = 'vid2.mov'
FILE3 = 'vid3.mov'
FILE4 = 'vid4.mov'
FILE5 = 'vid5.mov'

def startTrack(img, tracker):
    x, y, w, h = int(tracker[0]), int(tracker[1]), int(tracker[2]), int(tracker[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 0, 255), 3, 1)
    cv2.putText(img, "Tracking", (75, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 3)
    global posicion_x_actual
    posicion_x_actual = x
    # Agregar las posiciones x al arreglo
    posiciones_x.append(x)

def calculate_aceleration(vx, t_values):
    ax = np.diff(vx) / np.diff(t_values) # La función diff() de numpy calcula la diferencia entre dos puntos sucesivos.

    return ax.round(2)

def calculate_velocity(x_values, t_values):
    dx_dt = np.diff(x_values) / np.diff(t_values)
   
    return dx_dt.round(2) 

def calculate_viscous_force(ax,person_mass, bike_mass):
    total_mass = person_mass + bike_mass
    
    return np.multiply(ax,total_mass).round(2)

def write_data_to_file(file_path, data):
    with open(file_path,"w") as file:
        for item in data:
            file.write(f"{item},")    

def process_video(id, video_path,posiciones_x, vx, ax, viscous_force):
    # Extraigo del archivo los datos de conversion
    ruta_archivo = 'Conversiones\Pixeles_A_Metros.json'
    with open(ruta_archivo,"r") as archivo:
        datos = json.load(archivo)
        valor = float(datos[id-1]["valor"])


    cap = cv2.VideoCapture(video_path)
    cantidad_frames = 0
    cuadros = []

    tracked = cv2.TrackerCSRT_create()
    #tracked = cv2.legacy.TrackerMOSSE_create() #Mas rapido, lo usamos para pruebas
    success, img = cap.read()

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    

    cv2.namedWindow('Track',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Track', width, height)
    tracker = cv2.selectROI("Track", img, False)
    tracked.init(img, tracker)

    # Crear una ventana redimensionable
    cv2.namedWindow("Sample", cv2.WINDOW_NORMAL)  
    cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    
    while True:
        cantidad_frames = cantidad_frames + 1
        success, img = cap.read()

        if img is None:
            break
    
        success, tracker = tracked.update(img) 

        if success:
            startTrack(img, tracker)
        else:
            cv2.putText(img, "Lost Object", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

        cv2.imshow("Sample", img)
        key = cv2.waitKey(25)
        if key == 27:
            break
        if key == ord('s'):
            cuadros.append(cantidad_frames)

    cap.release()
    cv2.destroyAllWindows() 

    posiciones_x = np.multiply(posiciones_x,valor) #para tener posiciones en metros




    dir_base = f'Datos_Extraidos_Bici\Datos_Video_{i}'


    # Para calcular el tiempo_final(duracion del video) al saber que el celular graba a 30 FPS divido
    # la cantidad total de frames por 30 y obtengo la duracion en segundos
    tiempo_final = cantidad_frames / 30
    t = np.linspace(0,tiempo_final,len(posiciones_x))

    print(t)
    print()
    print(f"El tiempo final es {tiempo_final}")
    #Calculo las componentes x del vector velocidad y del vector aceleracion
    vx = calculate_velocity(list(posiciones_x),t)
    ax = calculate_aceleration(vx, t[1:])

    #Calculo la fuerza viscosa
    viscous_force = calculate_viscous_force(ax,65,14)

    # Graficos suavizados
    with open(ruta_archivo,"r") as archivo:
        datos = json.load(archivo)
        ventana = int(datos[id-1]["ventana"])

    x1 = savgol_filter(posiciones_x, ventana, 5)
    #x2 = savgol_filter(x1, 50, 4)
    vx3 = calculate_velocity(x1,t)
    #vx4= savgol_filter(vx3,50,5)
    vx5= savgol_filter(vx3,ventana,5)
    ax3= calculate_aceleration(vx5,t[1:])
    ax4= savgol_filter(ax3,ventana,5)
    viscous_force2 = calculate_viscous_force(ax4,65,14)
    

    fig2, axs2 = plt.subplots(3, 2, figsize=(14, 10))
    

    axs2[0,0].plot(t, x1)
    axs2[0,0].set_xlabel('tiempo')
    axs2[0,0].set_ylabel('$p_{x}$')
    axs2[0,0].grid(True)

    axs2[0,1].plot(t[1:], vx5)
    axs2[0,1].set_xlabel('tiempo')
    axs2[0,1].set_ylabel('$v_{x}$')
    axs2[0,1].grid(True)

    axs2[1,0].plot(t[2:], ax4)
    axs2[1,0].set_xlabel('tiempo')
    axs2[1,0].set_ylabel('$a_{x}$')
    axs2[1,0].grid(True)

    axs2[1,1].plot(t[2:],viscous_force2)
    axs2[1,1].set_xlabel('tiempo')
    axs2[1,1].set_ylabel('fuerza_viscosa')
    axs2[1,1].grid(True)

    axs2[2,0].plot(vx5[1:], viscous_force2)
    axs2[2,0].set_xlabel('velocidad')
    axs2[2,0].set_ylabel('fuerza_viscosa')
    axs2[2,0].grid(True)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()

     # Rutas de los archivos
    file_path_posiciones = f'{dir_base}\\posicion_{i}.txt'
    file_path_velocidad = f'{dir_base}\\velocidad_{i}.txt'
    file_path_aceleracion = f'{dir_base}\\aceleracion_{i}.txt'
    file_path_fuerza_viscosa = f'{dir_base}\\fuerza_viscosa_{i}.txt'
    file_path_tiempo = f'{dir_base}\\tiempo_{i}.txt'

    # Escribir en los archivos
    with open(file_path_posiciones, "w") as file:
        for item in x1:
            file.write(f"{item.round(2)},")
    with open(file_path_velocidad, "w") as file:
        for item in vx5:
            file.write(f"{item},")
    with open(file_path_aceleracion, "w") as file:
        for item in ax4:
            file.write(f"{item},")
    with open(file_path_tiempo, "w") as file:
        for item in t:
            file.write(f"{item},")        
    with open(file_path_fuerza_viscosa, "w") as file:
        for item in viscous_force2:
            file.write(f"{item},")


videos = [DIR + FILE1, DIR + FILE2, DIR + FILE3, DIR + FILE4, DIR + FILE5]


# Arreglos para almacenar las posiciones x 
posiciones_x = [] 
vx = []
ax = []
viscous_force = []

for i in range(1,6):
    posiciones_x = [] 
    vx = []
    ax = []
    viscous_force = []
    ruta_video = videos[i-1]
    print(ruta_video)
    process_video(i,ruta_video,posiciones_x,vx,ax,viscous_force)    process_video(i,videos[i-1],posiciones_x,vx,ax,viscous_force)