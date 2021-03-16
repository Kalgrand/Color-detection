# -*- coding: utf-8 -*-
"""
@author: micha
"""

import cv2
import numpy as np
import pandas as pd
import argparse

# argument parser
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help= "path to the image")
args = vars(ap.parse_args())
img_path = args['image']

# wczytanie obrazu
img = cv2.imread("../../Desktop/zad/pic.jpg")
img2 = cv2.imread("../../Desktop/zad/pic2.jpg")

# zmienne globalne
clicked = False
r = g = b = xpos = ypos = 0

# czytanie pliku csv i nadawanie nazw każdej kolumnie
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv("../../Desktop/zad/colours.csv", names=index, header=None)

# łączenie obraz w poziomie
Hori = np.concatenate((img, img2), axis=1) 

# funkcja obliczania minimalnej odległości od wszystkich kolorów i uzyskania najbardziej pasującego koloru
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

# funkcja do uzyskania współrzędnych x, y z dwukrotnego kliknięcia myszy
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = Hori[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)
  
while(1):

    cv2.imshow("image", Hori)
    if (clicked):
   
        # cv2.rectangle(obraz, punkt początkowy, punkt końcowy, kolor, grubość)
        cv2.rectangle(Hori,(20,20), (750,60), (b,g,r), -1)
        
        # Tworzenie ciągu tekstowego do wyświetlenia (nazwa koloru i wartości RGB)
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        
        # cv2.putText(img, tekst, początek, czcionka(0-7), fontScale, kolor, grubość, typ linii)
        cv2.putText(Hori, text,(50,50),7,0.8,(255,255,255),2,cv2.LINE_AA)
        
        # w przypadku bardzo jasnych kolorów wyświetlenie w kolorze czarnym
        if(r+g+b>=600):
            cv2.putText(Hori, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    # przerwanie pętli
    if cv2.waitKey(20) & 0xFF ==27:
        break
   
cv2.destroyAllWindows()