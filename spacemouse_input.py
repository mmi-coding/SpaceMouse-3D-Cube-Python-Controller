import pyspacemouse

class SpaceMouseInput:
    """Handles SpaceMouse input and provides movement/rotation data."""

    def __init__(self):
        try:
            self.device_connected = pyspacemouse.open()
        except Exception as e:
            print("⚠ Warning: No SpaceMouse detected. Running in fallback mode.")
            print("🔄 Running in fallback mode (keyboard/mouse input).")
            self.device_connected = False

    def get_input(self):
        """Reads input from SpaceMouse and returns movement/rotation data."""
        if not self.device_connected:
            return None

        state = pyspacemouse.read()
        if state is None:
            return None
        
        return {
            "tx": state.x,
            "ty": state.y,
            "tz": state.z,
            "rx": state.roll,
            "ry": state.pitch,
            "rz": state.yaw,
            "buttons": state.buttons
        }

    def close(self):
        """Closes the SpaceMouse connection."""
        if self.device_connected:
            pyspacemouse.close()
