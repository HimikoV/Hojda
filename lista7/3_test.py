# LISTA 7
# ZAD 3
# 1.1...DONE
# 1.2...DONE
# 1.3...DONE
# 1.4...
# 1.5...
# 1.6...

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import *
import time
import numpy as np

# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0
windowWidth = 800
windowHeight = 600
mousex = windowWidth / 2
mousey = windowHeight / 2


# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


quadratic = gluNewQuadric()

part1 = {}
part1 = dd(part1)
part1.v = [-5, 0, 5]
part1.p = [2, 1, 3]
part1.m = 10
part1.r = 1
part1.col = [0, 0.5, 1]
part1.quad = quadratic

part2 = {}
part2 = dd(part2)
part2.v = [-3, 0, 2]
part2.p = [-5, 1, 10]
part2.m = 10
part2.r = 1
part2.col = [1, 0, 0.5]
part2.quad = quadratic

part3 = {}
part3 = dd(part3)
part3.v = [4, 0, 4]
part3.p = [-5, 1, -5]
part3.m = 10
part3.r = 1
part3.col = [1, 1, 1]
part3.quad = quadratic

colors = np.array(
    [[1, 0, 0],
     [0, 1, 0],
     [0, 0, 1],
     [0, 0, 0],
     [1, 0, 1],
     [1, 1, 0],
     [0, 1, 1],
     [1, 0.5, 0],
     [0.5, 1, 0],
     [0.5, 1, 0.5],
     [0.5, 0, 0.5]])


def mouseMotion(x, y):
    global mousex, mousey
    mousex = 0 if x < 0 else windowWidth if x > windowWidth else x
    mousey = 0 if y < 0 else windowHeight if y > windowHeight else y
    pass


def mouseMouse(btn, stt, x, y):
    pass


# rysowanie sfery
def drawSphere(part):
    glLoadIdentity()
    glPolygonMode(GL_FRONT, GL_FILL)

    glTranslatef(part.p[0], part.p[1], part.p[2])
    glColor3fv(part.col)
    gluSphere(part.quad, part.r, 16, 16)


def rotejszyn(part, mousex, mousey):
    mousex = (windowWidth / 2 - mousex)
    mousey = (windowHeight / 2 - mousey)
    glTranslatef(part.p[0], part.p[1], part.p[2])
    glRotatef(mousex, 0, 0.5, 0)
    glTranslatef(-part.p[0], -part.p[1], -part.p[2])

def hitAnimejszyn(part):
    if metin2%2 == 0:
       glTranslatef(0, 0, -4)
    else:
        glTranslatef(0, 0, 0)


def kijekPrawdy(part, mousex, mousey):
    glLoadIdentity()
    rotejszyn(part, mousex, mousey)
    hitAnimejszyn(part)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glTranslatef(part.p[0], part.p[1], part.p[2] - 1.5)
    gluSphere(part.quad, 0.3, 16, 16)


    glLoadIdentity()
    rotejszyn(part, mousex, mousey)
    hitAnimejszyn(part)
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([part.p[0] - 0.3, part.p[1] + 0.3, part.p[2]- 1.5])
    glVertex3fv([part.p[0] - 0.3, part.p[1] + 0.3, part.p[2] - 1.5])
    glVertex3fv([part.p[0] + 0.3, part.p[1] + 0.3, part.p[2] - 1.5])
    glVertex3fv([part.p[0] + 0.3, part.p[1] + 0.3, part.p[2]- 1.5])
    glEnd()

    glLoadIdentity()
    rotejszyn(part, mousex, mousey)
    hitAnimejszyn(part)
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([part.p[0] + 0.3, part.p[1] - 0.3, part.p[2]- 1.5])
    glVertex3fv([part.p[0] + 0.3, part.p[1] - 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] + 0.3, part.p[1] + 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] + 0.3, part.p[1] + 0.3, part.p[2]- 1.5])
    glEnd()

    glLoadIdentity()
    rotejszyn(part, mousex, mousey)
    hitAnimejszyn(part)
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([part.p[0] - 0.3, part.p[1] - 0.3, part.p[2]- 1.5])
    glVertex3fv([part.p[0] - 0.3, part.p[1] - 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] - 0.3, part.p[1] + 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] - 0.3, part.p[1] + 0.3, part.p[2]- 1.5])
    glEnd()

    glLoadIdentity()
    rotejszyn(part, mousex, mousey)
    hitAnimejszyn(part)
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([part.p[0] - 0.3, part.p[1] - 0.3, part.p[2]- 1.5])
    glVertex3fv([part.p[0] - 0.3, part.p[1] - 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] + 0.3, part.p[1] - 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] + 0.3, part.p[1] - 0.3, part.p[2]- 1.5])
    glEnd()

    glLoadIdentity()
    rotejszyn(part, mousex, mousey)
    hitAnimejszyn(part)
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([part.p[0] - 0.3, part.p[1] - 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] - 0.3, part.p[1] + 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] + 0.3, part.p[1] + 0.3, part.p[2] - 20])
    glVertex3fv([part.p[0] + 0.3, part.p[1] - 0.3, part.p[2] - 20])
    glEnd()

