from OpenGL.GL import *;
from OpenGL.GLU import *;
from OpenGL.GLUT import *;
from OpenGL.GL.shaders import *;
import numpy as np;
from PIL import Image
import ctypes;
windowWidth = 800;
windowHeight = 600;
# vertex shader - kod
vsc = """
#version 330 core
layout (location = 0) in vec3 in_pozycja;
layout (location = 1) in vec3 in_kolor;
layout (location = 2) in vec2 in_tex;
uniform mat4 mvp;
out vec4 inter_kolor;
out vec2 inter_tex;
void main() {
gl_Position = mvp * vec4(in_pozycja.xyz, 1.0);
inter_kolor = vec4(in_kolor.xyz, 1.0);
inter_tex = in_tex;
}
"""
# fragment shader - kod
fsc = """
#version 330 core
in vec4 inter_kolor;
in vec2 inter_tex;
uniform sampler2D texobj;
layout (location = 0) out vec4 out_kolor;
void main() {
out_kolor = vec4(inter_kolor.xyzw) * texture2D(texobj, inter_tex);
}
"""
def dummy():
    glutSwapBuffers();
    pass;
def paint():

    # czyszczenie sceny
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    # reakcja na ruch myszką
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glutSwapBuffers();
    pass;
# utworzenie okna
glutInit(sys.argv);
glutInitWindowPosition(int((ctypes.windll.user32.GetSystemMetrics(0) - windowWidth)/2),
int((ctypes.windll.user32.GetSystemMetrics(1) - windowHeight)/2));
glutInitWindowSize(windowWidth, windowHeight);
glutCreateWindow(b"PyOpenGL");
# macierz punktów
punkty = np.array([-1.0, 0.0, 1.0,
1.0, 0.0, 1.0,
0.0, 1.0, 1.0], dtype='float32');
kolory = np.array([1.0, 0.0, 0.0,
0.0, 1.0, 0.0,
0.0, 0.0, 1.0], dtype='float32');
tekstura = np.array([0.0, 0.0,
0.0, 0.1,
1.0, 1.0], dtype='float32');
# shadery
vs = compileShader(vsc, GL_VERTEX_SHADER);
fs = compileShader(fsc, GL_FRAGMENT_SHADER);
sp = glCreateProgram();
glAttachShader(sp, vs);
glAttachShader(sp, fs);
glLinkProgram(sp);
glUseProgram(sp);
# przekazujemy dwa atrybuty do vertex shader-a; pozycję i kolor
glutDisplayFunc(dummy); # niewykorzystana
# bufory
vao0 = glGenVertexArrays(1);
glBindVertexArray(vao0);
vbo0 = glGenBuffers(1); # punkty
glBindBuffer(GL_ARRAY_BUFFER, vbo0);
glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(GLfloat) * len(punkty), punkty,
GL_DYNAMIC_DRAW);
8
glEnableVertexAttribArray(0);
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None);
vbo1 = glGenBuffers(1); # kolory
glBindBuffer(GL_ARRAY_BUFFER, vbo1);
glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(GLfloat) * len(kolory), kolory,
GL_DYNAMIC_DRAW);
glEnableVertexAttribArray(1);
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None);
vbo2 = glGenBuffers(1); # tekstury
glBindBuffer(GL_ARRAY_BUFFER, vbo2);
glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(GLfloat) * len(tekstura), tekstura,
GL_DYNAMIC_DRAW);
glEnableVertexAttribArray(2);
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None);
# tekstura
tex = glGenTextures(1);
glBindTexture(GL_TEXTURE_2D, tex);
image = Image.open("texture.bmp");
width = image.size[0];
height = image.size[1];
image = image.tobytes("raw", "RGBX", 0, -1);
glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image);
glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
#texloc = glGetUniformLocation(sp, "tex"); # tekstura
mvploc = glGetUniformLocation(sp, "mvp"); # model, widok, projekcja
while True:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); # czyszczenie sceny
    # modyfikacja trójkąta
    punkty[0] += 0.0001;
    kolory[0] -= 0.0001;
    # model, widok, projekcja
    mvp = np.identity(4, float);
    glUniformMatrix4fv(mvploc, 1, GL_FALSE, mvp); # przekazywanie do shadera
    # ustawiamy pozycję i kolor
    glBindBuffer(GL_ARRAY_BUFFER, vbo0);
    glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(GLfloat) * len(punkty), punkty,
    GL_DYNAMIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, vbo1);
    glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(GLfloat) * len(kolory), kolory,
    GL_DYNAMIC_DRAW);
    glDrawArrays(GL_TRIANGLES, 0, 3);
    9
    glutSwapBuffers();
    glFlush();
    glutMainLoopEvent();