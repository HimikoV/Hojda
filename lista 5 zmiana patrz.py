"""
DODAŁEM OBROT CUBE'a PRZY UZYCIU TEJ FUNKCJI Z LISTY 4
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import ctypes

x1 = x2 = x3 = 0
windowWidth = 800
windowHeight = 600
mousex = windowWidth
mousey = windowHeight

# vertex shader - kod
vsc = """
#version 330 core
layout (location = 0) in vec3 in_pozycja;
layout (location = 1) in vec3 in_kolor;
uniform mat4 mvp;
out vec4 inter_kolor;
void main() {
gl_Position = mvp * vec4(in_pozycja.xyz, 1.0);
inter_kolor = vec4(in_kolor.xyz, 1.0);
}
"""
# fragment shader - kod
fsc = """
#version 330 core
in vec4 inter_kolor;
layout (location = 0) out vec4 out_kolor;
void main() {
out_kolor = vec4(inter_kolor.xyzw);
}
"""

def mouseMotion(x, y):
    global mousex, mousey,ok,ko
    mousex = 0 if x < 0 else windowWidth/100 if x > windowWidth else x/100
    mousey = 0 if y < 0 else windowHeight/100 if y > windowHeight else y/100
    ok = mousex
    print(ok)
    ko = mousey

    pass

def mouseMouse(btn, stt, x, y):
    pass


def dummy():
    glutSwapBuffers()
    pass


def paint():
    # czyszczenie sceny
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # reakcja na ruch myszką
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    glutSwapBuffers()
    pass


def perspective(fov, aspect, near, far):
    n, f = near, far
    t = np.tan((fov * np.pi / 180) / 2) * near
    b = - t
    r = t * aspect
    l = b * aspect
    assert abs(n - f) > 0
    return np.array((
        ((2 * n) / (r - l), 0, 0, 0),
        (0, (2 * n) / (t - b), 0, 0),
        ((r + l) / (r - l), (t + b) / (t - b), (f + n) / (n - f), -1),
        (0, 0, 2 * f * n / (n - f), 0)))


def normalized(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


def patrz(eyeX, eyeY, eyeZ, targetX, targetY, targetZ, upX, upY, upZ):
    zax = normalized(np.array([eyeX, eyeY, eyeZ]) - np.array([targetX, targetY, targetZ]))
    xax = normalized(np.cross([upX, upY, upZ], zax))
    yax = np.cross(zax, xax)
    x = - xax.dot([eyeX, eyeY, eyeZ])
    y = - yax.dot([eyeX, eyeY, eyeZ])
    z = - zax.dot([eyeX, eyeY, eyeZ])
    return np.array(((xax[0], yax[0], zax[0], 0),
                     (xax[1], yax[1], zax[1], 0),
                     (xax[2], yax[2], zax[2], 0),
                     (x, y, z, 1)))


def create_mvp(width, height,ok,ko):
    fov, near, far = 45, 0.1, 100
    eyeX, eyeY, eyeZ = np.array((ok, ko, 2))
    targetX, targetY, targetZ = np.array((0, 0, 0))
    upX, upY, upZ = np.array((0, 1, 0))
    projection = perspective(fov, width / height, near, far)
    view = patrz(eyeX, eyeY, eyeZ, targetX, targetY, targetZ, upX, upY, upZ)
    model = np.identity(4)
    mvp = model @ view @ projection
    return mvp.astype(np.float32)


# utworzenie okna
glutInit(sys.argv)
glutInitWindowPosition(int((ctypes.windll.user32.GetSystemMetrics(0) - windowWidth) / 2),
                       int((ctypes.windll.user32.GetSystemMetrics(1) - windowHeight) / 2))
glutInitWindowSize(windowWidth, windowHeight)
glutCreateWindow(b"PyOpenGL")


def cube(mousex, mousey, size, kat, x1, x2, x3):
    punkty = [mousex + size, mousey - size, 1.0 - size,
              mousex - size, mousey - size, 1.0 - size,
              mousex - size, mousey + size, 1.0 - size,
              mousex - size, mousey + size, 1.0 - size,
              mousex + size, mousey + size, 1.0 - size,
              mousex + size, mousey - size, 1.0 - size,
              mousex + size, mousey + size, 1.0 - size,
              mousex + size, mousey - size, 1.0 - size,
              mousex + size, mousey + size, 1.0 + size,
              mousex + size, mousey - size, 1.0 - size,
              mousex + size, mousey - size, 1.0 + size,
              mousex + size, mousey + size, 1.0 + size,
              mousex - size, mousey - size, 1.0 - size,
              mousex - size, mousey + size, 1.0 - size,
              mousex - size, mousey - size, 1.0 + size,
              mousex - size, mousey + size, 1.0 - size,
              mousex - size, mousey - size, 1.0 + size,
              mousex - size, mousey + size, 1.0 + size,
              mousex - size, mousey - size, 1.0 + size,
              mousex - size, mousey + size, 1.0 + size,
              mousex + size, mousey + size, 1.0 + size,
              mousex - size, mousey - size, 1.0 + size,
              mousex + size, mousey - size, 1.0 + size,
              mousex + size, mousey + size, 1.0 + size,
              mousex - size, mousey + size, 1.0 - size,
              mousex - size, mousey + size, 1.0 + size,
              mousey + size, mousey + size, 1.0 + size,
              mousex - size, mousey + size, 1.0 - size,
              mousex + size, mousey + size, 1.0 + size,
              mousex + size, mousey + size, 1.0 - size,
              mousex - size, mousey - size, 1.0 - size,
              mousex - size, mousey - size, 1.0 + size,
              mousey + size, mousey - size, 1.0 + size,
              mousex - size, mousey - size, 1.0 - size,
              mousex + size, mousey - size, 1.0 + size,
              mousex + size, mousey - size, 1.0 - size, ]

    p0 = [mousex, mousey, 1]
    wersor = [12, 41, 11]
    lel = []
    for i in range(36):
        xd = obrot_zad_2(p0, wersor, (punkty[3 * i], punkty[3 * i + 1], punkty[3 * i + 2]), kat).tolist()
        lel.append(xd[0])
        lel.append(xd[1])
        lel.append(xd[2])

    lel2 = []
    for i in range(36):
        npkt = cam_trans((lel[3 * i], lel[3 * i + 1], lel[3 * i + 2]), x1, x2, x3)
        # npkt = npkt.tolist()
        lel2.append(npkt[0])
        lel2.append(npkt[1])
        lel2.append(npkt[2])
    return lel2


def cam_trans(p, tx, ty, tz):
    cam_t = [[1, 0, 0, tx],
             [0, 1, 0, ty],
             [0, 0, 1, tz],
             [0, 0, 0, 1]]
    p = [p[0], p[1], p[2], 1]
    xd = np.matmul(cam_t, p)
    return xd


def obrot_zad_2(p0, wektor, punkt, kat):
    jednostkowy = np.sqrt(wektor[0] ** 2 + wektor[1] ** 2 + wektor[2] ** 2)
    if jednostkowy != 1:
        wersor = wektor / jednostkowy
    wersor = np.array(wersor)
    M = [[wersor[0] ** 2 * (1 - np.cos(kat)) + np.cos(kat),
          wersor[0] * wersor[1] * (1 - np.cos(kat) - wersor[2] * np.sin(kat)),
          wersor[0] * wersor[2] * (1 - np.cos(kat)) + wersor[1] * np.sin(kat)],
         [wersor[0] * wersor[1] * (1 - np.cos(kat)) + wersor[2] * np.sin(kat),
          wersor[1] ** 2 * (1 - np.cos(kat) + np.cos(kat)),
          wersor[1] * wersor[2] * (1 - np.cos(kat)) - wersor[0] * np.sin(kat)],
         [wersor[0] * wersor[2] * (1 - np.cos(kat)) - wersor[1] * np.sin(kat),
          wersor[1] * wersor[2] * (1 - np.cos(kat) + wersor[0] * np.sin(kat)),
          wersor[2] ** 2 * (1 - np.cos(kat)) + np.cos(kat)]]

    M = np.array(M)
    punkt = np.array(punkt)
    punkt = punkt - p0
    punkt = M @ punkt.T
    punkt = punkt + np.array(p0)
    punkt = punkt.T
    return punkt


zplus = 0.0
kolory = [0.583, 0.771, 0.014,
          0.609, 0.115, 0.436,
          0.327, 0.483, 0.844,
          0.822, 0.569, 0.201,
          0.435, 0.602, 0.223,
          0.310, 0.747, 0.185,
          0.597, 0.770, 0.761,
          0.559, 0.436, 0.730,
          0.359, 0.583, 0.152,
          0.483, 0.596, 0.789,
          0.559, 0.861, 0.639,
          0.195, 0.548, 0.859,
          0.014, 0.184, 0.576,
          0.771, 0.328, 0.970,
          0.406, 0.615, 0.116,
          0.676, 0.977, 0.133,
          0.971, 0.572, 0.833,
          0.140, 0.616, 0.489,
          0.997, 0.513, 0.064,
          0.945, 0.719, 0.592,
          0.543, 0.021, 0.978,
          0.279, 0.317, 0.505,
          0.167, 0.620, 0.077,
          0.347, 0.857, 0.137,
          0.055, 0.953, 0.042,
          0.714, 0.505, 0.345,
          0.783, 0.290, 0.734,
          0.722, 0.645, 0.174,
          0.302, 0.455, 0.848,
          0.225, 0.587, 0.040,
          0.517, 0.713, 0.338,
          0.053, 0.959, 0.120,
          0.393, 0.621, 0.362,
          0.673, 0.211, 0.457,
          0.820, 0.883, 0.371,
          0.982, 0.099, 0.879]


def keyboard(bkey, x, y):
    global x1
    global x2
    global x3

    global lookz
    global mousey
    global kej
    global cube_select
    key = bkey.decode("utf-8")
    if key == 'd':
        x1 += 0.01
    elif key == 'a':
        x1 -= 0.01
    elif key == 'w':
        x2 += 0.01
    elif key == 's':
        x2 -= 0.01
    elif key == 'q':
        x3 -= 0.01
    elif key == 'e':
        x3 += 0.01
        # ESC HERE
    elif key == '\x1b':
        sys.exit()
    elif kej == '':
        kej = 0


# shadery
vs = compileShader(vsc, GL_VERTEX_SHADER)
fs = compileShader(fsc, GL_FRAGMENT_SHADER)
sp = glCreateProgram()
glAttachShader(sp, vs)
glutMouseFunc(mouseMouse)
glutMotionFunc(mouseMotion)

glAttachShader(sp, fs)
glLinkProgram(sp)
glUseProgram(sp)
# przekazujemy dwa atrybuty do vertex shader-a; pozycję i kolor
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)

glutDisplayFunc(dummy)  # niewykorzystana
kat = 0
ok = 0
ko = 0
while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # czyszczenie sceny
    # modyfikacja trójkąta
    # model, widok, projekcja
    # mvp = np.identity(4, float)
    punkty1 = cube(1, 1, 0.2, kat, x1, x2, x3)
    punkty2 = cube(2, 2, 0.2, kat, x1, x2, x3)
    punkty3 = cube(0.1, .1, 0.1, kat, x1, x2, x3)
    kat += 0.001

    mvp = create_mvp(mousex, mousey,ok,ko)
    mvploc = glGetUniformLocation(sp, "mvp")  # pobieranie nazwy z shadera
    glUniformMatrix4fv(mvploc, 1, GL_FALSE, mvp)  # przekazywanie do shadera
    # ustawiamy pozycję i kolor
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, punkty1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, kolory)
    glDrawArrays(GL_TRIANGLES, 0, 3 * 12)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, punkty2)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, kolory)
    glDrawArrays(GL_TRIANGLES, 0, 3 * 12)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, punkty3)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, kolory)
    glDrawArrays(GL_TRIANGLES, 0, 3 * 12)

    glutSwapBuffers()
    glFlush()
    glutKeyboardFunc(keyboard)
    glutMainLoopEvent()
