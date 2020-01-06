from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
import time;
import numpy as np;

# licznik czasu - do wymuszenia częstotliwości odświeżania
tick = 0;
# parametry kamery
eye = np.array([0., 0., 15.]);  # pozycja
orient = np.array([0., 0., -1.]);  # kierunek
up = np.array([0., 1., 0.]);  # góra




# tworzenie czworoscianów o zadanych wierzchołkach i kolorach
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
tetra2 = mTetra([3, 0, 0], [5, 0, 0], [3, 2, 0], [4, 1, 2],
                [1, 0, 0], [0, 1, 0], [1, 1, 0], [0, 1, 1]);
czworosciany = [tetra1, tetra2]
counter = 0

# rysowanie listy trójkątów
def dFacelist(flist):
    for face in flist:
        glColor3fv(face[3]);
        glBegin(GL_POLYGON)
        glVertex3fv(face[0]);
        glVertex3fv(face[1]);
        glVertex3fv(face[2]);
        glEnd();


# ruch kamery
def keypress(key, x, y):
    global eye, orient, up, counter, czworosciany;
    if key == b"e":
        eye = eye + orient * np.array([0.1, 0.1, 0.1]);
    if key == b"q":
        eye = eye - orient * np.array([0.1, 0.1, 0.1]);
    if key == b"a":
        right = np.cross(up, orient);
        right = right / np.linalg.norm(right);
        inverse = np.array([right, up, orient]);
        inverse = np.transpose(inverse);
        rot = np.array([[np.cos(0.1), 0, np.sin(0.1)], [0, 1, 0],
                        [-np.sin(0.1), 0, np.cos(0.1)]]);
        orient = np.matmul(rot, np.array([0, 0, 1]));
        orient = np.matmul(inverse, orient);
    if key == b"d":
        right = np.cross(up, orient);
        right = right / np.linalg.norm(right);
        inverse = np.array([right, up, orient]);
        inverse = np.transpose(inverse);
        rot = np.array([[np.cos(-0.1), 0, np.sin(-0.1)], [0, 1, 0],
                        [-np.sin(-0.1), 0, np.cos(-0.1)]]);
        orient = np.matmul(rot, np.array([0, 0, 1]));
        orient = np.matmul(inverse, orient);

    if key == b"s":
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
    if key == b"w":
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
    if key == b"+":
        if counter < len(czworosciany) - 1:
            counter += 1
        else:
            counter = 0
    if key == b"-":
        if counter > 0:
            counter -= 1
        else:
            counter = len(czworosciany) - 1
    if key == b'y':
        for i in range(4):
            for j in range(3):
                czworosciany[counter][i][j][1] += 0.1
    if key == b'h':
        for i in range(4):
            for j in range(3):
                czworosciany[counter][i][j][1] -= 0.1
    if key == b'g':
        for i in range(4):
            for j in range(3):
                czworosciany[counter][i][j][0] -= 0.1
    if key == b'j':
        for i in range(4):
            for j in range(3):
                czworosciany[counter][i][j][0] += 0.1
    if key == b't':
        for i in range(4):
            for j in range(3):
                czworosciany[counter][i][j][2] += 0.1
    if key == b'u':
        for i in range(4):
            for j in range(3):
                czworosciany[counter][i][j][2] -= 0.1
    if key == b'b':
        # obrot w lewo
        pass
    if key == b'm':
        # obrot w prawo
        pass




def strona(a, b, c, p):
    """Function checks on which side of (a, b, c) plane the point p is"""
    st = np.array([[a[0] - p[0], a[1] - p[1], a[2] - p[2]],
                   [b[0] - p[0], b[1] - p[1], b[2] - p[2]],
                   [c[0] - p[0], c[1] - p[1], c[2] - p[2]]])
    return np.linalg.det(st)


def pointonline(x, y, p):
    t1 = (p[2] - p[0]) / (p[1] - p[0])
    t2 = (x[2] - x[0]) / (x[1] - x[0])
    t3 = (y[2] - y[0]) / (y[1] - y[0])
    if t1 == t2 == t3:
        return True
    else:
        return False
    
def isPoint(a, b, c):
    """Function checks if given triangle is a point"""
    if a[0] == b[0] == c[0] and a[1] == b[1] == c[1] and a[2] == b[2] == c[2]:
        return True
    else:
        return False

def isSection(a, b, c):
    """Function checks if given triangle is a section"""
    test = np.cross(np.array(b) - np.array(a), np.array(c) - np.array(a))
    return True if test[0] == 0 and test[1] == 0 and test[2] == 0 else False

