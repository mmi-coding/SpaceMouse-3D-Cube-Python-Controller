from PyQt5.QtGui import QKeyEvent, QMouseEvent
from PyQt5.QtCore import Qt
from config import DEFAULT_CONFIG

class KeyboardMouseInput:
    """Handles keyboard and mouse input for cube control."""
    
    def __init__(self, cube_widget):
        self.cube_widget = cube_widget
        self.last_mouse_pos = None  # Track mouse movement
        self.keyboard_layout = DEFAULT_CONFIG.get("keyboard_layout", "AZERTY")
        self.key_mapping = self.get_key_mapping()  

    def get_key_mapping(self):
        """Returns key mappings for AZERTY and QWERTY layouts."""
        if self.keyboard_layout == "AZERTY":
            return {
                "forward": Qt.Key_Z,
                "backward": Qt.Key_S,
                "left": Qt.Key_Q,
                "right": Qt.Key_D,
                "up": Qt.Key_A,
                "down": Qt.Key_E,
            }
        else:  # QWERTY
            return {
                "forward": Qt.Key_W,
                "backward": Qt.Key_S,
                "left": Qt.Key_A,
                "right": Qt.Key_D,
                "up": Qt.Key_Q,
                "down": Qt.Key_E,
            }

    def handle_key_press(self, event: QKeyEvent):
        """Processes keyboard inputs for translation and rotation."""
        key = event.key()
        move_speed = self.cube_widget.sensitivity["translation"]
        rotate_speed = self.cube_widget.sensitivity["rotation"]

        # key_mapping = self.cube_widget.get_key_mapping()

        
        if key == self.key_mapping["forward"]:
            self.cube_widget.translation["ty"] += move_speed
        elif key == self.key_mapping["backward"]:
            self.cube_widget.translation["ty"] -= move_speed
        elif key == self.key_mapping["left"]:
            self.cube_widget.translation["tx"] -= move_speed
        elif key == self.key_mapping["right"]:
            self.cube_widget.translation["tx"] += move_speed
        elif key == self.key_mapping["up"]:
            self.cube_widget.translation["tz"] += move_speed
        elif key == self.key_mapping["down"]:
            self.cube_widget.translation["tz"] -= move_speed
        elif key == Qt.Key_Left:
            self.cube_widget.rotation["rz"] += rotate_speed
        elif key == Qt.Key_Right:
            self.cube_widget.rotation["rz"] -= rotate_speed
        elif key == Qt.Key_Up:
            self.cube_widget.rotation["rx"] += rotate_speed
        elif key == Qt.Key_Down:
            self.cube_widget.rotation["rx"] -= rotate_speed
        elif key == Qt.Key_R:
            self.cube_widget.reset_cube()
        
        self.cube_widget.update()

    def handle_mouse_press(self, event: QMouseEvent):
        """Tracks mouse press for rotation."""
        self.last_mouse_pos = event.pos()

    def handle_mouse_move(self, event: QMouseEvent):
        """Handles mouse movement for rotation."""
        if self.last_mouse_pos is None:
            return

        dx = event.x() - self.last_mouse_pos.x()
        dy = event.y() - self.last_mouse_pos.y()

        self.cube_widget.rotation["ry"] += dy * 0.2
        self.cube_widget.rotation["rz"] += dx * 0.2

        self.last_mouse_pos = event.pos()
        self.cube_widget.update()

    def handle_wheel_event(self, event):
        """Handles zooming with mouse wheel."""
        delta = event.angleDelta().y()
        zoom_factor = 0.1 if delta > 0 else -0.1
        self.cube_widget.translation["tz"] += zoom_factor
        self.cube_widget.update()
