import pygame
import numpy as np
from PIL import ImageGrab
import cv2
import time
import statistics
from pynput.mouse import Button, Controller
clock = pygame.time.Clock()
last_time = time.time()
mouse = Controller()
pygame.init()
joysticks = []
keepPlaying = True
grudar_mouse = 1
clickar_mouse = 1
X = 0
Y = 0
incre = 50
R = 1
n1 = 42
n2 = 42
n3 = 255
n4 = 255
min_pontos = 0
def pegar_imagem ():
    #print(grudar_mouse)
    printscreen = np.array(ImageGrab.grab(bbox=((0 + X), (0 + Y), (1920 + X) * R, (1080 + Y) * R)))
    processed_img = cv2.cvtColor(printscreen, cv2.COLOR_BGR2HSV)
    lower = np.array([n1, n3, 0])
    upper = np.array([n2, n4, 255])
    mask = cv2.inRange(processed_img, lower, upper)
    output = cv2.bitwise_and(processed_img, processed_img, mask=mask)
    output2 = cv2.bitwise_not(processed_img, processed_img, mask=mask)
    output_gray = cv2.cvtColor(output, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(output_gray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    pontos_de_contorno = 0
    index_do_maior = 0

    for cc in range(len(contours)):
        contorno = contours[cc]
        if (len(contorno) > pontos_de_contorno):
            pontos_de_contorno = len(contorno)
            index_do_maior = cc

    #print(pontos_de_contorno, index_do_maior)
    pontos_x = []
    pontos_y = []

    if (pontos_de_contorno > 5):
        for x in contours[index_do_maior]:
            for y in x:
                pontos_x.append(y[0])
                pontos_y.append(y[1])

    if (len(pontos_x) > min_pontos):
        try:
            x = int(round(statistics.median(pontos_x), 0))
            y = int(round(statistics.median(pontos_y), 0))
            cv_x = (statistics.stdev(pontos_x) / x)
            cv_y = (statistics.stdev(pontos_y) / y)
        except:
            cv_x = -1
            cv_y = -1
           #print("error")
        if(cv_y < 0.9 and cv_x <0.9):

           #print(x," , ",y)
            printscreen = cv2.circle(printscreen, (x, y), 20, [0, 255, 0], 3)

            if (grudar_mouse % 2 == 0):
               #print(pydirectinput.position())
                #mouse.move(x,y)
                mouse.position = (x+X,y+Y)
                if(clickar_mouse%2 ==0):
                    mouse.click(Button.left,2)

    cv2.drawContours(printscreen, contours, -1, (255, 0, 0), 5)
    printscreen = cv2.resize(printscreen, (940, 520))
    output = cv2.resize(output, (940, 520))
    output2 = cv2.resize(output2, (940, 520))
    s = "(" + str(n1) + " , " + str(n2) + " ) ,(" + str(n3) + " , " + str(n4) + ")"
    output = cv2.putText(output, s, ((0), (40)), cv2.FONT_ITALIC, 1, [255, 255, 255])
    output = cv2.putText(output, str(round(time.time() - last_time, 2)), (0, 580), cv2.FONT_ITALIC, 1, [255, 255, 255])
    return output ,output2 , printscreen

for i in range(0, pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-1].init()
   #print("Detected joystick "),joysticks[-1].get_name(),"'"

while keepPlaying:
   #print(min_pontos)
    clock.tick(120)
    r = pygame.event.get()


    #print('loop took {} seconds'.format(time.time() - last_time))

    output, output2, printscreen = pegar_imagem()


    last_time = time.time()
    if(grudar_mouse%2!=0):
        cv2.imshow("a",cv2.cvtColor(printscreen,cv2.COLOR_BGR2RGB))
        #cv2.imshow('t',cv2.cvtColor(output2,cv2.COLOR_HSV2RGB))
        cv2.imshow('window', cv2.cvtColor(output,cv2.COLOR_HSV2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    if(len(r)>0):#Controle foi usado
        event = r[0]
        print(r)
        string = str(event)
        string = string[string.find('{')+1:string.find('}')]
        c = string.find('button')
        d = string.find('hat')
        joy = string.find('joy')
        if (joy > 0):# O joystick foi ativado
            try:
                val = float(string[string.find('value')+8:])
                n = string.find('axis')
                axis = float(string[n+7:n+8])
                if (val != 0):
                    if(axis ==3):#direita vertical
                        if(val>0):
                            n4 += 1
                        if(val<0):
                            n4 -= 1
                    if (axis == 2):
                        if (val > 0):
                            n2 += 1
                        if (val < 0):
                            n2 -= 1
                    if (axis == 1):  # esquerda vertical
                        if (val > 0):
                            n3 += 1
                        if (val < 0):
                            n3 -= 1
                    if (axis == 0):  # esquerda horizon
                        if (val > 0):
                            n1 += 1
                        if (val < 0):
                            n1 -= 1
            except:
                pass
        if (c >0):#um botao foi apertado
            if(int(string[c+9:]) == 0):
                keepPlaying = False
            if (int(string[c + 9:]) == 1):
                grudar_mouse = 1
                X = 0
                Y = 0
                incre = 50
                R = 1
                n1 = 0
                n2 = 180
                n3 = 0
                n4 = 255
                min_pontos = 0

            if (int(string[c + 9:]) == 2):
                incre +=10
            if (int(string[c + 9:]) == 3):
                incre -=10
            if (int(string[c + 9:]) == 4):
                R += 0.05
            if (int(string[c + 9:]) == 5):
                R -= 0.05
            if (int(string[c + 9:]) == 6):
                min_pontos += 0.5
            if (int(string[c + 9:]) == 7):
                min_pontos -= 0.5
            if (int(string[c + 9:]) == 8):
                grudar_mouse += 0.5
            if (int(string[c + 9:]) == 9):
                clickar_mouse += 0.5



           #print(string[c+9:])
        elif(d >0):#um botao direciojnal foi ativo
            x,y = string[string.find('value')+8:].replace('(','').replace(')','').split(',')
            x = int(x)
            y = int(y)
            X += x*incre
            Y += y*-incre