def isTriangle(a, b, c):
    """Function checks if given point aren't single point or section, thus can create triangle"""
    return True if not isPoint(a, b, c) and not isSection(a, b, c) else False

def pointInTriangle(a, b, c, p):
    """Function checks if given point p is inside triangle (a, b, c)"""
    alpha = beta = 0
    bxax = b[0] - a[0]
    byay = b[1] - a[1]
    bzay = b[2] - a[1]
    bzaz = b[2] - a[2]
    cxax = c[0] - a[0]
    cyay = c[1] - a[1]
    czaz = c[2] - a[2]
    pxax = p[0] - a[0]
    pyay = p[1] - a[1]
    pzaz = p[2] - a[2]
    # Calculate alpha & beta
    if ((bxax*cyay) != (cxax*byay)):
        alpha = ((pxax*cyay) - (cxax*pyay))/((bxax*cyay)-(cxax*byay))
        beta = ((bxax*pyay) - (pxax*byay))/((bxax*cyay)-(cxax*byay))
    elif ((bxax*czaz) != (cxax*bzaz)):
        alpha = ((pzaz*cxax) - (czaz*pxax))/((bxax*czaz)-(cxax*bzaz))
        beta = ((pzaz*bxax) - (bzaz*pxax))/((bxax*czaz)-(cxax*bzaz))
    elif ((bzay*czaz) != (cyay*bzaz)):
        alpha = ((pzaz*cyay) - (czaz*pyay))/((bzay*czaz)-(cyay*bzaz))
        beta = ((pzaz*byay) - (bzaz*pyay))/((bzay*czaz)-(cyay*bzaz))

    # Sprawdzanie przecięcia
    if (alpha >= 0 and beta >= 0 and alpha + beta <= 1): # and (a,b,c,p) dziwnyznaczekpłaszczyzna = 0
        return True
    else:
        return False

def crossingSectionWithSection(a, b, c, d):
    """Function checks if given sections (a, b) and (c, d) cross"""

    # Funkcje pomocnicze
    def calculate_t1(a, b, c):
        if b[0] == a[0] and b[1] != a[1]:
            return calculate_t2(a, b, c)
        elif b[0] == a[0] and b[1] == a[1]:
            return calculate_t3(a, b, c)
        else:
            return (c[0] - a[0])/(b[0] - a[0])
    def calculate_t2(a, b, c):
        if b[1] == a[1] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[1] == a[1] and b[0] == a[0]:
            return calculate_t3(a, b, c)
        else:
            return (c[1] - a[1])/(b[1] - a[1])
    def calculate_t3(a, b, c):
        if b[2] == a[2] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[2] == a[2] and b[0] == a[0]:
            return calculate_t2(a, b, c)
        else:
            return (c[2] - a[2])/(b[2] - a[2])
    def calculate_k1(a, b, c, d):
        if b[0] == a[0] and b[1] != a[1]:
            return calculate_t2(a, b, c)
        elif b[0] == a[0] and b[1] == a[1]:
            return calculate_t3(a, b, c)
        else:
            return (d[0] - a[0])/(b[0] - a[0])
    def calculate_k2(a, b, c, d):
        if b[1] == a[1] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[1] == a[1] and b[0] == a[0]:
            return calculate_t3(a, b, c)
        else:
            return (d[1] - a[1])/(b[1] - a[1])
    def calculate_k3(a, b, c, d):
        if b[2] == a[2] and b[0] != a[0]:
            return calculate_t1(a, b, c)
        elif b[2] == a[2] and b[0] == a[0]:
            return calculate_t3(a, b, c)
        else:
            return (d[2] - a[2])/(b[2] - a[2])


    # Sprawdzenie czy odcinki nie są punktami i są równoległe
    if (not isPoint(a, b, b) and not isPoint(c, d, d) and np.cross(np.array(b) - np.array(a), np.array(d) - np.array(c)).all() == 0):
        t1 = calculate_t1(a, b, c)
        t2 = calculate_t2(a, b, c)
        t3 = calculate_t3(a, b, c)
        k1 = calculate_k1(a, b, c, d)
        k2 = calculate_k2(a, b, c, d)
        k3 = calculate_k3(a, b, c, d)
        t = (t1, t2, t3)
        k = (k1, k2, k3)
        if (
                not (b[0] == a[0] and (c[0] != a[0] or d[0] != a[0]))
            and not (b[1] == a[1] and (c[1] != a[1] or d[1] != a[1]))
            and not (b[2] == a[2] and (c[2] != a[2] or d[2] != a[2]))
            and t1 == t2 == t3
            and k1 == k2 == k3
            and (
                   min(min(t), min(k)) == 0
                or min(min(t), min(k)) == 1
                or max(max(t), max(k)) == 0
                or max(max(t), max(k)) == 1
            )
        ):
            return True
        else:
            return False
    else:
        t = s = 0
        bxax = b[0] - a[0]
        byay = b[1] - a[1]
        bzaz = b[2] - a[2]
        cxax = c[0] - a[0]
        cxdx = c[0] - d[0]
        cyay = c[1] - a[1]
        cydy = c[1] - d[1]
        czaz = c[2] - a[2]
        czdz = c[2] - d[2]
        if ((bxax*cydy) != (cxdx*byay)):
            t = ((cxdx*cyay) - (cxax*cydy))/((bxax*cydy)-(cxdx*byay))
            s = ((bxax*cyay) - (cxax*byay))/((bxax*cydy)-(cxdx*byay))
        elif ((bxax*czdz) != (cxdx*bzaz)):
            t = ((cxdx*czaz) - (cxax*czdz))/((bxax*czdz)-(cxdx*bzaz))
            s = ((bxax*czaz) - (cxax*bzaz))/((bxax*czdz)-(cxdx*bzaz))
        elif ((byay*czdz) != (cydy*bzaz)):
            t = ((cydy*czaz) - (cyay*czdz))/((byay*czdz)-(cydy*bzaz))
            s = ((byay*czaz) - (cyay*bzaz))/((byay*czdz)-(cydy*bzaz))
        # Sprawdzanie przecinania
        return True if t == s else False

