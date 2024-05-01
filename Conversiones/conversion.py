import cv2


def capture_first_frame(video_path, output_path):
    # Cargamos el video
    video_capture = cv2.VideoCapture(video_path)
    
    # Capturamos el primer frame
    ret, frame = video_capture.read()
    
    # Verificamos si el frame se capturó correctamente
    if not ret:
        print("Error al capturar el primer frame")
        return
    
    # Guardamos el primer frame como una imagen
    cv2.imwrite(output_path, frame)
    
    # Liberamos los recursos
    video_capture.release()
    
    return frame

def click_event(event, x, y, flags, param):
    global points
    global length
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        if len(points) == 2:
            cv2.line(img, points[0], points[1], (255, 0, 0), 2)
            length = ((points[1][0] - points[0][0])**2 + (points[1][1] - points[0][1])**2)**0.5
            print("Longitud del objeto en píxeles:", length)
            points = []
            cv2.destroyAllWindows()

video_path = "vid1.mp4"
output_path = "primer_frame.jpg"

# Capturamos el primer frame
primer_frame = capture_first_frame(video_path, output_path)

img = cv2.imread(output_path)
cv2.namedWindow('Imagen', cv2.WINDOW_NORMAL)
cv2.imshow('Imagen', img)
points = []
cv2.setMouseCallback('Imagen', click_event)
cv2.waitKey(0)

# Calculamos la longitud del objeto en metros
valor = 1.85 / length
with open("Pixeles_A_Metros.txt","w") as archivo:
    archivo.write(str(valor))

