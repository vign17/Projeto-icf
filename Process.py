import numpy as np
import matplotlib.pyplot as plt
import math as mt

#Constantes
R = 8.314                                                      #Constante Universal dos Gases Ideais (J/kgK)
G = 6.67e-11                                                   #Constante de Gravitação universal (Nm²/kg²)


#Dados da Terra
Mt = 5.98e24                                                   #Massa da terra (kg)
Re = 6371000.0                                                 #Raio da Terra (m)


#Dados da atmosfera
M = 0.02896                                                    #Massa molar do ar (kg/mol)
P0 = 101325.0                                                  #Pressão Atmosférica no nível do mar (Pa)
T0 = 300.0                                                     #Temperatura da atmosfera no nível do mar (K)


#Dados do foguete
m = 2990000.0                                                  #Massa inicial do foguete (kg)
A = 250*np.pi                                                   #Área frontal do foguete (m²)
C = 0.3                                                        #Coeficiente de arrasto
Ae = 8.82                                                      #Área de exaustão (m²)
me = 10040.0                                                   #Taxa de queima de combustível (kg/s)
ve = 2256.0                                                    #Velocidade de exaustão (m/s)
Pe = 400000.0                                                  #Pressão de exaustão (Pa)
Y0 = 89.999*np.pi/180                                          #Ângulo de voo inicial (rad)
v0 = 0.0                                                       #Velocidade inicial (m/s)
h0 = 0.0                                                       #Altura inicial (m)
X = 0.0                                                        #Posição x inicial (m)


#Condições iniciais
P = P0
m0 = m
Y = Y0
v = v0
h = h0
D = 0.0
g = 0.0
T = T0
d = 0.0
E = 0.0


#Tempo
t = 0.0                                                        #Instante de tempo inicial (s)
dt = 0.001                                                     #Intervalo de tempo para aplicação do método (s)
time = 1200                                                    #Tempo total de execução da simulação do lançamento (s)


#Definição de funções
#Arrasto dividido pelo quadrado da velocidade
def arrasto(dc):
   return (dc*A*1.5)/2


#Gravidade
def gravidade(hc):
   return G*Mt/(Re+hc)**2


#Densidade da atmosfera na primeira faixa (até 11km de altitude)
def dens1(P0,g,T0,h):
  d=(P0*M/(R*T0))*(1+2*M*g*(-h)/(7*R*T0))**(5/2)
  return(d)

#Pressão atmosférica na primeira faixa (até 11km de altitude)
def press1(P0,g,T0,h):
  P=P0*(1+2*M*g*(-h)/(7*R*T0))**(7/2)
  return(P)


#Densidade da atmosfera na segunda faixa (após 11km de altitude)
def dens2(P1,g,T1,h):
  d=(P1*M/(R*T1))*np.exp(-M*g*h/(R*T1))
  return(d)

#Pressão atmosférica na segunda faixa (após 11km de altitude)
def press2(P1,g,T1,h):
  P=P1*np.exp(-M*g*h/(R*T1))
  return(P)


#Taxa de variação da velocidade no tempo (O impulso é calculado dentro da função)
def dv_dt(v,P,D,g,Y,m,Pe,ve,me):
    d=(2*(me*ve+Ae*(Pe-P))/m-D*v**2/m-g*np.sin(Y))
    return(d)

#Taxa de variação da altitude no tempo
def dy_dt(v,h,g,Y):
    d=(v**2/(Re+h)-g)*np.cos(Y)/v
    return(d)

#Taxa de variação do ângulo de voo no tempo
def dY2_dt(Y,t):
  n=-0.13*pow(Y,0.5)/t
  return(n)


#Criando vetores preenchidos com zeros, de dimensão igual ao tempo total dividido pelo intervalo de tempo da iteração
n = int(time/dt)
x_pos = np.zeros(n)                   #Posição x
y_pos = np.zeros(n)                   #Posição y (altitude)
Y_pos = np.zeros(n)                   #Ângulo de voo
t_pos = np.zeros(n)                   #Instante de tempo
m_pos = np.zeros(n)                   #Massa do foguete
E_pos = np.zeros(n)                   #Anomalia excêntrica
exc_pos = np.zeros(n)                 #Excentricidade
a_pos = np.zeros(n)                   #Semieixo maior
p_pos = np.zeros(n)                   #Posição na órbita
Re_pos = np.array([Re]*n)             #Lista preenchida com o valor do raio da Terra (apenas para referência)



