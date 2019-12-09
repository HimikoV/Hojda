from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time
import numpy as np
from pyrr import Vector3, Matrix44, vector, vector3

## zmienne pomocnicze
pointSize = 10
windowSize = 150
clearColor = [0.0, 0.0, 0.0]

pixelMapR = [[clearColor[0] for y in range(windowSize)] for x in range(windowSize)]
pixelMapG = [[clearColor[1] for y in range(windowSize)] for x in range(windowSize)]
pixelMapB = [[clearColor[2] for y in range(windowSize)] for x in range(windowSize)]


class OP:  # parametry projekcji,
    l = -10
    r = 16
    b = -10
    t = 15
    n = 8
    f = 100


def clearMap(color):
    global pixelMapR, pixelMapG, pixelMapB
    for i in range(windowSize):
        for j in range(windowSize):
            pixelMapR[i][j] = color[0]
            pixelMapG[i][j] = color[1]
            pixelMapB[i][j] = color[2]


## funkcja rysująca zawartość macierzy pixelMap
def paint():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    for i in range(windowSize):
        for j in range(windowSize):
            glColor3f(pixelMapR[i][j], pixelMapG[i][j], pixelMapB[i][j])
            glVertex2f(0.5 + 1.0 * i, 0.5 + 1.0 * j)
    glEnd()
    glFlush()


## inicjalizacja okna
glutInit()
glutInitWindowSize(windowSize * pointSize, windowSize * pointSize)
glutInitWindowPosition(0, 0)
glutCreateWindow(b"Lab04")
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


def cupdate(step=0.1):
    global tick
    ltime = time.clock()
    if ltime < tick + step:
        return False
    tick = ltime
    return True


def odcinek(x1, y1, x2, y2, R, G, B):  # odcinek w 2d
    global pixelMapR
    global pixelMapG
    global pixelMapB
    if x2 == x1 and y2 == y1:
        x1 = round(x1)
        y1 = round(y1)
        if 0 <= x1 < windowSize:
            if 0 <= y1 < windowSize:
                pixelMapR[x1][y1] = R
                pixelMapR[x1][y1] = G
                pixelMapR[x1][y1] = B
        return
    ony = False
    d1 = None
    d2 = None
    if x2 == x1:
        d2 = 0
    elif y2 == y1:
        d1 = 0
    else:
        d2 = (x2 - x1) / (y2 - y1)
        if not -1 < d2 < 1:
            d1 = 1 / d2
    if d1 is not None:
        d = d1
        if x1 > x2:
            xtmp = x1
            x1 = x2
            x2 = xtmp
            ytmp = y1
            y1 = y2
            y2 = ytmp
        y = y1 - d
        for x in range(round(x1), round(x2) + 1):
            y = y + d
            dcx = x
            dcy = round(y)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMapR[dcx][dcy] = R
                    pixelMapG[dcx][dcy] = G
                    pixelMapB[dcx][dcy] = B
    else:
        d = d2
        if y1 > y2:
            xtmp = x1
            x1 = x2
            x2 = xtmp
            ytmp = y1
            y1 = y2
            y2 = ytmp
        x = x1 - d
        for y in range(round(y1), round(y2) + 1):
            x = x + d
            dcy = y
            dcx = round(x)
            if 0 <= dcx < windowSize:
                if 0 <= dcy < windowSize:
                    pixelMapR[dcx][dcy] = R
                    pixelMapG[dcx][dcy] = G
                    pixelMapB[dcx][dcy] = B


def punkt(x, y, R, G, B):  # punkt w 2d
    global pixelMapR, pixelMapG, pixelMapB
    if 0 <= x <= windowSize:
        if 0 <= y <= windowSize:
            pixelMapR[x][y] = R
            pixelMapG[x][y] = G
            pixelMapB[x][y] = B


def ortho(p, l, r, b, t, n, f):  # projekcja perspektywiczna
    ret = [2 * ((p[0] * n - r * p[2]) / (r * p[2] - l * p[2])) + 1,
           2 * ((p[1] * n - t * p[2]) / (t * p[2] - b * p[2])) + 1,
           1 - (2 * (p[2] - f) / (n - f))]
    return ret


