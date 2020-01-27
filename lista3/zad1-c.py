from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import math

# zmienne pomocnicze
pointSize = 10
windowSize = 100
pixelMap = [[0.0 for y in range(windowSize)] for x in range(windowSize)]
tick = 0.0


# funkcja rysująca zawartość macierzy pixelMap
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


# inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize*pointSize, windowSize*pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Newlist01")
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

# inicjalizacja wyświetlania
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

    x[0] = (x[0] - middlePoint[0]) * math.cos(a) - (x[1] - middlePoint[1]) * math.sin(a) + middlePoint[0]
    x[2] = (x[2] - middlePoint[0]) * math.cos(a) - (x[3] - middlePoint[1]) * math.sin(a) + middlePoint[0]
    x[4] = (x[4] - middlePoint[0]) * math.cos(a) - (x[5] - middlePoint[1]) * math.sin(a) + middlePoint[0]
    x[6] = (x[6] - middlePoint[0]) * math.cos(a) - (x[7] - middlePoint[1]) * math.sin(a) + middlePoint[0]

    x[1] = (x[0] - middlePoint[0]) * math.sin(a) + (x[1] - middlePoint[1]) * math.cos(a) + middlePoint[1]
    x[3] = (x[2] - middlePoint[0]) * math.sin(a) + (x[3] - middlePoint[1]) * math.cos(a) + middlePoint[1]
    x[5] = (x[4] - middlePoint[0]) * math.sin(a) + (x[5] - middlePoint[1]) * math.cos(a) + middlePoint[1]
    x[7] = (x[6] - middlePoint[0]) * math.sin(a) + (x[7] - middlePoint[1]) * math.cos(a) + middlePoint[1]

    # Rysowanie odcinków łączących punkty
    odcinek(x[0], x[1], x[2], x[3])
    odcinek(x[2], x[3], x[4], x[5])
    odcinek(x[4], x[5], x[6], x[7])
    odcinek(x[6], x[7], x[0], x[1])


while True:
    if cupdate():
        '''tt = tick
        x = windowSize * math.cos(tick)
        y = windowSize * math.sin(tick)
        odcinek(windowSize/2, windowSize/2, 50 + x, 50 + y)'''
        dx1 = 10
        dx2 = 10
        rot = 150
        prostokat([15, 20, 25, 20, 20, 30, 10, 30], dx1, dx2, rot)
    paint()
    glutMainLoopEvent()