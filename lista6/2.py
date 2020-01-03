from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time;
import numpy as np

# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0;


# klasa pomocnicza, pozwalająca na odwoływanie się do słowników przez notację kropkową
class dd(dict):
    __getattr__ = dict.get;
    __setattr__ = dict.__setitem__;
    __delattr__ = dict.__delitem__;


# trojkaty
tri1 = {"a": [-4.0, 0.0], "b": [-2.0, 0.0], "c": [-1.0, 2.0],
        "col": [1, 0, 0]};
tri1 = dd(tri1);
tri1.center = [(tri1.a[0] + tri1.b[0] + tri1.c[0]) / 3,
               (tri1.a[1] + tri1.b[1] + tri1.c[1]) / 3]
tri2 = {"a": [-4.0, -4.0], "b": [-2.0, -6.0], "c": [-0.0, -0.0],
        "col": [0, 0, 1]};
tri2 = dd(tri2);
tri2.center = [(tri2.a[0] + tri2.b[0] + tri2.c[0]) / 3,
               (tri2.a[1] + tri2.b[1] + tri2.c[1]) / 3];
tri3 = {"a": [4.0, 4.0], "b": [2.0, 6.0], "c": [1.0, 1.0],
        "col": [0, 1, 1]};
tri3 = dd(tri3);
tri3.center = [(tri3.a[0] + tri3.b[0] + tri3.c[0]) / 3,
               (tri3.a[1] + tri3.b[1] + tri3.c[1]) / 3];

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
# Return true if line segments AB and CD intersect
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def triColDet(a, b, c, center, aa, bb, cc, center2):
    area = np.abs((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))
    ph = [np.sqrt((aa[0] - center[0]) ** 2 + (aa[1] - center[1]) ** 2),
          np.sqrt((bb[0] - center[0]) ** 2 + (bb[1] - center[1]) ** 2),
          np.sqrt((cc[0] - center[0]) ** 2 + (cc[1] - center[1]) ** 2)]
    ph1 = [aa, bb, cc]
    p = ph1[ph.index(min(ph))]
    area1 = np.abs((a[0] - p[0]) * (b[1] - p[1]) - (b[0] - p[0]) * (a[1] - p[1]))
    area2 = np.abs((b[0] - p[0]) * (c[1] - p[1]) - (c[0] - p[0]) * (b[1] - p[1]))
    area3 = np.abs((c[0] - p[0]) * (a[1] - p[1]) - (a[0] - p[0]) * (c[1] - p[1]))
    if (area1 + area2 + area3) != area and not(intersect(a,b,aa,bb)) and not(intersect(a,b,bb,cc)) and not(intersect(a,b,cc,aa)) and not(intersect(b,c,aa,bb)) and not(intersect(b,c,bb,cc)) and not(intersect(b,c,cc,aa)) and not(intersect(c,a,aa,bb)) and not(intersect(c,a,bb,cc)) and not(intersect(c,a,cc,aa)):
        return 0
    return 1;

# funkcja rysująca trójkąt w 2d
def dtri2f(a, b, c, col):
    glColor3fv(col);
    glBegin(GL_POLYGON);
    glVertex2fv(a);
    glVertex2fv(b);
    glVertex2fv(c);
    glEnd();

# obsługa klawiatury
def keypress(key, x, y):
    global tri3;
    if key == b"a": tri3.a[0] -= 0.1; tri3.b[0] -= 0.1; tri3.c[0] -= 0.1;
    if key == b"d": tri3.a[0] += 0.1; tri3.b[0] += 0.1; tri3.c[0] += 0.1;
    if key == b"w": tri3.a[1] += 0.1; tri3.b[1] += 0.1; tri3.c[1] += 0.1;
    if key == b"s": tri3.a[1] -= 0.1; tri3.b[1] -= 0.1; tri3.c[1] -= 0.1;
    tri3.center = [(tri3.a[0] + tri3.b[0] + tri3.c[0]) / 3,
                   (tri3.a[1] + tri3.b[1] + tri3.c[1]) / 3];
    if key == b"q": tri3 = rotTri(tri3, 0.1);
    if key == b"e": tri3 = rotTri(tri3, -0.1);