def ccTriangles(a, b, c, d, e, f):
    """
    Funkcja sprawdza kolizje między trójkątami (a, b, c) i (d, e, f)
    Brakujące rzeczy: przecinanie się odcinków i właściwych trójkątów
    """
    # 1. typ degeneracji: trójkąty są punktami
    if isPoint(a, b, c) and isPoint(d, e, f):
        if a == d:
            return True
        else:
            return False

    # 2. typ degeneracji: jeden trójkąt jest punktem, drugi odcinkiem (ale nie punktem)
    if isPoint(a, b, c) and not isPoint(d, e, f) and isSection(d, e, f):
        return pointonline(e - d, f - d, a)

    # 3. typ degeneracji: jeden trójkąt jest punktem, drugi nie jest odcinkiem
    if isPoint(a, b, c) and not isSection(d, e, f):
        if (strona(d, e, f, a) == 0 and pointInTriangle(e, d, f, a)):
            return True
        else:
            return False

    # 4. typ degeneracji: sytuacja odwrotna do drugiego
    if isPoint(d, e, f) and isSection(a, b, c):
        return pointonline(b - a, c - a, d)

    # 5. typ degeneracji: sytuacja odwrotna do trzeciego
    if isPoint(d, e, f) and not isSection(a, b, c):
        if (strona(a, b, c, d) == 0 and pointInTriangle(a, b, c, d)):
            return True
        else:
            return False

    # 6. typ degeneracji: trójkąty są odcinkami (ale nie punktami)
    if not(isPoint(a, b, c) or isPoint(d, e, f)) and isSection(a, b, c) and isSection(d, e, f):
        return crossingSectionWithSection(a, b, c, d)

    # 7. typ: jeden trójkąt jest odcinkiem (ale nie punktem), drugi jest trójkątem (ale nie odcinkiem)
    if not(isPoint(a, b, c) or isPoint(d, e, f)) and not isSection(d, e, f) and isSection(a, b, c):
        return sectionInTriangle(b - a, c - a, d, e, f)

    # 8. typ: sytuacja odwrotna do siódmego
    if not(isPoint(a, b, c) or isPoint(d, e, f)) and not isSection(a, b, c) and isSection(d, e, f):
        return sectionInTriangle(e - d, f - d, a, b, c)

    # Brak degeneracji
    return crossingTriangleWithTriangle(a, b, c, d, e, f)

def sectionInTriangle(a, b, d, e, f):
    """Function checks if given section (a, b) is inside triangle (d, e, f)"""
    if isSection(a, b, b) and isTriangle(d, e, f):
        return True if pointInTriangle(d, e, f, a) or pointInTriangle(d, e, f, b) else False
    else:
        return False