#Primeira etapa: Lançamento
print("Iniciando a primeira etapa: Lançamento")
#Laço que ocorre enquanto o instante de tempo for menor que o tempo total

indicador = "Realizando cálculos"
contador = 0
contador2 = 0


while(t<time):
    contador += 1
    contador2 +=1
    #Indicador de que o laço está rodando
    if contador == 10000:
       contador = 0
       if len(indicador)<=22:
          indicador += "."
       else:
          indicador = "Realizando cálculos."
       print(indicador+" ",int(contador2/time*dt*100),"%")


    if(t>160):                              #Verifica se já é tempo do segundo estágio
      #Dados do segundo estágio
      me = 1868.0                           #Taxa de queima de combustível (kg/s)
      ve = 1256.0                           #Velocidade de exaustão (m/s)
      Pe = 600000.0                         #Pressão de exaustão(Pa)
    if(t>700):                              #Verifica se já é tempo do terceiro estágio
      #Dados do segundo estágio
      me = 360.0                            #Taxa de queima de combustível (kg/s)
      ve = 686.0                            #Velocidade de exaustão (m/s)
      Pe = 30000.0                          #Pressão de exaustão(Pa)
    if(t>1200):                             #Verifica se já é tempo de desligar os motores 
      #Motores desligados
      me = 0.0                              #Taxa de queima de combustível (kg/s)
      ve = 0.0                              #Velocidade de exaustão (m/s)
      Pe = 0.0                              #Pressão de exaustão(Pa)
    
    if(t==0):                                                                   #Verifica se é o instante inicial
      #Calcula as variáveis de ambiente

      P = press1(P0,g,T0,h)                                                     #Pressão  atmosférica
      d = dens1(P0,g,T0,h)                                                      #Densidade da atmosfera
      g = gravidade(h)                                                          #Gravidade

      #Calcula o arrasto
      D = arrasto(d)                                                            #Arrasto
      
      #Aplicação do método de Euler simples para calcular o próximo ponto a partir das condições iniciais
      v_back=dv_dt(v,P,D,g,Y,m,Pe,ve,me)                                                #Taxa de variação da velocidade no tempo
      v+=(v_back+dv_dt(v+v_back*dt,P,D,g,Y,m,Pe,ve,me))*dt/2                            #Velocidade
      X+=(Re/(Re+h)*v*np.cos(Y))*dt                                                     #Posição em x
      x_pos[int(t/dt)]=X
      h+=(v*np.sin(Y))*dt                                                               #Altitude
      y_pos[int(t/dt)]=h
      Y_back=dy_dt(v,h,g,Y)                                                             #Taxa de variação do ângulo de voo
      Y+=(Y_back+dy_dt(v,h,g,Y+dt*Y_back))*dt/2                                         #Ângulo de voo
      Y_pos[int(t/dt)]=Y*180/np.pi
      m-=me*dt                                                                          #Massa do foguete
      m_pos[int(t/dt)]=m
      E_pos[int(t/dt)]=v**2/2-G*Mt/(h+Re)
      e_m=v**2/2-G*Mt/(h+Re)
      exc_pos[int(t/dt)]=(1+(2*e_m*((h+Re)*v*np.sin(np.pi+Y))**2)/(G*Mt)**2)**0.5
      a_pos[int(t/dt)]=-G*Mt/e_m
      p_pos[int(t/dt)]=a_pos[int(t/dt)]*(1-exc_pos[int(t/dt)])
      t_pos[int(t/dt)]=t
      t-=dt                                                                             #Retorna um passo
    
    #Verifica se a etapa anterior foi realizada
    elif(t==-dt):
        t = dt                          #Avança um passo, considerando, assim, a etapa anterior como instante inicial

        #Sendo a primeira iteração, o foguete está na faixa 1 na atmosfera (até 11km de altitude)
        #Calculando as variáveis de ambiente
        P1= press1(P0,g,T0,h)                     #Pressão Atmosférica
        d1= dens1(P0,g,T0,h)                      #Densidade da atmosfera
        g1= gravidade(h)                          #Gravidade
        
        #Calcula o arrasto
        D1 = arrasto(d)                           #Arrasto
      
      
        #Aplicando Euler Simples para calcular mais um ponto, a partir do ponto anterior
        v_back=dv_dt(v,P,D,g,Y,m,Pe,ve,me)
        v1=v+(v_back+dv_dt(v+v_back*dt,P1,D1,g1,Y,m,Pe,ve,me))*dt/2
        X1=X+(Re/(Re+h)*v*np.cos(Y))*dt
        x_pos[int(t/dt)]=X
        h1=h+(v*np.sin(Y))*dt
        y_pos[int(t/dt)]=h
        Y_back=dy_dt(v,h,g,Y)
        Y1=Y+(Y_back+dy_dt(v,h,g,Y+dt*Y_back))*dt/2
        Y_pos[int(t/dt)]=Y*180/np.pi
        m1=m-me*dt
        m_pos[int(t/dt)]=m
        E_pos[int(t/dt)]=v**2/2-G*Mt/(h+Re)
        e_m=v**2/2-G*Mt/(h+Re)
        exc_pos[int(t/dt)]=(1+(2*e_m*((h+Re)*v*np.sin(np.pi+Y))**2)/(G*Mt)**2)**0.5
        a_pos[int(t/dt)]=-G*Mt/e_m
        p_pos[int(t/dt)]=a_pos[int(t/dt)]*(1-exc_pos[int(t/dt)])
        t_pos[int(t/dt)]=t
    
    
    else:                                   #Caso tenha passado pelos dois passos anteriores, entra no laço final
        
        if(h<11000):                        #Verifica se o foguete está na faixa 1 da atmosfera (até 11km de altitude)
            P = P1
            P1= press1(P0,g,T0,h)
            d = d1
            d1= dens1(P0,g,T0,h)
        elif(h<50000 and h>11000):          #Verifica se o foguete está na faixa 2 da atmosfera (de 11km até 50km de altitude)
            P = P1
            P1= press2(P0,g,T0,h)
            d = d1
            d1= dens2(P0,g,T0,h)
        else:                               #O foguete já passou da atmosfera
            P = 0.0
            d = 0.0
        
        #Cálculo da gravidade
        g = g1
        g1 = gravidade(h)
        
        #Cálculo do arrasto
        D = D1
        D1 = arrasto(d)
        
        #Aplicação do método de Euler Melhorado
        v_back=dv_dt(v,P,D,g,Y,m,Pe,ve,me)
        v=v1
        v1+=(v_back+dv_dt(v+v_back*dt,P1,D1,g1,Y1,m1,Pe,ve,me))*dt/2
        X=X1
        X1+=(Re/(Re+h)*v*np.cos(Y)+Re/(Re+h1)*v1*np.cos(Y1))*dt/2
        x_pos[int(t/dt)]=X1
        h=h1
        h1+=((v*np.sin(Y))+v1*np.sin(Y1))*dt/2
        y_pos[int(t/dt)]=h1
        Y_back=dy_dt(v,h,g,Y)
        Y=Y1
        Y1=Y+(dY2_dt(Y,t)+dY2_dt(Y+dt*dY2_dt(Y,t),t+dt))*dt/2
        Y_pos[int(t/dt)]=Y1*180/np.pi
        m=m1
        m1-=me*dt
        m_pos[int(t/dt)]=m
        t_pos[int(t/dt)]=t
        E_pos[int(t/dt)]=v**2/2-G*Mt/(h+Re)
        e_m=v**2/2-G*Mt/(h+Re)
        exc_pos[int(t/dt)]=(1+(2*e_m*((h+Re)*v*np.sin(np.pi/2+Y))**2)/(G*Mt)**2)**0.5
        a_pos[int(t/dt)]=-G*Mt/(2*e_m)
        p_pos[int(t/dt)]=a_pos[int(t/dt)]*(1-exc_pos[int(t/dt)])
        t+=dt