def screen(p, width, height):  # przekształcanie na wymiary ekranu
    ret = [(width - 1) * (p[0] + 1) / 2, (height - 1) * (p[1] + 1) / 2]
    return ret


def odcinek3D(p1, p2, R, G, B):  # rysowanie odcinka w 3D
    p1o = ortho(p1, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)
    p2o = ortho(p2, OP.l, OP.r, OP.b, OP.t, OP.n, OP.f)
    p1s = screen([p1o[0], p1o[1]], windowSize, windowSize)
    p2s = screen([p2o[0], p2o[1]], windowSize, windowSize)
    odcinek(p1s[0], p1s[1], p2s[0], p2s[1], R, G, B)


def szescian(dlugoscboku, srodek, rotx, roty, rotz, R, G, B):
    pkt = [[srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku]]

    for i in range(8):
        npkt = np.matmul(np.array([[1, 0, 0], [0, np.cos(rotx), -np.sin(rotx)],
                                   [0, np.sin(rotx), np.cos(rotx)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt
    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(roty), 0, np.sin(roty)], [0, 1, 0],
                                   [-np.sin(roty), 0, np.cos(roty)]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt
    for i in range(8):
        npkt = np.matmul(np.array([[np.cos(rotz), -np.sin(rotz), 0],
                                   [np.sin(rotz), np.cos(rotz), 0], [0, 0, 1]]), np.array(pkt[i]).transpose())
        npkt = npkt.tolist()
        pkt[i] = npkt

    odcinek3D(pkt[0], pkt[1], R, G, B)
    odcinek3D(pkt[1], pkt[2], R, G, B)
    odcinek3D(pkt[2], pkt[3], R, G, B)
    odcinek3D(pkt[3], pkt[0], R, G, B)
    odcinek3D(pkt[4], pkt[5], R, G, B)
    odcinek3D(pkt[5], pkt[6], R, G, B)
    odcinek3D(pkt[6], pkt[7], R, G, B)
    odcinek3D(pkt[7], pkt[4], R, G, B)
    odcinek3D(pkt[0], pkt[4], R, G, B)
    odcinek3D(pkt[1], pkt[5], R, G, B)
    odcinek3D(pkt[2], pkt[6], R, G, B)
    odcinek3D(pkt[3], pkt[7], R, G, B)


"""cos do kamery"""


def get_view_matrix():
    return look_at(camera_pos, camera_pos + camera_front, camera_up)


"""kamera"""


def look_at(position, target, world_up):
    # 1.Position = known
    # 2.Calculate cameraDirection
    zaxis = vector.normalise(position - target)
    # 3.Get positive right axis vector
    xaxis = vector.normalise(vector3.cross(vector.normalise(world_up), zaxis))
    # 4.Calculate the camera up vector
    yaxis = vector3.cross(zaxis, xaxis)

    # create translation and rotation matrix
    translation = Matrix44.identity()
    translation[3][0] = -position.x
    translation[3][1] = -position.y
    translation[3][2] = -position.z

    rotation = Matrix44.identity()
    rotation[0][0] = xaxis[0]
    rotation[1][0] = xaxis[1]
    rotation[2][0] = xaxis[2]
    rotation[0][1] = yaxis[0]
    rotation[1][1] = yaxis[1]
    rotation[2][1] = yaxis[2]
    rotation[0][2] = zaxis[0]
    rotation[1][2] = zaxis[1]
    rotation[2][2] = zaxis[2]

    return translation * rotation


""" obrot, nie wiem jak to ustawic zeby dzialalo wokol krawedzi figury"""
def obrot_zad_2(p0, wektor, punkt, kat):
    jednostkowy = np.sqrt(wektor[0] ** 2 + wektor[1] ** 2 + wektor[2] ** 2)

    if jednostkowy != 1:
        wersor = wektor / jednostkowy
    wersor = np.array(wersor)
    M=[[wersor[0]**2*(1-np.cos(kat))+np.cos(kat),wersor[0]*wersor[1]*(1-np.cos(kat)-wersor[2]*np.sin(kat)),wersor[0]*wersor[2]*(1-np.cos(kat))+wersor[1]*np.sin(kat)],
       [wersor[0]*wersor[1]*(1-np.cos(kat))+wersor[2]*np.sin(kat),wersor[1]**2*(1-np.cos(kat)+np.cos(kat)),wersor[1]*wersor[2]*(1-np.cos(kat))-wersor[0]*np.sin(kat)],
       [wersor[0]*wersor[2]*(1-np.cos(kat))-wersor[1]*np.sin(kat),wersor[1]*wersor[2]*(1-np.cos(kat)+wersor[0]*np.sin(kat)),wersor[2]**2*(1-np.cos(kat))+np.cos(kat)]]

    M = np.array(M)
    punkt = np.array(punkt)
    punkt = punkt - p0
    punkt = M @ punkt.T
    punkt = punkt + np.array(p0)
    punkt = punkt.T
    # punkt=lookAt(center[0],center[1],center[2])[:3,:3]@punkt
    return punkt


def punkt_zad_1(p, R, G, B):
    odcinek3D(p, p, R, G, B)


def odcinek_zad_1(p, p1, R, G, B):
    odcinek3D(p, p1, R, G, B)


def trojkat_zad_1(p, p1, p2, R, G, B):
    odcinek3D(p, p1, R, G, B)
    odcinek3D(p1, p2, R, G, B)
    odcinek3D(p2, p, R, G, B)


def prostokat_zad_1(p, p1, R, G, B):
    odcinek3D(p, [p1[0], p[1], p1[2]], R, G, B)
    odcinek3D(p, [p[0], p1[1], p[2]], R, G, B)
    odcinek3D(p1, [p[0], p1[1], p[2]], R, G, B)
    odcinek3D(p1, [p1[0], p[1], p1[2]], R, G, B)


def cam_trans(p, tx, ty, tz):
    cam_t = [[1, 0, 0, tx],
             [0, 1, 0, ty],
             [0, 0, 1, tz],
             [0, 0, 0, 1]]
    p = [p[0], p[1], p[2], 1]
    xd = np.matmul(cam_t, p)
    return xd


"""PROSTOPADLOSCIAN"""
def prostopadloscian_zad_1(dlugoscbokuA, dlugoscbokuB, dlugoscbokuC, psrodek, kat, wersor, p0, R, G, B, x1, x2,x3):
    pkt = [[psrodek[0] - dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] - dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] - dlugoscbokuC],
           [psrodek[0] - dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] + dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] - dlugoscbokuB, psrodek[2] + dlugoscbokuC],
           [psrodek[0] + dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] + dlugoscbokuC],
           [psrodek[0] - dlugoscbokuA, psrodek[1] + dlugoscbokuB, psrodek[2] + dlugoscbokuC]]
    # print(np.array(pkt[3]) - np.array(pkt[0]))

    for i in range(8):
        pkt[i] = obrot_zad_2(p0, wersor, pkt[i], kat).tolist()

    for i in range(8):
        npkt = cam_trans(pkt[i], x1, x2, x3)
        npkt = npkt.tolist()
        pkt[i] = npkt

    odcinek3D(pkt[0], pkt[1], R, G, B)
    odcinek3D(pkt[1], pkt[2], R, G, B)
    odcinek3D(pkt[2], pkt[3], R, G, B)
    odcinek3D(pkt[0], pkt[3], R, G, B)
    odcinek3D(pkt[4], pkt[5], R, G, B)
    odcinek3D(pkt[5], pkt[6], R, G, B)
    odcinek3D(pkt[6], pkt[7], R, G, B)
    odcinek3D(pkt[4], pkt[7], R, G, B)
    odcinek3D(pkt[0], pkt[4], R, G, B)
    odcinek3D(pkt[1], pkt[5], R, G, B)
    odcinek3D(pkt[2], pkt[6], R, G, B)
    odcinek3D(pkt[3], pkt[7], R, G, B)


