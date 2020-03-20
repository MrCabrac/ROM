import cv2
import os
import utilities

cap = cv2.VideoCapture(0)
frameCount = 0 #contar el numero de frames

frames = utilities.Config.frames()

while True:
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
                cv2.imwrite('frame/img.jpg', img) #guardar la imagende interes
    
    cv2.imshow('frame', frame)
    #cv2.imshow('gray', gray)
    #cv2.imshow('thresh_img', thresh_img)
    #cv2.imshow('interes', frame2)
    
    frameCount+=1 #aumentar el contador de frames

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()