def crossingSectionWithTriangle(a, b, d, e, f):
    """Function checks if given section (a, b) crosses triangle (d, e, f)"""
    if (not isPoint(a, b, b) and not isSection(d, e, f) and strona(d, e, f, a) == 0 and strona(d, e, f, b) == 0):
        if (
               (pointInTriangle(d, e, f, a) or pointInTriangle(d, e, f, b))
            or crossingSectionWithSection(a, b, d, e)
            or crossingSectionWithSection(a, b, e, f)
            or crossingSectionWithSection(a, b, f, d)
        ):
            return True
    elif (not isPoint(a, b, b) and not isSection(d, e, f) and (strona(d, e, f, a) != 0 or strona(d, e, f, b) != 0)):
        v = np.cross(np.array(e) - np.array(d), np.array(f) - np.array(d))
        u = v * d
        t = (u - v * a)/(v * (b - a))
        p = np.array(a) + t*(np.array(b) - np.array(a))
        if 0 <= t[0] <= 1 and 0 <= t[1] <= 1 and 0 <= t[2] <= 1 and pointInTriangle(d, e, f, p):
            return True
    return False

def crossingTriangleWithTriangle(a, b, c, d, e, f):
    """Function checks if given triangles (a, b, c) and (d, e, f) crosses"""
    sabcd = strona(a, b, c, d)
    sabce = strona(a, b, c, e)
    sabcf = strona(a, b, c, f)
    if (not isSection(a, b, c) and not isSection(d, e, f)
        and sabcd == 0 and sabce == 0 and sabcf == 0):
        if (
            pointInTriangle(d, e, f, a)
            or pointInTriangle(a, b, c, d)
            or crossingSectionWithSection(a, b, d, e)
            or crossingSectionWithSection(b, c, d, e)
            or crossingSectionWithSection(c, a, d, e)
            or crossingSectionWithSection(a, b, e, f)
            or crossingSectionWithSection(b, c, e, f)
            or crossingSectionWithSection(c, a, e, f)
            or crossingSectionWithSection(a, b, f, d)
            or crossingSectionWithSection(b, c, f, d)
            or crossingSectionWithSection(c, a, f, d)
        ):
            return True
    elif (not isSection(a, b, c) and not isSection(d, e, f)
        and (
               sabcd != sabce
            or sabcd != sabcf
            or sabce != sabcf
        )
    ):
        # Get m, n, o from ^?
        if sabcd != sabce and sabcd != sabcf:
            o = d
            m = e
            n = f
        elif sabce != sabcd and sabce != sabcf:
            o = e
            m = d
            n = f
        elif sabcf != sabcd and sabcf != sabce:
            o = f
            m = d
            n = e
        v = np.cross(np.array(b) - np.array(a), np.array(c) - np.array(a))
        u = v * a
        s = (u - v * np.array(o))/(v * (np.array(m) - np.array(o)))
        p = np.array(o) + s*(np.array(m) - np.array(o))
        t = (u - v * np.array(o))/(v * (np.array(n) - np.array(o)))
        q = np.array(o) + t*(np.array(n) - np.array(o))
        if (crossingSectionWithTriangle(p, q, a, b, c)):
            return True
    return False


# wymuszenie częstotliwości odświeżania
def cupdate():
    global tick;
    ltime = time.clock();
    if (ltime < tick + 0.1):  # max 10 ramek / s
        return False
    tick = ltime
    return True


# pętla wyświetlająca
def display():
    if not cupdate():
        return
    global eye, orient, up
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity();
    glFrustum(-1, 1, -1, 1, 1, 100)
    center = eye + orient;
    gluLookAt(eye[0], eye[1], eye[2], center[0], center[1], center[2],
              up[0], up[1], up[2]);
    global tetra1, tetra2;
    txt = "-"
    for t1 in tetra1:
        for t2 in tetra2:
            if ccTriangles(t1[0], t1[1], t1[2], t2[0], t2[1], t2[2]):
                txt += "Kolizja "
    print(txt)
    glMatrixMode(GL_MODELVIEW);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    dFacelist(tetra1);
    dFacelist(tetra2);
    glFlush();


glutInit();
glutInitWindowSize(600, 600);
glutInitWindowPosition(0, 0);
glutCreateWindow(b"Kolizje 03");
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
glutDisplayFunc(display);
glutIdleFunc(display);
glutKeyboardFunc(keypress);
glClearColor(1.0, 1.0, 1.0, 1.0);
glClearDepth(1.0);
glDepthFunc(GL_LESS);
glEnable(GL_DEPTH_TEST);
glutMainLoop();
