from vpython import *
import numpy as np
import math as mt

Re = 6371000
ind=0

def angulo(x):
    if x>2*mt.pi*Re:
        x=x-(x//(2*mt.pi*Re))*2*mt.pi*Re
    a=x/Re
    return(a)

def turnx(a,h):
    x=h*mt.cos(3.14/2-a)
    return(x)

def turny(a,h):
    y=h*mt.sin(3.14/2-a)
    return(y)

def track(v):
    if v.checked==True:
        scene.follow(proj)
    elif v.checked==False:
        scene.follow(None)
        scene.center=vec(0,0,0)

radio(bind=track,text="Track")


scene.width=scene.height=600
r=30000.0
proj=sphere(pos=vector(0,0,Re), radius = r, color=color.white, make_trail= True, trail_color=vector(1,0,0), trail_radius=15000)
earth=sphere(pos=vector(0,0,0), radius = Re, texture=textures.earth)
earth.rotate(angle=44.1*pi/180,axis=vector(0,1,0),origin=vec(0,0,0))
earth.rotate(angle=-19*pi/180,axis=vector(1,0,0),origin=vec(0,0,0))
scene.title='Simulação lançamento de um foguete'


with open("posicaoX.txt","r") as file:
    for string in file:
        posicoesX = string.split(",")

with open("posicaoY.txt","r") as file:
    for string in file:
        posicoesY = string.split(",")

with open("posicaoX2.txt","r") as file:
    for string in file:
        posicoesX2 = string.split(",")

with open("posicaoY2.txt","r") as file:
    for string in file:
        posicoesY2 = string.split(",")

verif_atm=True
for i in range(0,12000):
    rate(1000)
    alfa=angulo(float(posicoesX[i*100]))
    x=turnx(alfa,float(posicoesY[i*100])+Re)
    y=turny(alfa,float(posicoesY[i*100])+Re)
    proj.pos = vector(x,0,y)
    if(mag(proj.pos)-Re>50000) and verif_atm==True:
        scene.append_to_caption("\nO foguete passou pela atmosfera terrestre")
        verif_atm=False
    if(i==0):
        scene.append_to_caption('\n\nLançamento iniciado\n')
    if(i==1600):
        scene.append_to_caption('\nSegundo estágio acionado')
    if(i==7000):
        scene.append_to_caption('\n\nTerceiro estágio acionado')

    
    



for i in range(0,14400000):
    rate(1000)
    x=float(posicoesX2[i*100])
    y=float(posicoesY2[i*100])
    proj.pos = vector(x,0,y)
    if(i==0):
        scene.append_to_caption("\nO foguete entrou em uma órbita estável, motores desligados\n\n")