# rotacja trójkąta (uwaga: deformacja przy każdym uruchomieniu)
def rotTri(tri, rot):
    nx = cos(rot) * (tri.a[0] - tri.center[0]) - sin(rot) * (tri.a[1] - tri.center[1]) + tri.center[0];
    ny = sin(rot) * (tri.a[0] - tri.center[0]) + cos(rot) * (tri.a[1] - tri.center[1]) + tri.center[1];
    tri.a[0] = nx;
    tri.a[1] = ny;
    nx = cos(rot) * (tri.b[0] - tri.center[0]) - sin(rot) * (tri.b[1] - tri.center[1]) + tri.center[0];
    ny = sin(rot) * (tri.b[0] - tri.center[0]) + cos(rot) * (tri.b[1] - tri.center[1]) + tri.center[1];
    tri.b[0] = nx;
    tri.b[1] = ny;
    nx = cos(rot) * (tri.c[0] - tri.center[0]) - sin(rot) * (tri.c[1] - tri.center[1]) + tri.center[0];
    ny = sin(rot) * (tri.c[0] - tri.center[0]) + cos(rot) * (tri.c[1] - tri.center[1]) + tri.center[1];
    tri.c[0] = nx;
    tri.c[1] = ny;
    return tri;

# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick;
    ltime = time.clock();
    if (ltime < tick + 0.1):  # max 10 ramek / s
        return False;
    tick = ltime;
    return True;

# pętla wyświetlająca
def display():
    if not cupdate():
        return;
    global tri1, tri2, tri3;
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    dtri2f(tri3.a, tri3.b, tri3.c, tri3.col);
    dtri2f(tri2.a, tri2.b, tri2.c, tri2.col);
    dtri2f(tri1.a, tri1.b, tri1.c, tri1.col);
    tri2 = rotTri(tri2, 0.1);
    txt = "-";
    if triColDet(tri1.a, tri1.b, tri1.c, tri1.center, tri2.a, tri2.b, tri2.c, tri2.center) or triColDet(tri2.a, tri2.b, tri2.c, tri2.center, tri1.a, tri1.b, tri1.c, tri1.center):
        txt += "tri1 x tri2, ";
    if triColDet(tri1.a, tri1.b, tri1.c, tri1.center, tri3.a, tri3.b, tri3.c, tri3.center) or triColDet(tri3.a, tri3.b, tri3.c, tri3.center, tri1.a, tri1.b, tri1.c, tri1.center):
        txt += "tri1 x tri3, ";
    if triColDet(tri3.a, tri3.b, tri3.c, tri3.center, tri2.a, tri2.b, tri2.c, tri2.center) or triColDet(tri2.a, tri2.b, tri2.c, tri2.center, tri3.a, tri3.b, tri3.c, tri3.center):
        txt += "tri2 x tri3, ";

    txt += "\n";
    sys.stdout.write(txt);
    glFlush();

glutInit();
glutInitWindowSize(600, 600);
glutInitWindowPosition(0, 0);
glutCreateWindow(b"Kolizje 02");
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
glutDisplayFunc(display);
glutIdleFunc(display);
glutKeyboardFunc(keypress);
glClearColor(1.0, 1.0, 1.0, 1.0);
glClearDepth(1.0);
glDepthFunc(GL_LESS);
glEnable(GL_DEPTH_TEST);
# ustaw projekcję ortograficzną
glMatrixMode(GL_PROJECTION);
glLoadIdentity();
glOrtho(-10, 10, -10, 10, 15, 20);
gluLookAt(0.0, 0.0, 15.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
glMatrixMode(GL_MODELVIEW);
glutMainLoop();
