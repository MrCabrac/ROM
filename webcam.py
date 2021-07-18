import cv2
import os
import utilities
import modelo
import sys
try:
    clf_filename = sys.argv[1]
except IndexError as error:
    clf_filename = ""

# Help
if(clf_filename == ""):
    print('You must be specify the model path, like: modelo/modeloEntrenado.pkl')

# clf_filename = "modelo/modeloEntrenado2.pkl" #Ubicacion del modelo entrenado

modelClass = modelo.Modelo()

cap = cv2.VideoCapture(1)
frameCount = 0 #contar el numero de frames

frames = utilities.Config.frames()

while True and clf_filename!="":
    ret, frame = cap.read() #captura frame by frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #pasar el frame a escala de grises
    ret, thresh_img = cv2.threshold(gray, 91, 255, cv2.THRESH_BINARY_INV) #binarizar el frame
    [fil, col] = gray.shape ##obtener las dimensiones del frame

    ymargin = 150 ##un margen en y para el recuadro de enfoque
    xmargin = 80 ##un margen en x para el recuadro de enfoque
    
    frame2 = frame[ymargin:fil-ymargin, xmargin:col-xmargin] ##recorta el area interesante
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY) ##convierte el area interesante en escala de grises
    cv2.rectangle(frame, (xmargin, ymargin), (col-xmargin, fil-ymargin), (0, 255, 0), 4) ##dibuja el area interesante en frame

    print("LOG:DEBUG -- fil:{} - col:{}".format(fil, col))

    if frameCount%frames == 0: #si se alcanzan 30 frames
        print("LOG:DEBUG -- {} frames alcanzados".format(frames))
        if ret:
            img = cv2.resize(frame2, (1240, 1024)) #redimensionar la parte de interes
            
            if not os.path.isdir('frame'): #verificar si 'frame' existe
                os.mkdir('frame')
            else:
                try:
                    cv2.imwrite('frame/img.jpg', img) #guardar la imagen de interes
                    response = modelClass.predecir(clf_filename, "frame/img.jpg")
                    respuesta = "{} = {}".format(response[0], eval(response[0]))
                except Exception as error:
                    respuesta = "{} = 0".format(response[0])
                    utilities.Log.e(error)
                utilities.Log.i(respuesta)
    
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (0,25)
    fontScale              = 1
    fontColor              = (0, 0, 255)
    lineType               = 2

    cv2.putText(frame, respuesta, bottomLeftCornerOfText, font, fontScale, fontColor, 2)
    cv2.putText(frame, 'Frames:'+str(frameCount), (0, 0-5), font, fontScale, fontColor, lineType)

    
    cv2.imshow('frame', frame)
    #cv2.imshow('gray', gray)
    cv2.imshow('thresh_img', thresh_img)
    cv2.imshow('interes', frame2)
    
    frameCount+=1 #aumentar el contador de frames

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if clf_filename!="":
    cap.release()
    cv2.destroyAllWindows()