from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import ctypes
import time

windowWidth = 800
windowHeight = 600
camx = 0.0
camy = 0.0
camz = -5.0
lookx = 0.0
looky = 0.0
lookz = 5.0
upx = 0.0
upy = 1.0
upz = 0.0
mousex = windowWidth / 2
mousey = windowHeight / 2
global stat1
kordy = []
cube_select = 0


def mouseMotion(x, y):
    global mousex, mousey
    mousex = 0 if x < 0 else windowWidth if x > windowWidth else x
    mousey = 0 if y < 0 else windowHeight if y > windowHeight else y
    pass


def mouseMouse(btn, stt, x, y):
    pass


def paint():
    # czyszczenie sceny
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # reakcja na ruch myszką
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    right = np.cross(np.array([lookx, looky, lookz]), np.array([upx, upy, upz]))
    look = np.array([lookx, looky, lookz])
    right = right / np.linalg.norm(right)
    up = np.cross(right, look)
    look -= right * 5.0 * (windowWidth / 2 - mousex) / windowWidth
    look -= up * 5.0 * (windowHeight / 2 - mousey) / windowHeight
    lookx2 = look[0]
    looky2 = look[1]
    lookz2 = look[2]
    lookx2 = lookx2 / np.linalg.norm(look)
    looky2 = looky2 / np.linalg.norm(look)
    lookz2 = lookz2 / np.linalg.norm(look)
    atx = camx + lookx2
    aty = camy + looky2
    atz = camz + lookz2
    gluLookAt(camx, camy, camz, atx, aty, atz, upx, upy, upz)
    colors = (
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1),
        (0, 0, 0),
        (1, 0, 1),
        (1, 1, 0),
        (0, 1, 1),
        (1, 0.5, 0),
        (0.5, 1, 0),
        (0.5, 1, 0.5),
        (0.5, 0, 0.5)
    )

    def Cube(mousex, mousey, color, size, cube_number):
        global kej
        glBegin(GL_QUADS)
        glColor3f(colors[color][0], colors[color][1], colors[color][2])
        # upper right -> upper left -> lower left -> lower right
        mousex = (windowWidth / 2 - mousex) / 130
        mousey = -(windowHeight / 2 - mousey) / 20
        """górna ściana"""
        glVertex3f(mousex + size, mousey + size, 1.0 - size)  # front upper right
        glVertex3f(mousex - size, mousey + size, 1.0 - size)  # front upper left
        glVertex3f(mousex - size, mousey + size, 1.0 + size)  # back upper left
        glVertex3f(mousex + size, mousey + size, 1.0 + size)  # back upper right
        """tylnia ściana"""
        glVertex3f(mousex - size, mousey + size, 1.0 + size)  # back upper left
        glVertex3f(mousex + size, mousey + size, 1.0 + size)  # back upper right
        glVertex3f(mousex + size, mousey - size, 1.0 + size)  # back lower right
        glVertex3f(mousex - size, mousey - size, 1.0 + size)  # back lower left
        """dolna ściana"""
        glVertex3f(mousex + size, mousey - size, 1.0 + size)  # back lower right
        glVertex3f(mousex - size, mousey - size, 1.0 + size)  # back lower left
        glVertex3f(mousex - size, mousey - size, 1.0 - size)  # front lower left
        glVertex3f(mousex + size, mousey - size, 1.0 - size)  # fron lower right
        """przednia ściana"""
        glVertex3f(mousex + size, mousey - size, 1.0 - size)  # front lower right
        glVertex3f(mousex - size, mousey - size, 1.0 - size)  # front lower left
        glVertex3f(mousex - size, mousey + size, 1.0 - size)  # front upper left
        glVertex3f(mousex + size, mousey + size, 1.0 - size)  # front upper right
        """lewa ściana"""
        glVertex3f(mousex + size, mousey + size, 1.0 - size)  # front upper right
        glVertex3f(mousex + size, mousey - size, 1.0 - size)  # front lower right
        glVertex3f(mousex + size, mousey - size, 1.0 + size)  # back lower right
        glVertex3f(mousex + size, mousey + size, 1.0 + size)  # back upper right
        """prawa ściana"""
        glVertex3f(mousex - size, mousey + size, 1.0 - size)  # front upper left
        glVertex3f(mousex - size, mousey - size, 1.0 - size)  # front lower left
        glVertex3f(mousex - size, mousey - size, 1.0 + size)  # back lower left
        glVertex3f(mousex - size, mousey + size, 1.0 + size)  # back upper left
        glEnd()
        text = f'Cube nr:{cube_number+1}'
        glColor3f(0, 0, 0)
        glRasterPos3f(mousex, mousey,-1.5)
        for ch in text:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ctypes.c_int(ord(ch)))
        kej = 0

        # testowe
        # glVertex3f(1.0, 1.0, 1.0) # upper right
        # glVertex3f(-1.0, 1.0, 1.0) # upper left
        # glVertex3f(-1.0, -1.0, 1.0) # lower left
        # glVertex3f(1.0, -1.0, 1.0) # lower right
        # glEnd()

    losu_losu = np.random.randint(0, 11)
    losu_losu2 = np.random.uniform(0.2, 2)

    if kej == 1:
        kordy.append((mousex, mousey, losu_losu, losu_losu2))
        # print(((windowHeight / 2 - mousey)/20))

    for i in range(len(kordy)):
        Cube(kordy[i][0], kordy[i][1], kordy[i][2], kordy[i][3],i)