# rysowanie podłogi
def drawFloor():
    glLoadIdentity()
    glColor3fv([0.0, 1.0, 0.0])
    glPolygonMode(GL_FRONT, GL_FILL)

    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 0, 18])
    glVertex3fv([10, 0, 18])
    glVertex3fv([10, 0, -10])
    glEnd()


def drawScianki():
    glLoadIdentity()  # jedno sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -10])
    glVertex3fv([-10, 2, -10])
    glVertex3fv([-10, 2, 18])
    glVertex3fv([-10, 0, 18])
    glEnd()

    glLoadIdentity()  # drugo sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, 18])
    glVertex3fv([-10, 2, 18])
    glVertex3fv([10, 2, 18])
    glVertex3fv([10, 0, 18])
    glEnd()

    glLoadIdentity()  # trzecio sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([10, 0, 18])
    glVertex3fv([10, 2, 18])
    glVertex3fv([10, 2, -10])
    glVertex3fv([10, 0, -10])
    glEnd()

    glLoadIdentity()  # czwarto sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([10, 0, -10])
    glVertex3fv([10, 2, -10])
    glVertex3fv([-10, 2, -10])
    glVertex3fv([-10, 0, -10])
    glEnd()


# ruch sfery
def updateSphere(part, dt, aero, graw):
    # tutaj trzeba dodać obsługę sił, w tym grawitacji
    part.v[0] = part.v[0] + aero[0]
    part.v[1] = part.v[1] + aero[1] - graw
    part.v[2] = part.v[2] + aero[2]
    part.p[0] += dt * part.v[0]
    part.p[1] += dt * part.v[1]
    part.p[2] += dt * part.v[2]


def checkSphereToSciankiCollision(part, k):
    if part.p[0] - part.r < 7:
        pass
    else:
        part.p[0] = 7 + part.r
        part.v[0] = -part.v[0] * k

    if part.p[0] + part.r > -7:
        pass
    else:
        part.p[0] = -part.r - 7
        part.v[0] = -part.v[0] * k

    if part.p[2] - part.r < 15:
        pass
    else:
        part.p[2] = 15 + part.r
        part.v[2] = - part.v[2] * k

    if part.p[2] + part.r > -7:
        pass
    else:
        part.p[2] = -part.r - 7
        part.v[2] = - part.v[2] * k


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
    if not checkSphereToFloorCollision(part):
        return
    else:
        # jeśli sfera zachodzi pod podłogę, to podnieś ją
        if part.p[1] - part.r < 0:
            part.p[1] = part.r
            part.v[1] = - part.v[1]


