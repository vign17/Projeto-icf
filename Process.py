import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import math as mt

sp.init_printing()
M=0.02896                                                                       #massa molar do ar
R=8.314                                                                         #R
m=2990000                                                                       #massa do foguete
m0=m                                                                            #massa inicial do foguete
A=25*mt.pi                                                                      #Área do foguete
C=0.3                                                                           #Coeficiente de arrasto
G=6.67*10**(-11)                                                                #G
Mt=5.98*10**(24)                                                                #Massa da terra
Ae=8.82                                                                         #Área de exaustão
Re=6371000                                                                      #Área de exaustão
Y0=89.999*mt.pi/180                                                             #ângulo
Y=Y0
v0=0
v=v0
h0=0
h=h0
P0=101325
P=P0
D=0
I=0
g=0
T0=300
T=T0
d=0                                                                             #densidade do ar
dt=0.001
X=0
t=0
E=0                                                                             #energia da órbita

me=10040                                                                        #kg/s
ve=2256
Pe=400000
time=1200

def arrasto(d):
  D=(d*A*15)/2                            #arrasto divido pelo quadrado da velocidade
  return(D)

#def impulso(P,v):
#    T= me*(ve+v)+Ae*(Pe-P)
#    return(T)

def gravidade(h):
  g=G*Mt/(Re+h)**2
  return(g)

def dens1(P0,g,T0,h):
  d=(P0*M/(R*T0))*(1+2*M*g*(-h)/(7*R*T0))**(5/2)
  return(d)

def press1(P0,g,T0,h):
  P=P0*(1+2*M*g*(-h)/(7*R*T0))**(7/2)
  return(P)

def dens2(P1,g,T1,h):
  d=(P1*M/(R*T1))*mt.exp(-M*g*h/(R*T1))
  return(d)

def press2(P1,g,T1,h):
  P=P1*mt.exp(-M*g*h/(R*T1))
  return(P)

def dv_dt(v,P,D,g,Y,m,Pe,ve,me):
    d=(2*(me*ve+Ae*(Pe-P))/m-D*v**2/m-g*mt.sin(Y))
    return(d)

def dy_dt(v,h,g,Y):
    d=(v**2/(Re+h)-g)*mt.cos(Y)/v
    return(d)

def dY2_dt(Y,t):
  n=-0.13*mt.pow(Y,0.5)/t
  return(n)

x_pos=np.zeros(int(time/dt))
y_pos=np.zeros(int(time/dt))
Y_pos=np.zeros(int(time/dt))
t_pos=np.zeros(int(time/dt))
m_pos=np.zeros(int(time/dt))
E_pos=np.zeros(int(time/dt))
exc_pos=np.zeros(int(time/dt))
a_pos=np.zeros(int(time/dt))
p_pos=np.zeros(int(time/dt))
Re_pos=np.zeros(int(time/dt))
for i in range(0,int(time/dt)):
  Re_pos[i]=Re

test=0

