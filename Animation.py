from vpython import *
import math as mt

#Definição das constantes
Re = 6371000                                  #Raio da Terra (m)


#Definindo funções
#Função que calcula o ângulo a partir do arco de circunferência descrito (posição em x)
def angulo(x):
    if x>2*mt.pi*Re:                            #Evita que o índice -1 seja procurado na lista de posições
        x=x-(x//(2*mt.pi*Re))*2*mt.pi*Re
    a=x/Re
    return(a)

#Função que calcula a posição em x no referencial da animação (considerando a curvatura da Terra)
def turnx(a,h):
    x=h*mt.cos(3.14/2-a)
    return(x)

#Função que calcula a posição em x no referencial da animação (considerando a curvatura da Terra)
def turny(a,h):
    y=h*mt.sin(3.14/2-a)
    return(y)

#Função que verifica se a opção "Track" está ativada
def track(v):
    if v.checked==True:                             #Se sim, a câmera segue o projetil
        scene.follow(proj)
    elif v.checked==False:                          #Se não, centraliza a cena
        scene.follow(None)
        scene.center=vec(0,0,0)

radio(bind=track,text="Track")                      #Cria o botão de "Track"


#Configura o tamanho da cena
scene.width=1500
scene.height=700

#Criando o modelo do foguete
r=30000.0                               #Raio da cilindro (corpo)
proj=cylinder(pos=vector(0,0,Re), radius = r, axis=vector(0,0,200000), color=color.white, make_trail= True, trail_color=vector(1,0,0), trail_radius=10000)
nozzle=cone(pos=vector(0,0,Re+200000), radius = r, axis=vector(0,0,10000), color=color.white)
base=cone(pos=vector(0,0,Re), radius = r+10000, axis=vector(0,0,10000), color=color.black)

#Criando a Terra e inclinando de forma que Belo Horizonte esteja no centro do sistema de coordenadas
earth=sphere(pos=vector(0,0,0), radius = Re, texture=textures.earth)
earth.rotate(angle=44.1*pi/180,axis=vector(0,1,0),origin=vec(0,0,0))
earth.rotate(angle=-19*pi/180,axis=vector(1,0,0),origin=vec(0,0,0))

#Seta o título da cena
scene.title='Simulação lançamento de um foguete'
scene.up=vector(0,mt.cos(-19*pi/180),mt.sin(-19*pi/180))       #Rotaciona a câmera de forma que a Terra fique orientada da maneira usual


#Lendo os arquivos e criando as listas das posições
#Lançamento (em relação à superfície da Terra)
#Posições em x
with open("posicoesXLancamento.txt","r") as file:
    for string in file:
        posicoesX = string.split(",")

#Posições em y
with open("posicoesYLancamento.txt","r") as file:
    for string in file:
        posicoesY = string.split(",")

#Órbita
#Posições em x
with open("posicoesXOrbita.txt","r") as file:
    for string in file:
        posicoesX2 = string.split(",")

#Posições em y
with open("posicoesYOrbita.txt","r") as file:
    for string in file:
        posicoesY2 = string.split(",")

#Número de elementos nos arquivos, relacionados ao tempo de cada etapa
time_launch=len(posicoesX)
time_orb=len(posicoesY2)

#Switch para indicar passagem pela atmosfera
verif_atm=True
for i in range(0,int(time_launch/100)):
    rate(1000)
    #Definição das coordenadas do foguete
    alfa=angulo(float(posicoesX[i*100]))
    x=turnx(alfa,float(posicoesY[i*100])+Re)
    y=turny(alfa,float(posicoesY[i*100])+Re)
    
    #Atualização da posição do foguete
    proj.pos = vector(x,0,y)
    nozzle.pos = vector(x,0,y+200000)
    base.pos = vector(x,0,y)

    #Rotação do foguete, apartir do segundo índice pois é preciso uma posição anterior
    if(i>0):
        #Deslocamentos em relação ao eixos coordenados
        Vx=x-turnx(alfa,float(posicoesY[i*100-1]))
        Vy=y-turny(alfa,float(posicoesY[i*100-1]))

        #Aproxiamção dos senos e cossenos entre o vetor velocidade e os eixos coordenados
        axz=Vy/(Vx**2+Vy**2)**0.5
        axx=Vx/(Vx**2+Vy**2)**0.5

        #Atualição do eixo do foguete e rotação do mesmo
        proj.axis=vector(200000*axz,0,-200000*axx)
        nozzle.axis=vector(100000*axz,0,-100000*axx)
        base.axis=vector(100000*axz,0,-100000*axx)
        nozzle.pos=vector(x+200000*axz,0,y-200000*axx)

    #Avisos referenetes a momentos analisados através dos gráficos e códigos do programa anterior
    if(mag(proj.pos)-Re>50000) and verif_atm==True:
        scene.append_to_caption("\nO foguete passou pela atmosfera terrestre")
        verif_atm=False
    if(i==0):
        scene.append_to_caption('\n\nLançamento iniciado\n')
    if(i==1600):
        scene.append_to_caption('\nSegundo estágio acionado')
    if(i==7000):
        scene.append_to_caption('\n\nTerceiro estágio acionado')

    #Rotação da Terra
    earth.rotate(angle=7.27*10**-6, axis=vector(0,mt.cos(-19*mt.pi/180),mt.sin(-19*mt.pi/180)))

#Switch para sinalizar a órbita
verif_orb=True
i=1

#Ciclo da órbita
while True:
    rate(1000)
    #Definição das coordenadas do foguete
    x=float(posicoesX2[i*100])
    y=float(posicoesY2[i*100])

    #Atualização da posição do foguete
    proj.pos = vector(x,0,y)
    nozzle.pos = vector(x,0,y+200000)
    base.pos=vector(x,0,y)

    #Rotação do foguete, apartir do segundo índice pois a primeira posição foi armazenada como 0 por padrão
    if(i>2):
        #Deslocamentos em relação ao eixos coordenados
        Vx=float(posicoesX2[i*100])-float(posicoesX2[i*100-1])
        Vy=float(posicoesY2[i*100])-float(posicoesY2[i*100-1])

        #Aproxiamção dos senos e cossenos entre o vetor velocidade e os eixos coordenados
        axz=Vy/(Vx**2+Vy**2)**0.5
        axx=Vx/(Vx**2+Vy**2)**0.5

        #Atualição do eixo do foguete e rotação do mesmo
        proj.axis=vector(200000*axx,0,200000*axz)
        nozzle.axis=vector(100000*axx,0,100000*axz)
        base.axis=vector(100000*axx,0,100000*axz)
        nozzle.pos=vector(x+200000*axx,0,y+200000*axz)

    #Anúncio de entrada na órbita
    if(verif_orb==True):
        verif_orb=False
        scene.append_to_caption("\nO foguete entrou em uma órbita estável, motores desligados\n\n")
    i+=1

    #Retorna ao início quando a órbita chega ao seu fim, completa uma volta
    if (i==int(time_orb/100)-1):
        i=1

    #Rotação da Terra
    earth.rotate(angle=7.27*10**-6, axis=vector(0,mt.cos(-19*mt.pi/180),mt.sin(-19*mt.pi/180)))