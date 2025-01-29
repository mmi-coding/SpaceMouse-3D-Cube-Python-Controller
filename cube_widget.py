import sys
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtCore import Qt
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
from OpenGL.GLUT import glutInit
from config import DEFAULT_CONFIG
from PyQt5.QtCore import Qt
from OpenGL.GLUT import glutInit
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_QUADS, 
    glBegin, glClear, glClearColor, glColor3f, glEnable, glEnd, glLoadIdentity,
    glMatrixMode, glRotatef, glTranslatef, glVertex3fv, glViewport, GL_MODELVIEW, GL_PROJECTION
)
from OpenGL.GLU import gluPerspective

from PyQt5.QtWidgets import (
    QOpenGLWidget,
)
from keyboard_mouse_input import KeyboardMouseInput
from spacemouse_input import SpaceMouseInput

class CubeWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        glutInit()
        
        self.rotation = {"rx": 0, "ry": 0, "rz": 0}
        self.translation = {"tx": 0, "ty": 0, "tz": -5}
        self.sensitivity = DEFAULT_CONFIG["sensitivity"].copy()
        self.axis_direction = DEFAULT_CONFIG["axis_direction"].copy()
        self.threshold = DEFAULT_CONFIG["threshold"]
        self.axis_enabled = DEFAULT_CONFIG["axis_enabled"].copy()
        self.current_action = "None"
        self.last_mouse_pos = None  # Track mouse movement

        # Initialize SpaceMouse safely
        self.space_mouse = SpaceMouseInput()

        # Initialize Keyboard & Mouse Input
        self.keyboard_mouse = KeyboardMouseInput(self)

        self.setFocusPolicy(Qt.StrongFocus)  # Ensure keyboard focus

        # Reset cube on startup
        self.reset_cube()


    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.2, 0.2, 1.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        glTranslatef(self.translation["tx"], self.translation["tz"], self.translation["ty"])
        glRotatef(self.rotation["ry"], 1, 0, 0)
        glRotatef(self.rotation["rz"], 0, 1, 0)
        glRotatef(self.rotation["rx"], 0, 0, 1)
        
        self.draw_cube()

    def draw_cube(self):
        """Draws a 3D cube."""
        vertices = [(1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, -1),
                    (1, 1, 1), (-1, 1, 1), (-1, -1, 1), (1, -1, 1)]
        faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 3, 7, 4), (1, 2, 6, 5), (0, 1, 5, 4), (3, 2, 6, 7)]
        colors = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
        
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glColor3f(*colors[i])
            for vertex in face:
                glVertex3fv(vertices[vertex])
        glEnd()

    def reset_cube(self):
        """Resets cube position and rotation."""
        self.rotation = {"rx": 0, "ry": 0, "rz": 0}
        self.translation = {"tx": 0, "ty": -5, "tz": 0}
        self.update()

    # ----------- DELEGATE KEYBOARD & MOUSE EVENTS ------------
    def keyPressEvent(self, event: QKeyEvent):
        """Delegate keyboard events to `KeyboardMouseInput`."""
        self.keyboard_mouse.handle_key_press(event)

    def mousePressEvent(self, event: QMouseEvent):
        """Delegate mouse press events to `KeyboardMouseInput`."""
        self.keyboard_mouse.handle_mouse_press(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """Delegate mouse movement events to `KeyboardMouseInput`."""
        self.keyboard_mouse.handle_mouse_move(event)

    def wheelEvent(self, event):
        """Delegate mouse wheel events to `KeyboardMouseInput`."""
        self.keyboard_mouse.handle_wheel_event(event)