"""SZSCIAN MORDKO"""


def szescian_zad_1(dlugoscboku, srodek, kat, wersor, p0, R, G, B, x1, x2,x3):
    pkt = [[srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] - dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] - dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] + dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku],
           [srodek[0] - dlugoscboku, srodek[1] + dlugoscboku, srodek[2] + dlugoscboku]]

    print(np.array(pkt[1]) - np.array(pkt[0]))

    for i in range(8):
        pkt[i] = obrot_zad_2(p0, wersor, pkt[i], kat).tolist()

    for i in range(8):
        npkt = cam_trans(pkt[i], x1, x2, x3)
        npkt = npkt.tolist()
        pkt[i] = npkt

    odcinek3D(pkt[0], pkt[1], R, G, B)
    odcinek3D(pkt[1], pkt[2], R, G, B)
    odcinek3D(pkt[2], pkt[3], R, G, B)
    odcinek3D(pkt[3], pkt[0], R, G, B)
    odcinek3D(pkt[4], pkt[5], R, G, B)
    odcinek3D(pkt[5], pkt[6], R, G, B)
    odcinek3D(pkt[6], pkt[7], R, G, B)
    odcinek3D(pkt[7], pkt[4], R, G, B)
    odcinek3D(pkt[0], pkt[4], R, G, B)
    odcinek3D(pkt[1], pkt[5], R, G, B)
    odcinek3D(pkt[2], pkt[6], R, G, B)
    odcinek3D(pkt[3], pkt[7], R, G, B)