while(t<time):
    if(t>160):
      me=1868                                                                        #kg/s
      ve=1256
      Pe=600000
    if(t>700):
      me=360                                                                        #kg/s
      ve=686
      Pe=30000
    if(t>1200):
      me=0
      ve=0
      Pe=0
    if(t==0):
      P = press1(P0,g,T0,h)
      d = dens1(P0,g,T0,h)
      #print("P "+P)
      g = gravidade(h)
      #I= impulso(P,v)
      D = arrasto(d)
      v_back=dv_dt(v,P,D,g,Y,m,Pe,ve,me)
      v+=(v_back+dv_dt(v+v_back*dt,P,D,g,Y,m,Pe,ve,me))*dt/2
      X+=(Re/(Re+h)*v*mt.cos(Y))*dt
      x_pos[int(t/dt)]=X
      h+=(v*mt.sin(Y))*dt
      y_pos[int(t/dt)]=h
      Y_back=dy_dt(v,h,g,Y)
      Y+=(Y_back+dy_dt(v,h,g,Y+dt*Y_back))*dt/2
      Y_pos[int(t/dt)]=Y*180/mt.pi
      m-=me*dt
      m_pos[int(t/dt)]=m
      E_pos[int(t/dt)]=v**2/2-G*Mt/(h+Re)
      e_m=v**2/2-G*Mt/(h+Re)
      exc_pos[int(t/dt)]=(1+(2*e_m*((h+Re)*v*mt.sin(mt.pi+Y))**2)/(G*Mt)**2)**0.5
      a_pos[int(t/dt)]=-G*Mt/e_m
      p_pos[int(t/dt)]=a_pos[int(t/dt)]*(1-exc_pos[int(t/dt)])
      t_pos[int(t/dt)]=t
      t-=dt
    elif(t==-dt):
      t=dt
      if(h<11000):
          P1= press1(P0,g,T0,h)
          d1= dens1(P0,g,T0,h)
      else:
          P1= press2(P0,g,T0,h)
          d1= dens2(P0,g,T0,h)
      #print("P "+P)
      g1= gravidade(h)
      #I= impulso(P,v)
      D1= arrasto(d)
      v_back=dv_dt(v,P,D,g,Y,m,Pe,ve,me)
      v1=v+(v_back+dv_dt(v+v_back*dt,P1,D1,g1,Y,m,Pe,ve,me))*dt/2
      X1=X+(Re/(Re+h)*v*mt.cos(Y))*dt
      x_pos[int(t/dt)]=X
      h1=h+(v*mt.sin(Y))*dt
      y_pos[int(t/dt)]=h
      Y_back=dy_dt(v,h,g,Y)
      Y1=Y+(Y_back+dy_dt(v,h,g,Y+dt*Y_back))*dt/2
      Y_pos[int(t/dt)]=Y*180/mt.pi
      m1=m-me*dt
      m_pos[int(t/dt)]=m
      E_pos[int(t/dt)]=v**2/2-G*Mt/(h+Re)
      e_m=v**2/2-G*Mt/(h+Re)
      exc_pos[int(t/dt)]=(1+(2*e_m*((h+Re)*v*mt.sin(mt.pi+Y))**2)/(G*Mt)**2)**0.5
      a_pos[int(t/dt)]=-G*Mt/e_m
      p_pos[int(t/dt)]=a_pos[int(t/dt)]*(1-exc_pos[int(t/dt)])
      t_pos[int(t/dt)]=t
    else:
        if(h<11000):
            P=P1
            P1= press1(P0,g,T0,h)
            d=d1
            d1= dens1(P0,g,T0,h)
        elif(h<50000 and h>11000):
            P=P1
            P1= press2(P0,g,T0,h)
            d=d1
            d1= dens2(P0,g,T0,h)
        else:
            P=0
            d=0
        #print("P "+P)
        g=g1
        g1= gravidade(h)
        #I= impulso(P,v)
        D=D1
        D1= arrasto(d)
        v_back=dv_dt(v,P,D,g,Y,m,Pe,ve,me)
        v=v1
        v1+=(v_back+dv_dt(v+v_back*dt,P1,D1,g1,Y1,m1,Pe,ve,me))*dt/2
        X=X1
        X1+=(Re/(Re+h)*v*mt.cos(Y)+Re/(Re+h1)*v1*mt.cos(Y1))*dt/2
        x_pos[int(t/dt)]=X1
        h=h1
        h1+=((v*mt.sin(Y))+v1*mt.sin(Y1))*dt/2
        y_pos[int(t/dt)]=h1
        Y_back=dy_dt(v,h,g,Y)
        Y=Y1
        Y1=Y+(dY2_dt(Y,t)+dY2_dt(Y+dt*dY2_dt(Y,t),t+dt))*dt/2
        Y_pos[int(t/dt)]=Y1*180/mt.pi
        m=m1
        m1-=me*dt
        m_pos[int(t/dt)]=m
        t_pos[int(t/dt)]=t
        E_pos[int(t/dt)]=v**2/2-G*Mt/(h+Re)
        e_m=v**2/2-G*Mt/(h+Re)
        exc_pos[int(t/dt)]=(1+(2*e_m*((h+Re)*v*mt.sin(mt.pi/2+Y))**2)/(G*Mt)**2)**0.5
        a_pos[int(t/dt)]=-G*Mt/(2*e_m)
        p_pos[int(t/dt)]=a_pos[int(t/dt)]*(1-exc_pos[int(t/dt)])
        t+=dt

