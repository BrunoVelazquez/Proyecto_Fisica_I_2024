import cv2
import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

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
    ruta_archivo = 'Conversiones\Pixeles_A_Metros.txt'
    #with open(ruta_archivo,"r") as archivo:
    #    contenido = archivo.read()
    #    valor = float(contenido)


    cap = cv2.VideoCapture(video_path)
    cantidad_frames = 0
    cuadros = []

    tracked = cv2.TrackerCSRT_create()
    #tracked = cv2.legacy.TrackerMOSSE_create() Mas rapido, lo usamos para pruebas
    success, img = cap.read()

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))    
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    

    cv2.namedWindow('Track',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Track', width, height)
    tracker = cv2.selectROI("Track", img, False)
    tracked.init(img, tracker)

    # Crear una ventana redimensionable
    cv2.namedWindow("Sample", cv2.WINDOW_NORMAL)  

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

    if id == 1:
        valor = 0.00897381812634432
    else:
        if id == 2:
            valor = 0.008110213653567056
        else:
            if id == 3:
                valor = 0.00780340688235733
            else:
                if id == 4:
                    valor = 0.008445287789158155
                else:
                    valor = 0.006923984374912447               

    posiciones_x = np.multiply(posiciones_x,valor) #para tener posiciones en metros


    file_name_datos = f'\datos_video_{id}.txt'

    file_path = f'Datos_Extraidos\{file_name_datos}'

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
  
    velocidad_rueda = (cuadros[1]-cuadros[0])/60
    print("La rueda da una vuelta completa cada: ",velocidad_rueda)
    with open(file_path,"w") as file:
        file.write("Componentes de la posicion: \n")
        for item in posiciones_x:
            file.write(f"{item.round(2)},")  
        file.write("\nComponentes de la velocidad: \n")
        for item in vx:
            file.write(f"{item},")
        file.write("\nComponentes de la aceleracion: \n")
        for item in ax:
            file.write(f"{item},")
        file.write("\nComponentes de la fuerza viscosa: \n")
        for item in viscous_force:
            file.write(f"{item},")
        file.write(f"\nRevoluciones por segundo: {velocidad_rueda} ")

    # Graficos sin suavizar
    fig, axs=plt.subplots(3,2, figsize = (14,10))

    axs[0,0].plot(t,posiciones_x)
    axs[0,0].set_xlabel('tiempo')
    axs[0,0].set_ylabel('$p_{x}$')
    axs[0,0].grid(True)

    axs[0,1].plot(t[1:], vx)
    axs[0,1].set_xlabel('tiempo')
    axs[0,1].set_ylabel('$v_{x}$')
    axs[0,1].grid(True)


    axs[1,0].plot(t[2:],ax)
    axs[1,0].set_xlabel('tiempo')
    axs[1,0].set_ylabel('$a_{x}$')
    axs[1,0].grid(True)

    axs[1,1].plot(t[2:], viscous_force)
    axs[1,1].set_xlabel('tiempo')
    axs[1,1].set_ylabel('fuerza_viscosa')
    axs[1,1].grid(True)


    axs[2,0].plot(vx[1:], viscous_force)
    axs[2,0].set_xlabel('velocidad')
    axs[2,0].set_ylabel('fuerza_viscosa')
    axs[2,0].grid(True)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()    

    # Graficos suavizados
    smoothed_x = gaussian_filter1d(posiciones_x, sigma=2)
    smoothed_vx = gaussian_filter1d(vx, sigma=2)
    smoothed_ax = gaussian_filter1d(ax, sigma=2)
    smoothed_viscous_force = gaussian_filter1d(viscous_force, sigma=2)
    smoothed_vx_viscous_force = gaussian_filter1d(viscous_force, sigma=2)

    fig2, axs2 = plt.subplots(3, 2, figsize=(14, 10))

    axs2[0,0].plot(t, smoothed_x)
    axs2[0,0].set_xlabel('tiempo')
    axs2[0,0].set_ylabel('$p_{x}$')
    axs2[0,0].grid(True)

    axs2[0,1].plot(t[1:], smoothed_vx)
    axs2[0,1].set_xlabel('tiempo')
    axs2[0,1].set_ylabel('$v_{x}$')
    axs2[0,1].grid(True)

    axs2[1,0].plot(t[2:], smoothed_ax)
    axs2[1,0].set_xlabel('tiempo')
    axs2[1,0].set_ylabel('$a_{x}$')
    axs2[1,0].grid(True)

    axs2[1,1].plot(t[2:],smoothed_viscous_force)
    axs2[1,1].set_xlabel('tiempo')
    axs2[1,1].set_ylabel('fuerza_viscosa')
    axs2[1,1].grid(True)

    axs2[2,0].plot(vx[1:], smoothed_vx_viscous_force)
    axs2[2,0].set_xlabel('velocidad')
    axs2[2,0].set_ylabel('fuerza_viscosa')
    axs2[2,0].grid(True)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()

    # Calculo la aceleracion a partir de la suavizacion de vx y tambien a la fuerza viscosa

    ax2 = calculate_aceleration(smoothed_vx,t[1:])    
    viscous_force2 = calculate_viscous_force(ax2,65,14)

    # Grafico la aceleracion y la fuerza viscosa a partir de la suavizacion de vx

    fig3, axs3 = plt.subplots(3, 2, figsize=(14, 10))

    axs3[0,0].plot(t[2:], ax2)
    axs3[0,0].set_xlabel('tiempo')
    axs3[0,0].set_ylabel('$a_{x}$')
    axs3[0,0].grid(True)

    axs3[0,1].plot(t[2:], viscous_force2)
    axs3[0,1].set_xlabel('tiempo')
    axs3[0,1].set_ylabel('fuerza_viscosa')
    axs3[0,1].grid(True)

    axs3[1,0].plot(smoothed_vx[1:], viscous_force2)
    axs3[1,0].set_xlabel('$v_{x}$')
    axs3[1,0].set_ylabel('fuerza_viscosa')
    axs3[1,0].grid(True)

    plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.5)
    plt.show()

videos = ['vid1.mov','vid2.mov','vid3.mov','vid4.mov','vid5.mov']


# Arreglos para almacenar las posiciones x 
posiciones_x = [] 
vx = []
ax = []
viscous_force = []

for i in range(1,6):
    #print(f"Posiciones x : {posiciones_x}")
    posiciones_x = [] 
    vx = []
    ax = []
    viscous_force = []
    ruta_video = videos[i-1]
    print(ruta_video)
    process_video(i,ruta_video,posiciones_x,vx,ax,viscous_force)