def aerodynamika(v, c):
    v = np.array(v)
    vnorm = v / np.linalg.norm(v)
    opor = v @ v * c * vnorm * -1 / 2
    opor.tolist()
    return opor


def gravity(m, g):
    grawitacja = m * g
    return grawitacja


def colisionOvO(p1, p2):
    list1 = [p1.p[0], p1.p[2]]
    list2 = [p2.p[0], p2.p[2]]
    if np.sqrt((list1[0] - list2[0]) ** 2 + (list1[1] - list2[1]) ** 2) < 2 * part1.r:
        p1.p[0], p2.p[2] = list1[0], list1[1]
        p2.p[0], p2.p[2] = list2[0], list2[1]
        m1, m2 = p1.r ** 2, p2.r ** 2
        M = m1 + m2
        r1, r2 = np.array(p1.p), np.array(p2.p)
        d = np.linalg.norm(r1 - r2) ** 2
        v1, v2 = np.array(p1.v), np.array(p2.v)
        u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, r1 - r2) / d * (r1 - r2)
        u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, r2 - r1) / d * (r2 - r1)
        p1.v = u1
        p2.v = u2


    else:
        pass


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True


k = 0.8
c = 0.02
g = 0.5
rot_cam=0
cam_r=20
import random

metin2 = 1
def keyboard(bkey, x, y):
    key = bkey.decode("utf-8")
    global k, rot_cam, cam_r, part1, c, g,metin2,mousex,mousey
    if key == 'k':
        k += 0.05
    if key == 'l':
        k -= 0.05
    if key == "e":
        cam_r -= 1
    if key == "q":
        cam_r += 1
    if key == 'd':
        rot_cam += 5
    if key == 'a':
        rot_cam -= 5
    if key == 'y':
        x = random.random()
        if x > .67:
            part1.v[0] += random.randint(-30, 30)
            part1.v[2] += random.randint(-30, 30)
        elif x < .33:
            part2.v[0] += random.randint(-30, 30)
            part2.v[2] += random.randint(-30, 30)
        else:
            part3.v[0] += random.randint(-30, 30)
            part3.v[2] += random.randint(-30, 30)
    if key == 'c':
        c += 0.001
    if key == 'x':
        c -= 0.001
    if key == 'g':
        g += 0.001
    if key == 'h':
        g -= 0.001
    if key == '\x20':
        metin2 += 1
        if metin2 %2==1:
            print(mousex,mousey)
            mousex,mousey=abs(mousex),abs(mousey)
            predkosc=np.array([-cos(np.radians(mousex-45)),0,sin(np.radians(mousey+135    ))])
            part3.v=predkosc*20




# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global part1,k,rot_cam,cam_r,c,g
    #print("współczynnik aerodynamiczny:", c)
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
    checkSphereToSciankiCollision(part1, k)
    checkSphereToSciankiCollision(part2, k)
    checkSphereToSciankiCollision(part3, k)
    # print("współczynnik sprężystości: ", k)
    # print("siła grawitacji: ", g)
    updateSphere(part1, 0.1, aerodynamika(part1.v, c), gravity(part1.m, g))
    updateSphereCollision(part1)
    updateSphere(part2, 0.1, aerodynamika(part2.v, c), gravity(part2.m, g))
    updateSphereCollision(part2)
    updateSphere(part3, 0.1, aerodynamika(part3.v, c), gravity(part3.m, g))
    updateSphereCollision(part3)
    colisionOvO(part1, part2)
    colisionOvO(part2, part3)
    colisionOvO(part1, part3)
    kijekPrawdy(part3, mousex, mousey)
    drawSphere(part1)
    drawSphere(part2)
    drawSphere(part3)

    glutKeyboardFunc(keyboard)
    glFlush()


glutInit()
glutInitWindowSize(800, 600)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Kolizje 05")
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH)
glutDisplayFunc(display)
glutMouseFunc(mouseMouse)
glutMotionFunc(mouseMotion)
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
