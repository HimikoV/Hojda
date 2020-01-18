
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

def mTetra(a, b, c, d, col1, col2, col3, col4):
    tetra = [];
    face = [a, b, c, col1];
    tetra.append(face);
    face = [a, b, d, col2];
    tetra.append(face);
    face = [b, c, d, col3];
    tetra.append(face);
    face = [c, a, d, col4];
    tetra.append(face);
    return tetra;


# deklaracje czworościanów (wierzchołki i kolory ścian)
tetra1 = mTetra([0, 0, 0], [2, 0, 0], [0, 2, 0], [1, 1, 2],
                [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1]);



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






def mTetra(a, b, c, d, col1, col2, col3, col4):
    tetra = [];
    face = [a, b, c, col1];
    tetra.append(face);
    face = [a, b, d, col2];
    tetra.append(face);
    face = [b, c, d, col3];
    tetra.append(face);
    face = [c, a, d, col4];
    tetra.append(face);
    return tetra;


# deklaracje czworościanów (wierzchołki i kolory ścian)
tetra1 = mTetra([1, 5, 1], [3, 5, 1], [1, 8, 1], [2, 7, 3],
                [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1]);

# rysowanie listy trójkątów
def dFacelist(flist):
    for face in flist:
        glColor3fv(face[3]);
        glBegin(GL_POLYGON)
        glVertex3fv(face[0]);
        glVertex3fv(face[1]);
        glVertex3fv(face[2]);
        glEnd();




# rysowanie podłogi
def drawFloor():
    glLoadIdentity()
    glColor3fv([0.0, 0.0, 0.0])
    glPolygonMode(GL_FRONT, GL_FILL)

    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -14])
    glVertex3fv([-10, 0, 14])
    glVertex3fv([10, 0, 14])
    glVertex3fv([10, 0, -14])
    glEnd()


def drawScianki():
    glLoadIdentity()  # jedno sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, -14])
    glVertex3fv([-10, 2, -14])
    glVertex3fv([-10, 2, 14])
    glVertex3fv([-10, 0, 14])
    glEnd()

    glLoadIdentity()  # drugo sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([-10, 0, 14])
    glVertex3fv([-10, 2, 14])
    glVertex3fv([10, 2, 14])
    glVertex3fv([10, 0, 14])
    glEnd()

    glLoadIdentity()  # trzecio sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([10, 0, 14])
    glVertex3fv([10, 2, 14])
    glVertex3fv([10, 2, -14])
    glVertex3fv([10, 0, -14])
    glEnd()

    glLoadIdentity()  # czwarto sciano
    glColor3fv([0.3, 0.3, 0.3])
    glPolygonMode(GL_FRONT, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex3fv([10, 0, -14])
    glVertex3fv([10, 2, -14])
    glVertex3fv([-10, 2, -14])
    glVertex3fv([-10, 0, -14])
    glEnd()


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick
    ltime = time.clock()
    if ltime < tick + 0.1:  # max 10 ramek / s
        return False
    tick = ltime
    return True



rot_cam=0
cam_r=20
def keyboard(bkey, x, y):
    key = bkey.decode("utf-8")
    global k, rot_cam, cam_r, part1, c, g,metin2,mousex,mousey,moc
    if key == "e":
        cam_r -= 1
    if key == "q":
        cam_r += 1
    if key == 'd':
        rot_cam += 5
    if key == 'a':
        rot_cam -= 5





# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global part1,rot_cam,cam_r

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
    dFacelist(tetra1)

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

glutMainLoop()