##################### ZMIANY PO ITERACJI HERE

    text = f'Select cube:{cube_select}'
    glColor3f(0, 0, 0)
    glRasterPos3f(0, 2,-2.5)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ctypes.c_int(ord(ch)))

    text = f'Change cube: +/-'
    glColor3f(0, 0, 0)
    glRasterPos3f(0, 2,-2.4)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ctypes.c_int(ord(ch)))
    text = f'Change color: k | Delete cube: l'
    glColor3f(0, 0, 0)
    glRasterPos3f(0, 2,-2.3)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_10, ctypes.c_int(ord(ch)))



    # # zielony prostokąt
    # glColor3f(0.0, 1.0, 0.0)
    # glBegin(GL_QUADS)
    # glVertex(2.0, 0.0, 0.0)
    # glVertex(3.0, 0.0, 0.0)
    # glVertex(3.0, 1.0, 0.0)
    # glVertex(2.0, 1.0, 0.0)
    # glEnd()
    # # niebieski wielokąt
    # glColor3f(0.0, 0.0, 1.0)
    # glBegin(GL_QUADS)
    # glVertex(-3.0, 0.0, 0.0)
    # glVertex(-2.0, 1.0, 0.0)
    # glVertex(-3.0, 2.0, 0.0)
    # glVertex(-4.0, 2.0, 0.0)
    # glVertex(-4.0, 1.0, 0.0)
    # glEnd()
    # celownik
    glColor(0.0, 0.0, 0.0)
    glPushMatrix()
    glLoadIdentity()
    gluLookAt(0.0, 0.0, -2.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-0.2, 0.0)
    glVertex2f(-0.1, 0.0)
    glVertex2f(0.0, -0.2)
    glVertex2f(0.0, -0.1)
    glVertex2f(0.2, 0.0)
    glVertex2f(0.1, 0.0)
    glVertex2f(0.0, 0.2)
    glVertex2f(0.0, 0.1)

    glEnd()
    glPopMatrix()

    glutSwapBuffers()
    pass

kej = 0
##############################
def color_cube(cube_select):
    if cube_select <= 0:
        pass
    elif cube_select > len(kordy):
        pass
    else:
        kolorki = np.random.uniform(0,11)
        kordy[cube_select-1] = list(kordy[cube_select-1])
        kordy[cube_select-1][2] = int(kolorki)
        kordy[cube_select-1] = tuple(kordy[cube_select-1])

def del_cube(cube_select):
    if cube_select <= 0:
        pass
    elif cube_select > len(kordy):
        pass
    else:
        kolorki = np.random.uniform(0,11)
        kordy[cube_select-1] = list(kordy[cube_select-1])
        del kordy[cube_select-1]

def keyboard(bkey, x, y):
    global mousex
    global lookz
    global mousey
    global kej
    global cube_select
    key = bkey.decode("utf-8")
    if key == 'd':
        mousex += 10
    elif key == 'a':
        mousex -= 10
    elif key == 'w':
        mousey += 5
    elif key == 's':
        mousey -= 5
    elif key == '+':
        if cube_select >= len(kordy):
            pass
        else:
            cube_select += 1
    elif key == '-':
        if cube_select < 1:
            pass
        else:
            cube_select -= 1
    elif key == 'k':
        color_cube(cube_select)
    elif key == 'l':
        del_cube(cube_select)
    elif key == '1':
        kej = 1
        # ESC HERE
    elif key == '\x1b':
        sys.exit()
    elif kej == '':
        kej = 0


##############################

while True:
    # utworzenie okna
    glutInit(sys.argv)
    glutInitWindowPosition(int((ctypes.windll.user32.GetSystemMetrics(0) - windowWidth) / 2),
                           int((ctypes.windll.user32.GetSystemMetrics(1) - windowHeight) / 2))
    glutInitWindowSize(windowWidth, windowHeight)
    glutCreateWindow(b"PyOpenGL")
    # konfiguracja opengl
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutIdleFunc(paint)
    glutDisplayFunc(paint)
    glutMouseFunc(mouseMouse)
    glutMotionFunc(mouseMotion)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glEnable(GL_PROGRAM_POINT_SIZE)
    glPointSize(5.0)
    # przygotowanie sceny
    glClearColor(1.0, 1.0, 1.0, 0.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, float(windowWidth / windowHeight), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    # pętla programu
    glutKeyboardFunc(keyboard)
    glutMainLoop()
