#LISTA 7
#ZAD 2
#1.1...DONE
#1.2...DONE



from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time
import numpy as np

# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0
eye = np.array([-5., 5., 10.]);  # pozycja
orient = np.array([0., 0., -1.]);  # kierunek
up = np.array([0., 1., 0.]);  # góra

# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


part1 = {}
part1 = dd(part1)
part1.v = [3, 15, 1]
part1.p = [-5, 2, 3]
part1.m = 10
part1.r = 1
part1.col = [0, 0.5, 0]
part1.quad = None


# rysowanie sfery
def drawSphere(part):
    glLoadIdentity()
    glTranslatef(part.p[0], part.p[1], part.p[2])
    glColor3fv(part.col)
    gluSphere(part.quad, part.r, 16, 16)


# rysowanie podłogi
def drawFloor():
    glLoadIdentity()
    glColor3fv([0.3, 0.3, 0.3])
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 0, 10])
    glVertex3fv([10, 0, 10])
    glVertex3fv([10, 0, -10])
    glEnd()


def drawScianki():
    glLoadIdentity() # jedno sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT,GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 10, -10])
    glVertex3fv([-10, 10, 10])
    glVertex3fv([-10, 0, 10])
    glEnd()

    glLoadIdentity()  # drugo sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT,GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, 10])
    glVertex3fv([-10, 10, 10])
    glVertex3fv([10, 10, 10])
    glVertex3fv([10, 0, 10])
    glEnd()

    glLoadIdentity()  # trzecio sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT,GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([10, 0, 10])
    glVertex3fv([10, 10, 10])
    glVertex3fv([10, 10, -10])
    glVertex3fv([10, 0, -10])
    glEnd()

    glLoadIdentity()  # czwarto sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT,GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([10, 0, -10])
    glVertex3fv([10, 10, -10])
    glVertex3fv([-10, 10, -10])
    glVertex3fv([-
                 10, 0, -10])
    glEnd()




# ruch sfery
def updateSphere(part, dt,aero):
    # tutaj trzeba dodać obsługę sił, w tym grawitacji
    part.v[0] = part.v[0] + aero[0]
    part.v[1] = part.v[1] + aero[1]
    part.v[2] = part.v[2] + aero[2]
    part.p[0] += dt * part.v[0]
    part.p[1] += dt * part.v[1]
    part.p[2] += dt * part.v[2]


def checkSphereToSciankiCollision(part, k):
    if part.p[0] - part.r < 7:
        pass
    else:
        part.p[0] = 7+part.r
        part.v[0] = -part.v[0] * k

    if part.p[0] + part.r > -7:
        pass
    else:
        part.p[0] = -part.r -7
        part.v[0] = -part.v[0] * k

    if part.p[2] - part.r < 7:
        pass
    else:
        part.p[2] = 7 + part.r
        part.v[2] = - part.v[2] * k

    if part.p[2] + part.r > -7:
        pass
    else:
        part.p[2] = -part.r - 7
        part.v[2] = - part.v[2] * k

def graw(h,a):
    return h*a

# sprawdzenie czy doszło do kolizji
def checkSphereToFloorCollision(part):
    if part.p[1] - part.r < 0:
        return True
    else:
        # jeśli sfera zachodzi pod podłogę, to podnieś ją
        if part.p[1] - part.r < 0:
            part.p[1] = part.r
            part.v[1] = - part.v[1]


# obsługa kolizji
def updateSphereCollision(part):
    if not checkSphereToFloorCollision(part1):
        return
    else:
        # jeśli sfera zachodzi pod podłogę, to podnieś ją
        if part.p[1] - part.r < 0:
            part.p[1] = part.r
            part.v[1] = - part.v[1]



def aerodynamika(v,c,graw,g):
    v = np.array(v)
    vnorm=v/np.linalg.norm(v)
    opor=v@v*c*vnorm*-1/2
    opor.tolist()
    opor[1]-=graw(0.1,opor[1],g)
    return opor

def aero(p,c,graw,g):
    x=runge2(0.1,f,p,c)
    y=runge3(0.1,f,p,c)-graw(0.1,runge3(0.1,f,p,c),g)
    z=runge4(0.1,f,p,c)
    vk=[x,y,z]
    print(vk)
    return vk