kej = 0
param = 0
x1 = x2 = x3 = 0
decisionholder=False

def keyboard(bkey, x, y):
    global kej
    global x1
    global decisionholder
    global x2
    global x3
    global param
    global rotationx
    key = bkey.decode("utf-8")
    if key == '1':
        kej = 1
    elif key == '2':
        kej = 2
    elif key == '3':
        kej = 3
    elif key == '4':
        kej = 4
    elif key == '5':
        kej = 5
    elif key == 'q':
        sys.exit()

    # PARAMETRY HERE
    elif key == '+':
        param = 1
    elif key == '-':
        param = 2
    elif key == 'z':
        if param == 1:
            OP.l += 1
        elif param == 2:
            OP.l -= 1
    elif key == 'x':
        if param == 1:
            OP.r += 1
        elif param == 2:
            OP.r -= 1
    elif key == 'c':
        if param == 1:
            OP.b += 1
        elif param == 2:
            OP.b -= 1
    elif key == 'v':
        if param == 1:
            OP.t += 1
        elif param == 2:
            OP.t -= 1
    elif key == 'b':
        if param == 1:
            OP.n += 1
        elif param == 2:
            OP.n -= 1
    elif key == 'n':
        if param == 1:
            OP.f += 1
        elif param == 2:
            OP.f -= 1
    elif key == 'l':
        rotationx += 0.1
    elif key == '0':
        kej = 0
    elif key == 'd':
        x1 -= 1
    elif key == 'w':
        x2 -= 1
    elif key == 's':
        x2 += 1
    elif key == 'a':
        x1 += 1
    elif key == 'e':
        x3 += 1
    elif key == 'r':
        x3 -= 1
    elif key=='t':
        decisionholder=True
    elif key=='y':
        decisionholder=False


kat = 0
while True:
    clearMap([0.0, 0.0, 0.0])
    glutKeyboardFunc(keyboard)
    if kej == 1:
        punkt_zad_1([2, 2, 30], 1, 1, 1)
    elif kej == 2:
        odcinek_zad_1([2, 2, 30], [5, 5, 40], 1, 1, 1)
    elif kej == 3:
        trojkat_zad_1([2, 2, 30], [4, 4, 40], [4, 2, 50], 1, 1, 1)
    elif kej == 4:
        prostokat_zad_1([2, 2, 30], [5, 8, 40], 1, 1, 1)
    elif kej == 5:
        prostopadloscian_zad_1(3, 5, 7, [2, 2, 30], kat, [6, 2, 6], [0, 1, 1], 1, 1, 1, x1, x2,x3)
    # szescian_zad_1(3, [0, 0, 15], kat, [12,5,3], [6,3,1], 1.0, 1.0, 1.0, x1, x2,x3)
    prostopadloscian_zad_1(3, 5, 7, [15, 12, 30], kat,[0,6,0], [12,7,23], 1, 1, 1, x1, x2,x3)
    szescian_zad_1(5, [17, 3, 12], kat, [6,6,6], [16,2,11], 1.0, 1.0, 1.0, x1, x2,x3)
    if decisionholder==True:
        kat += 0.1
    paint()
    glutMainLoopEvent()