plt.plot(t_pos,Y_pos, marker='o', linestyle='none', ms=0.01)
plt.title("Inclinação x tempo")
plt.ylabel("Y(º)")
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

plt.plot(t_pos,E_pos, marker='o', linestyle='none', ms=0.01)
plt.title("Energia x tempo")
plt.ylabel("e(J/kg)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

plt.plot(t_pos,exc_pos, marker='o', linestyle='none', ms=0.01)
plt.title("Excentricidade x tempo")
plt.ylabel("e")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

plt.plot(t_pos,p_pos/1000, marker='o', linestyle='none', ms=0.01)
plt.plot(t_pos,Re_pos/1000, color='red')
plt.title("Periastro x tempo")
plt.ylabel("P(km)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

#òrbita
#iteração da anomalia excêntrica com método de Newton(OK)
def iterarE(ecen, M, chute):
  e0 = chute
  for i in range(0,10):                                                                    #salva o último valor em caso de conferência
    e0 = e0 - (M - e0 + ecen * mt.sin(e0)) / (ecen*mt.cos(e0) - 1)
  return (e0)

def angulo(x):
    if x>2*mt.pi*Re:
        x=x-(x//(2*mt.pi*Re))*2*mt.pi*Re
    a=x/Re
    return(a)
  
#Tratamento inicial
time2=14400
r_orb=np.zeros(int(time2/dt))
th_orb=np.zeros(int(time2/dt))
x_orb=np.zeros(int(time2/dt))
y_orb=np.zeros(int(time2/dt))
t_orb=np.zeros(int(time2/dt))
rho_orb=np.zeros(int(time2/dt))
r=h+Re
r_orb[0]=r
v=v
exc=exc_pos[int(time/dt)-1]
a=a_pos[int(time/dt)-1]
phi=Y+mt.pi/2
n=mt.sqrt(G*Mt/a**3)
theta=mt.acos((a*(1-exc**2)-r)/(r*exc))
th_orb[0]=theta                                                                   #calcular a variação para extrair informção
AE_roc=mt.acos((r-a)/(-a*exc))
AM_roc=AE_roc-exc*mt.sin(AE_roc)
t=AM_roc/n
t_orbit=dt

rho_orb[0]=angulo(x_pos[int(time/dt)-1])

#Tratamento padrão
while (t_orbit<time2):
  AM_roc+=n*dt
  AE_roc=iterarE(exc,AM_roc,AE_roc)
  theta=2*mt.atan(mt.sqrt((1+exc)/(1-exc))*mt.tan(AE_roc/2))
  th_orb[int(t_orbit/dt)]=theta
  r=a*(1-exc*mt.cos(AE_roc))
  r_orb[int(t_orbit/dt)]=r
  t_orb[int(t_orbit/dt)]=t_orbit
  rho_orb[int(t_orbit/dt)]=rho_orb[0]+th_orb[int(t_orbit/dt)]-th_orb[0]
  x_orb[int(t_orbit/dt)]=r*mt.sin(rho_orb[int(t_orbit/dt)])
  y_orb[int(t_orbit/dt)]=r*mt.cos(rho_orb[int(t_orbit/dt)])
  t_orbit+=dt

plt.plot(t_orb,y_orb/1000, marker='o', linestyle='none', ms=0.01)
plt.title("Trajetória")
plt.ylabel("y(km)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

plt.plot(t_orb,x_orb/1000, marker='o', linestyle='none', ms=0.01)
plt.title("Trajetória")
plt.ylabel("x(km)")
plt.xlabel("t(s)")
plt.grid()
plt.show()

print("\n")

with open("posicaoX.txt","w") as file:
   indc = len(x_pos)
   for ka in range(0,indc):
      file.write(str(x_pos[ka])+",")

with open("posicaoY.txt","w") as file:
   indc = len(y_pos)
   for ka in range(0,indc):
      file.write(str(y_pos[ka])+",")

with open("posicaoX2.txt","w") as file:
   indc = len(x_orb)
   for ka in range(0,indc):
      file.write(str(x_orb[ka])+",")

with open("posicaoY2.txt","w") as file:
   indc = len(y_orb)
   for ka in range(0,indc):
      file.write(str(y_orb[ka])+",")