from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL.shaders import *
import numpy as np
import ctypes

windowWidth = 800
windowHeight = 600
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
        ((2*n)/(r-l),           0,           0,  0),
        (          0, (2*n)/(t-b),           0,  0),
        ((r+l)/(r-l), (t+b)/(t-b), (f+n)/(n-f), -1),
        (          0,           0, 2*f*n/(n-f),  0)))

def normalized(v):
    norm = np.linalg.norm(v)
    return v / norm if norm > 0 else v


def look_at(eye, target, up):
    zax = normalized(eye - target)
    xax = normalized(np.cross(up, zax))
    yax = np.cross(zax, xax)
    x = - xax.dot(eye)
    y = - yax.dot(eye)
    z = - zax.dot(eye)
    return np.array(((xax[0], yax[0], zax[0], 0),
                     (xax[1], yax[1], zax[1], 0),
                     (xax[2], yax[2], zax[2], 0),
                     (x, y, z, 1)))


def create_mvp(width, height):
    fov, near, far = 45, 0.1, 100
    eye = np.array((4,3,3))
    target, up = np.array((0,0,0)), np.array((0,1,0))
    projection = perspective(fov, width / height, near, far)
    view = look_at(eye, target, up)
    model = np.identity(4)
    mvp = model @ view @ projection
    print(mvp)
    return  mvp.astype(np.float32)



# utworzenie okna
glutInit(sys.argv)
glutInitWindowPosition(int((ctypes.windll.user32.GetSystemMetrics(0) - windowWidth) / 2),
                       int((ctypes.windll.user32.GetSystemMetrics(1) - windowHeight) / 2))
glutInitWindowSize(windowWidth, windowHeight)
glutCreateWindow(b"PyOpenGL")
# macierz punktów
punkty = [-1.0, 0.0, 1.0,
          1.0, 0.0, 1.0,
          0.0, 1.0, 1.0]
zplus = 0.0
kolory = [1.0, 0.0, 0.0,
          0.0, 1.0, 0.0,
          0.0, 0.0, 1.0]
# shadery
vs = compileShader(vsc, GL_VERTEX_SHADER)
fs = compileShader(fsc, GL_FRAGMENT_SHADER)
sp = glCreateProgram()
glAttachShader(sp, vs)
glAttachShader(sp, fs)
glLinkProgram(sp)
glUseProgram(sp)
# przekazujemy dwa atrybuty do vertex shader-a; pozycję i kolor
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)
glutDisplayFunc(dummy)  # niewykorzystana
while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # czyszczenie sceny
    # modyfikacja trójkąta
    punkty[0] += 0.0001
    # model, widok, projekcja
#    mvp = np.identity(4, float)
    mvp = create_mvp(windowWidth,windowHeight)
    mvploc = glGetUniformLocation(sp, "mvp")  # pobieranie nazwy z shadera
    glUniformMatrix4fv(mvploc, 1, GL_FALSE, mvp)  # przekazywanie do shadera
    # ustawiamy pozycję i kolor
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, punkty)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, kolory)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glutSwapBuffers()
    glFlush()
    glutMainLoopEvent()
