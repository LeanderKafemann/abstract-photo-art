from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import *
from random import randint, choice
from time import sleep
import pygame
import pygame.camera

def getallpixels():
    global bild
    pixellist = []
    pixellistcolors = []
    allpixels = bild.width()*bild.height()
    durchlauf = 0
    prozent = 0
    for x in range(bild.width()):
        for y in range(bild.height()):
            aktpxl = bild.get(x, y)
            color = rgb2hex(aktpxl[0], aktpxl[1], aktpxl[2])
            pixellistcolors.append(color)
            pixellist.append(aktpxl)
            durchlauf += 1
            if round(allpixels / 5) == durchlauf:
                prozent += 20
                durchlauf = 0
                print(str(prozent) + "% der Pixel erfasst.")
    return pixellistcolors, pixellist

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def hex2rgb(hexcode):
    value = hexcode.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def mischen():
    global bild
    pxllst, x = getallpixels()
    allpixels = round(len(pxllst)/20)
    durchlauf = 0
    prozent = 0
    for x in range(bild.width()):
        for y in range(bild.height()):
            color = pxllst.pop(randint(0, (len(pxllst) - 1)))
            bild.put(color, (x, y))
            durchlauf += 1
            if allpixels == durchlauf:
                prozent += 5
                durchlauf = 0
                print(str(prozent) + "% der Pixel umgewandelt.")
                fenster.update()

def getallcolors():
    colorlist, allpxls = getallpixels()
    colors = []
    lenge = round(len(colorlist)/10)
    durchlauf = 0
    prozent = 0
    for i in colorlist:
        if not i in colors:
            colors.append(i)
        durchlauf += 1
        if lenge == durchlauf:
            prozent += 10
            durchlauf = 0
            print(str(prozent) + "% der Farben erfasst.")
    x = []
    for i in colors:
        x.append(tuple([hex2rgb(i), choice(colors)]))
    colordict = dict(x)
    return colordict, allpxls

def tauschen():
    global bild
    coldict, allpxls = getallcolors()
    allpixels = round(len(allpxls)/20)
    durchlauf = 0
    d2 = 0
    prozent = 0
    for x in range(bild.width()):
        for y in range(bild.height()): 
            color = coldict[allpxls[d2]]
            bild.put(color, (x, y))
            durchlauf += 1
            d2 += 1
            if allpixels == durchlauf:
                prozent += 5
                durchlauf = 0
                print(str(prozent) + "% der Pixel umgewandelt.")
                fenster.update()

def save():
    global bild
    save = asksaveasfilename(title="Speicherort wählen.") + ".png"
    bild.write(save)

def makeImage(x=True):
    global bild, label
    foto = "./programdata/abstrakt/photo.png"
    try:
        pygame.camera.init()
        camlist = pygame.camera.list_cameras()
        cam = pygame.camera.Camera(camlist[int(input("Kamera-Index angeben (Default: -1): ") or "-1")],(1280, 720))
        cam.start()
        sleep(1)
        img = cam.get_image()
        pygame.image.save(img, foto)
        if x:
            assert ""
    except:
        foto = askopenfilename(title="Foto auswählen")
    finally:
        bild = PhotoImage(file=foto)
        try:
            label.destroy()
        except:
            print("[Destroying error]")
        finally:
            label = Label(master=fenster, image=bild)
            label.pack()

fenster = Tk()
fenster.title("humoristische Bilder 1.3")
button = Button(master=fenster, command=mischen, font=("Arial", 12), text="Foto in den Mixer")
button4 = Button(master=fenster, command=tauschen, font=("Arial", 12), text="Farben tauschen")
button2 = Button(master=fenster, command=save, font=("Arial", 12), text="Bild speichern")
button3 = Button(master=fenster, command=makeImage, font=("Arial", 12), text="Neues Bild machen")

label = None

button.pack(fill=Y)
button2.pack(fill=Y)
button3.pack(fill=Y)
button4.pack(fill=Y)
makeImage(x=False)

fenster.mainloop()
