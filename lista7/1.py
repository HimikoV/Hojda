#LISTA 7
#ZAD 1
#1.1...DONE
#1.2...DONE
#1.3...DONE
#1.4...DONE
#1.5...NIE WIEM W SUMIE CZY O TO CHODZIŁO ALE INACZEJ NIE UMIAŁEM
#1.6...DONE?


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
part1.v = [3, -1, 1]
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
def updateSphere(part, dt):
    # tutaj trzeba dodać obsługę sił, w tym grawitacji
    part.p[0] += dt * part.v[0]
    part.p[1] += dt * part.v[1]
    part.p[2] += dt * part.v[2]


def checkSphereToSciankiCollision(part,k):
    if part.p[0] - part.r < 5:
        pass
    else:
        part.v[0] = -part.v[0]*k

    if part.p[0] - part.r > -8:
        pass
    else:
        part.v[0] = np.abs(part.v[0])*k

    if part.p[2] - part.r < 10:
        pass
    else:
        part.v[2] = - part.v[2]*k

    if part.p[2] - part.r > -5:
        pass
    else:
        part.v[2] = - part.v[2]*k


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


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True
k=1
import random
def keyboard(bkey,x,y):
    key = bkey.decode("utf-8")
    global k,eye, orient, up,part1
    if key == 'k':
        k+=0.05
    if key=='l':
        k-=0.05
    if key == "e":
        eye = eye + orient * np.array([0.1, 0.1, 0.1]);
    if key == "q":
        eye = eye - orient * np.array([0.1, 0.1, 0.1]);
    if key == "a":
        right = np.cross(up, orient);
        right = right / np.linalg.norm(right);
        inverse = np.array([right, up, orient]);
        inverse = np.transpose(inverse);
        rot = np.array([[np.cos(0.1), 0, np.sin(0.1)], [0, 1, 0],
                        [-np.sin(0.1), 0, np.cos(0.1)]]);
        orient = np.matmul(rot, np.array([0, 0, 1]));
        orient = np.matmul(inverse, orient);
    if key == "d":
        right = np.cross(up, orient);
        right = right / np.linalg.norm(right);
        inverse = np.array([right, up, orient]);
        inverse = np.transpose(inverse);
        rot = np.array([[np.cos(-0.1), 0, np.sin(-0.1)], [0, 1, 0],
                        [-np.sin(-0.1), 0, np.cos(-0.1)]]);
        orient = np.matmul(rot, np.array([0, 0, 1]));
        orient = np.matmul(inverse, orient);

    if key == "s":
        right = np.cross(up, orient);
        right = right / np.linalg.norm(right);
        inverse = np.array([right, up, orient]);
        inverse = np.transpose(inverse);
        rot = np.array([[1, 0, 0], [0, np.cos(0.1), -np.sin(0.1)],
                        [0, np.sin(0.1), np.cos(0.1)]]);
        orient = np.matmul(rot, np.array([0, 0, 1]));
        orient = np.matmul(inverse, orient);
        up = np.matmul(rot, np.array([0, 1, 0]));
        up = np.matmul(inverse, up);
    if key == "w":
        right = np.cross(up, orient);
        right = right / np.linalg.norm(right);
        inverse = np.array([right, up, orient]);
        inverse = np.transpose(inverse);
        rot = np.array([[1, 0, 0], [0, np.cos(-0.1), -np.sin(-0.1)],
                        [0, np.sin(-0.1), np.cos(-0.1)]]);
        orient = np.matmul(rot, np.array([0, 0, 1]));
        orient = np.matmul(inverse, orient);
        up = np.matmul(rot, np.array([0, 1, 0]));
        up = np.matmul(inverse, up);
    if key == 'y':
        part1.v[random.randint(0,2)]+=0.5
    if key=='u':
        part1.v[random.randint(0, 2)] -= 0.5
# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global part1,k,eye,orient,up
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1, 1, -1, 1, 1, 100)
    center = eye + orient;
    gluLookAt(eye[0],eye[1],eye[2],center[0],center[1],center[2],up[0],up[1],up[2])
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    drawScianki()
    drawFloor()
    checkSphereToSciankiCollision(part1,k)
    print(k)
    updateSphere(part1, 0.1)
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