def f(x,y,z,m,c):
    vz=z/(np.sqrt(x**2+y**2+z**2))
    return 1/m*(np.sqrt(x**2+y**2+z**2)*c*(-1/2)*vz)

def runge2(h,f,p,c):
    k1=h*f(p.v[0],p.v[1],p.v[2],p.m,c)
    k2=h*f(p.v[0]+k1/2,p.v[1],p.v[2],p.m,c)
    k3=h*f(p.v[0]+k2/2,p.v[1],p.v[2],p.m,c)
    k4=h*f(p.v[0]+k3,p.v[1],p.v[2],p.m,c)
    return f(p.v[0],p.v[1],p.v[2],p.m,c) +1/6*(k1+2*k2+2*k3+k4)

def runge3(h,f,p,c):
    k1=h*f(p.v[0],p.v[1],p.v[2],p.m,c)
    k2=h*f(p.v[0],p.v[1]+k1/2,p.v[2],p.m,c)
    k3=h*f(p.v[0],p.v[1]+k2/2,p.v[2],p.m,c)
    k4=h*f(p.v[0],p.v[1]+k3,p.v[2],p.m,c)
    return f(p.v[0],p.v[1],p.v[2],p.m,c) +1/6*(k1+2*k2+2*k3+k4)

def runge4(h,f,p,c):
    k1=h*f(p.v[0],p.v[1],p.v[2],p.m,c)
    k2=h*f(p.v[0],p.v[1],p.v[2]+k1/2,p.m,c)
    k3=h*f(p.v[0],p.v[1],p.v[2]+k2/2,p.m,c)
    k4=h*f(p.v[0],p.v[1],p.v[2]+k3,p.m,c)
    return f(p.v[0],p.v[1],p.v[2],p.m,c) +1/6*(k1+2*k2+2*k3+k4)


print(runge2(0.1,f,part1,0.02))


def gravity(m,g):
    grawitacja=m*g
    return grawitacja

def runge(h,x,a):
    k1=h*x+a
    k2=h*(x+k1/2+a)
    k3=h*(x+k2/2+a)
    k4=h*(x+k3+a)
    return x+1/6*(k1+2*k2+2*k3+k4)
# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True

k=0.94
c=8
g=9.81
rot_cam=0
cam_r=10
import random
def keyboard(bkey,x,y):
    key = bkey.decode("utf-8")
    global k,rot_cam,cam_r,part1,c,g
    if key == 'k':
        k+=0.05
    if key=='l':
        k-=0.05
    if key == "e":
        cam_r-=1
    if key == "q":
        cam_r+=1
    if key=='d':
        rot_cam+=5
    if key=='a':
        rot_cam-=5
    if key == 'y':
        if random.random()>.5:
            part1.v[0]+=15
        else:
            part1.v[2]+=15
    if key=='c':
        c+=0.5
    if key=='x':
        c-=0.5
    if key=='g':
        g+=0.5
    if key=='h':
        g-=0.5
    if key=='u':
        part1.v[1]+=10
# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global part1,k,rot_cam,cam_r,c,g
    print("współczynnik aerodynamiczny:", c)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)
    camx=sin(np.radians(rot_cam))*cam_r
    camz=cos(np.radians(rot_cam))*cam_r
    gluLookAt(camx,12,camz,0,0,0,0,1,0)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    drawScianki()
    drawFloor()
    checkSphereToSciankiCollision(part1,k)
    print("współczynnik sprężystości: ", k)
    print("siła grawitacji: ",g)

    updateSphere(part1, 0.1,aero(part1,c,runge,g))
    updateSphereCollision(part1)
    drawSphere(part1)
    glutKeyboardFunc(keyboard)
    glFlush()


glutInit()
glutInitWindowSize(600, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 05")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutIdleFunc(display)
glClearColor(1.0, 1.0, 1.0, 1.0)
glClearDepth(1.0)

# glPolygonMode(x,x)

glDepthFunc(GL_LESS)
glEnable(GL_DEPTH_TEST)
# przygotowanie oświetlenia
glEnable(GL_LIGHT0)
glLight(GL_LIGHT0, GL_POSITION, [0., 5., 5., 0.])
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
# przygotowanie sfery
part1.quad = gluNewQuadric()
gluQuadricNormals(part1.quad, GLU_SMOOTH)
glutMainLoop()
