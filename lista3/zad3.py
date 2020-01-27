from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import math
import numpy as np
from math import sin, cos

## zmienne pomocnicze
pointSize = 10
windowSize = 100
pixelMap = [[0.0 for y in range(windowSize)] for x in range(windowSize)]
tick = 0.0


## funkcja rysująca zawartość macierzy pixelMap
def paint():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.0, 0.0)
    for i in range(windowSize):
        for j in range(windowSize):
            glColor3f(pixelMap[i][j], 1.0, 1.0)
            glVertex2f(0.5 + 1.0 * i, 0.5 + 1.0 * j)
    glEnd()
    glFlush()

## inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize*pointSize, windowSize*pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Newlist01")
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

## inicjalizacja wyświetlania
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0.0, windowSize, 0.0, windowSize)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glutDisplayFunc(paint)
glutIdleFunc(paint)
glClearColor(1.0, 1.0, 1.0, 1.0)
glEnable(GL_PROGRAM_POINT_SIZE)
glPointSize(pointSize)


def clearMap():
    global pixelMap
    pixelMap = [[0.0 for y in range(windowSize)] for x in range(windowSize)]


def cupdate(step=0.1):
    global tick
    ltime = time.clock()
    if ltime < tick + step:
        return False
    tick = ltime
    return True


def odcinek(x1, y1, x2, y2):
    global pixelMap
    try:
        d = (y2 - y1) / (x2 - x1)  # współczynnik kierunkowy
    except ZeroDivisionError:
        d = 0
    if -1 < d < 1:
        if x1 > x2:  # rysujemy od lewej do prawej
            xtmp = x1; x1 = x2; x2 = xtmp
            ytmp = y1; y1 = y2; y2 = ytmp
        y = y1  # początkowa wartość y
        for x in range(round(x1), round(x2)+1):  # przechodzimy przez piksele od x1 do x2
            y = y + d
            dcx = x
            dcy = round(y)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMap[dcx][dcy] = 1.0
    else:
        try:
            d = (x2 - x1) / (y2 - y1)
        except ZeroDivisionError:
            d = 0
        if y1 > y2:  # rysujemy od lewej do prawej
            xtmp = x1; x1 = x2; x2 = xtmp
            ytmp = y1; y1 = y2; y2 = ytmp
        x = x1
        for y in range(round(y1), round(y2)):
            x += d
            dcx = round(x)
            dcy = round(y)
            if 0 <= dcx < windowSize and 0 <= dcy < windowSize:
                pixelMap[dcx][dcy] = 1.0


def prostokat(x, dx, dy, a):
    # Translacja
    x[0] += dx; x[2] += dx; x[4] += dx; x[6] += dx
    x[1] += dy; x[3] += dy; x[5] += dy; x[7] += dy

    # Ze stopni na radiany
    a = math.radians(a)

    # Wyznaczenie środka prostokąta wokół którego będzie następować obrót
    middlePoint = [(x[0] + x[2] + x[4] + x[6])/4, (x[1] + x[3] + x[5] + x[7])/4]

    p1 = obrotPunktu((x[0], x[1]), middlePoint, a)
    p2 = obrotPunktu((x[2], x[3]), middlePoint, a)
    p3 = obrotPunktu((x[4], x[5]), middlePoint, a)
    p4 = obrotPunktu((x[6], x[7]), middlePoint, a)

    # Rysowanie odcinków łączących punkty
    odcinek(*p1, *p2)
    odcinek(*p2, *p3)
    odcinek(*p3, *p4)
    odcinek(*p4, *p1)



def obrotPunktu(punkt, punktCentralny, a):
    nowyPunkt = [
        (punkt[0] - punktCentralny[0]) * math.cos(a) - (punkt[1] - punktCentralny[1]) * math.sin(a) + punktCentralny[0],
        (punkt[0] - punktCentralny[0]) * math.sin(a) + (punkt[1] - punktCentralny[1]) * math.cos(a) + punktCentralny[1]
    ]
    return nowyPunkt


def punkt(x, y, col):
    global pixelMap
    if 0 <= x <= windowSize:
        if 0 <= y <= windowSize:
            pixelMap[x][y] = col


def ff(x, u):
    # równanie stanu
    r = 5
    T = np.array([
        [math.cos(x[2]), 0],
        [math.sin(x[2]), 0],
        [0, 1]
    ])
    w = np.array([
        1 / 2 * (u[0] + u[1]),
        1 / r * (u[1] - u[0])
    ])
    return np.dot(T, w)


def gg(x, u):
    # wyjście obiektu
    return np.array([x[0] * 10, x[1] * 10]).transpose()


def uu(t):
    # wejście obiektu
    return np.array([t])


def rk4(f, u, x, dt):
    # Runge-Kutta 4
    k1 = dt * f(x, u)
    k2 = dt * f(x + (k1/2)/2, u)
    k3 = dt * f(x + (k2/2)/2, u)
    k4 = dt * f(x + k3, u)
    return x + dt * 1/6 * (k1 + 2*k2 + 3*k3 + k4)


def rysujRobota(x):
    robotSize = 10
    robotRadius = robotSize/2
    corners = []
    corners.append(int(x[0] + robotRadius))
    corners.append(int(x[1] + robotRadius))
    corners.append(int(x[0] + robotRadius))
    corners.append(int(x[1] - robotRadius))
    corners.append(int(x[0] - robotRadius))
    corners.append(int(x[1] - robotRadius))
    corners.append(int(x[0] - robotRadius))
    corners.append(int(x[1] + robotRadius))
    prostokat(corners, 10, 10, x[2])


# u = uu(tick)
u = [75, 75, 0]
x = np.array([windowSize/2, windowSize/2, 279]).transpose() #3 parametr, kąt obrotu
y = gg(x, u)


while True:
    if cupdate() and tick < 100:
        clearMap()
        x = rk4(ff, u, x, 0.05)
        print(x)
        y = gg(x, u)
        rysujRobota(x)
    paint()
    glutMainLoopEvent()
