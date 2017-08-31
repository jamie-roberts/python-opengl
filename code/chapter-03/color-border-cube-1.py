# -----------------------------------------------------------------------------
# Python, OpenGL & Scientific Visualization
# www.labri.fr/perso/nrougier/python+opengl
# Copyright (c) 2017, Nicolas P. Rougier
# Distributed under the 2-Clause BSD License.
# -----------------------------------------------------------------------------
import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.geometry import colorcube

vertex = """
uniform mat4   u_model;         // Model matrix
uniform mat4   u_view;          // View matrix
uniform mat4   u_projection;    // Projection matrix
attribute vec4 a_color;         // Vertex color
attribute vec3 a_position;      // Vertex position
varying vec3   v_position;      // Interpolated vertex position (out)
varying vec4   v_color;         // Interpolated fragment color (out)
void main()
{
    v_color = a_color;
    v_position = a_position;
    gl_Position = u_projection * u_view * u_model * vec4(a_position,1.0);
}
"""

fragment = """
varying vec4 v_color;    // Interpolated fragment color (in)
varying vec3 v_position; // Interpolated vertex position (in)
void main()
{
    float xy = min( abs(v_position.x), abs(v_position.y));
    float xz = min( abs(v_position.x), abs(v_position.z));
    float yz = min( abs(v_position.y), abs(v_position.z));
    float b = 0.85;

    if ((xy > b) || (xz > b) || (yz > b))
        gl_FragColor = vec4(0,0,0,1);
    else
        gl_FragColor = v_color;
}
"""

window = app.Window(width=512, height=512, color=(1, 1, 1, 1))

@window.event
def on_draw(dt):
    global phi, theta
    window.clear()

    # Filled cube
    cube.draw(gl.GL_TRIANGLES, I)
    
    # Rotate cube
    theta += 1.0 # degrees
    phi += -1.0 # degrees
    model = np.eye(4, dtype=np.float32)
    glm.rotate(model, theta, 0, 0, 1)
    glm.rotate(model, phi, 0, 1, 0)
    cube['u_model'] = model


@window.event
def on_resize(width, height):
    cube['u_projection'] = glm.perspective(45.0, width / float(height), 2.0, 100.0)

@window.event
def on_init():
    gl.glEnable(gl.GL_DEPTH_TEST)


V = np.zeros(8, [("a_position", np.float32, 3),
                 ("a_color",    np.float32, 4)])
V["a_position"] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                   [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
V["a_color"]    = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1],
                   [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1]]
V = V.view(gloo.VertexBuffer)
I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
              1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)
I = I.view(gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(V)

cube['u_model'] = np.eye(4, dtype=np.float32)
cube['u_view'] = glm.translation(0, 0, -5)
phi, theta = 40, 30

app.run(framerate=60, framecount=360)