print("Cálculos do lançamento finalizados\n")


#Gráficos do lançamento
print("Plotando gráficos do lançamento")

plt.plot(t_pos,Y_pos, marker='o', linestyle='none', ms=0.01)
plt.title("Inclinação x tempo")
plt.ylabel("Y(°)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

plt.plot(x_pos/1000,y_pos/1000, marker='o', linestyle='none', ms=0.01)
plt.title("Trajetória")
plt.ylabel("h(km)")
plt.xlabel("x(km)")
plt.grid()
plt.show()

print("\n")

plt.plot(t_pos,m_pos, marker='o', linestyle='none', ms=0.01)
plt.title("Massa")
plt.ylabel("m(kg)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

#Deve se manter abaixo de 0 para órbitas fechadas
plt.plot(t_pos,E_pos, marker='o', linestyle='none', ms=0.01)
plt.title("Energia por unidade de massa x tempo")
plt.ylabel("e(J/kg)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

#Quanto mais próximo de 0 mais se aproxima de um círculo e quanto mais próximo de 1 mais se aproxima de uma parábola
plt.plot(t_pos,exc_pos, marker='o', linestyle='none', ms=0.01)
plt.title("Excentricidade x tempo")
plt.ylabel("e")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

#Deve ultrapassar o raio terrestre em algumas centenas de kilometros para não ocorrer interações desnecessárias com a atmosfera
plt.plot(t_pos,p_pos/1000, marker='o', linestyle='none', ms=0.01)
plt.plot(t_pos,Re_pos/1000, color='red')
plt.title("Periastro x tempo")
plt.ylabel("P(km)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("Gráficos do lançamento finalizados\n")

#Criando os arquivos com as posições
print("Criando arquivos do lançamento")

#Arquivo com as posições em x
print("Criando arquivo das posições x")
with open("posicoesXLancamento.txt","w") as file:
   indxc = len(x_pos)
   for ka in range(0,indxc):
      file.write(str(x_pos[ka])+",")
print("Arquivo das posições x criado")

print("Criando arquivo das posições y")
#Arquivo com as posições em y
with open("posicoesYLancamento.txt","w") as file:
   indyc = len(y_pos)
   for ka in range(0,indyc):
      file.write(str(y_pos[ka])+",")
print("Arquivo das posições y criado")

print("Arquivos do lançamento criados")
print("Etapa do Lançamento finalizada\n")


#Segunda etapa: Órbita
print("Iniciando a segunda etapa: Órbita")

#iteração da anomalia excêntrica com o método de Newton
def iterarE(ecen, M, chute):
  e0 = chute                                                                      #chute definido como o útltimo valor da anomalia excêntrica para prever erros
  for i in range(0,10):
    e0 = e0 - (M - e0 + ecen * np.sin(e0)) / (ecen*np.cos(e0) - 1)
  return (e0)

#conversão da coordenada cartesiana x em polar
def angulo(x):
    if x>2*np.pi*Re:
        x=x-(x//(2*np.pi*Re))*2*np.pi*Re
    a=x/Re
    return(a)
  
a=a_pos[int(time/dt)-1]                                                           #Definição do semi eixo maior da órbita como valor calculado quando os motores foram desligados
Per=2*np.pi*np.sqrt(a**3/(G*Mt))                                                  #Cálculo do período orbital pela 3ª lei de Kepler
time2=int(Per)+1
n_orb=int(time2/dt)

#Criando vetores preenchidos com zeros, de dimensão igual ao tempo total dividido pelo intervalo de tempo da iteração
r_orb=np.zeros(n_orb)                                                             #distância ao foco da elipse
th_orb=np.zeros(n_orb)                                                            #anomalia verdadeira
x_orb=np.zeros(n_orb)                                                             #posição x
y_orb=np.zeros(n_orb)                                                             #posição y
t_orb=np.zeros(n_orb)                                                             #tempo
rho_orb=np.zeros(n_orb)                                                           #Ângulo entre o vetor posição e o vetor y

#Definido a excentricidade como o mesmo valor calculado quando os motores foram desligados
exc=exc_pos[int(time/dt)-1]

r=h+Re
r_orb[0]=r                                                                        #Definindo distância inicial do foguete ao centro da terra (foco da elipse)  
phi=Y+np.pi/2                                                                     #ângulo inicial entre vetor velocidade e vetor posição (antigo ângulo do foguete com a horizontal mais um ângulo reto)
n=np.sqrt(G*Mt/a**3)                                                              #Representa a velocidade angular média do corpor em rad/s derivada da 3ª lei de kepler
th_orb[0]=mt.acos((a*(1-exc**2)-r)/(r*exc))                                       #Cálculo da anomalia verdadeira inicial
rho_orb[0]=angulo(x_pos[int(time/dt)-1])                                          #Cálculo da ângulo inicial entre o vetor posição e o vetor y
x_orb[0]=r*np.sin(rho_orb[0])                                                     #Cálculo da posição x inicial
y_orb[0]=r*np.cos(rho_orb[0])                                                     #Cálculo da posição y inicial
AE_roc=mt.acos((r-a)/(-a*exc))                                                    #Cálculo da anomalia excêntrica inicial
AM_roc=AE_roc-exc*np.sin(AE_roc)                                                  #Cálculo da anomalia média inicial
t=AM_roc/n                                                                        #Obtenção do tempo relativo a anomalia média
t_orbit=0                                                                        

indicador = "Realizando cálculos"
contador = 0
contador2 = 0

#Ciclo orbital
while (t_orbit<time2):
  contador += 1
  contador2 +=1
  #Indicador de que o laço está rodando
  if contador == 10000:
    contador = 0
    if len(indicador)<=22:
      indicador += "."
    else:
      indicador = "Realizando cálculos."
    print(indicador+" ",int(contador2/time2*dt*100),"%")
  AM_roc+=n*dt                                                                    #Cálculo da próxima anomalia média
  ind=int(t_orbit/dt)                                                             #Definição do índice desta iteração
  AE_roc=iterarE(exc,AM_roc,AE_roc)                                               #Cálculo da anomalia excêntrica
  th_orb[ind]=2*mt.atan(np.sqrt((1+exc)/(1-exc))*np.tan(AE_roc/2))                #Cálculo da anomalia verdadeira
  r=a*(1-exc*np.cos(AE_roc))                                                      #Cálculo da distância
  r_orb[ind]=r                                                                    #Armazenamento de r
  t_orb[ind]=t_orbit                                                              #Armazenamento do tempo referente a todas grandezas calculadas
  rho_orb[ind]=rho_orb[0]+th_orb[ind]-th_orb[0]                                   #Cálculo e armazenamento do ângulo entre vetor posição e vetor y
  x_orb[ind]=r*np.sin(rho_orb[ind])                                               #Cálculo e armazenamento da coordenada x
  y_orb[ind]=r*np.cos(rho_orb[ind])                                               #Cálculo e armazenamento da coordenada y
  t_orbit+=dt                                                                     #Avanaço temporal

#Gráfico da posição y durante o tempo (Para uma elipse deve apresentar comportamento oscilatório)
plt.plot(t_orb,y_orb/1000, marker='o', linestyle='none', ms=0.01)
plt.title("Trajetória")
plt.ylabel("y(km)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

#Gráfico da posição x durante o tempo (Para uma elipse deve apresentar comportamento oscilatório)
plt.plot(t_orb,x_orb/1000, marker='o', linestyle='none', ms=0.01)
plt.title("Trajetória")
plt.ylabel("x(km)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

#Arquivo com as posições em x
with open("posicoesXOrbita.txt","w") as file:
   indyc = len(x_orb)
   for ka in range(0,indyc):
      file.write(str(x_orb[ka])+",")
print("Arquivo das posições x criado")

#Arquivo com as posições em y
with open("posicoesYOrbita.txt","w") as file:
   indyc = len(y_orb)
   for ka in range(0,indyc):
      file.write(str(y_orb[ka])+",")
print("Arquivo das posições y criado")

print("Arquivos da órbita criados")
print("Etapa do Órbita finalizada\n")
print("Cálculos de trajetória finalizada\n")