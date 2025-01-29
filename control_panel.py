import sys
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,
    QSlider, QLabel, QPushButton, QCheckBox, QFormLayout, QDoubleSpinBox, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer
from cube_widget import CubeWidget

class ControlPanel(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("3Dconnexion Cube Control")
        self.setGeometry(100, 100, 1000, 600)

        # Cube widget on the left (2/3 of window space)
        self.cube_widget = CubeWidget()

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.cube_widget.reset_cube)

        controls_layout = QFormLayout()

        # Sensitivity controls
        self.translation_sensitivity = QDoubleSpinBox()
        self.translation_sensitivity.setValue(self.cube_widget.sensitivity["translation"])
        self.translation_sensitivity.setRange(0.01, 1.0)
        self.translation_sensitivity.setSingleStep(0.01)
        self.translation_sensitivity.valueChanged.connect(
            lambda v: self.cube_widget.sensitivity.update({"translation": v})
        )
        controls_layout.addRow("Translation Sensitivity:", self.translation_sensitivity)

        self.rotation_sensitivity = QDoubleSpinBox()
        self.rotation_sensitivity.setValue(self.cube_widget.sensitivity["rotation"])
        self.rotation_sensitivity.setRange(0.1, 5.0)
        self.rotation_sensitivity.setSingleStep(0.1)
        self.rotation_sensitivity.valueChanged.connect(
            lambda v: self.cube_widget.sensitivity.update({"rotation": v})
        )
        controls_layout.addRow("Rotation Sensitivity:", self.rotation_sensitivity)

        # Threshold control
        self.threshold_slider = QSlider(Qt.Horizontal)
        self.threshold_slider.setRange(1, 100)
        self.threshold_slider.setValue(int(self.cube_widget.threshold * 100))
        self.threshold_slider.valueChanged.connect(
            lambda value: self.cube_widget.__setattr__('threshold', value / 100)
        )
        controls_layout.addRow("Threshold:", self.threshold_slider)

        # Axis inversion checkboxes
        inversion_layout = QGridLayout()
        axis_labels = ["tx", "ty", "tz", "rx", "ry", "rz"]

        for i, axis in enumerate(axis_labels):
            checkbox = QCheckBox(f"Invert {axis.upper()}")
            checkbox.setChecked(self.cube_widget.axis_direction[axis] == -1)
            checkbox.toggled.connect(
                lambda checked, ax=axis: self.cube_widget.axis_direction.update({ax: -1 if checked else 1})
            )
            row, col = divmod(i, 2)
            inversion_layout.addWidget(checkbox, row, col)
        controls_layout.addRow(QLabel("Axis Inversion:"), inversion_layout)

        # Axis activation checkboxes
        activation_layout = QGridLayout()
        for i, axis in enumerate(axis_labels):
            checkbox = QCheckBox(f"Enable {axis.upper()}")
            checkbox.setChecked(self.cube_widget.axis_enabled[axis])
            checkbox.toggled.connect(lambda checked, ax=axis: self.cube_widget.axis_enabled.update({ax: checked}))
            row, col = divmod(i, 2)
            activation_layout.addWidget(checkbox, row, col)
        controls_layout.addRow(QLabel("Axis Activation:"), activation_layout)

        # DOF Status Indicators
        self.dof_status_labels = {axis: QLabel(f"⚪ {axis.upper()} {label}") for axis, label in zip(axis_labels, ["Translate X", "Translate Y", "Translate Z", "Rotate X", "Rotate Y", "Rotate Z"])}
        status_layout = QVBoxLayout()
        status_layout.addWidget(QLabel("DOF Status:"))
        for label in self.dof_status_labels.values():
            status_layout.addWidget(label)
        controls_layout.addRow(status_layout)

        # Add reset button
        controls_layout.addRow(self.reset_button)

        # Combine layouts
        right_controls_widget = QWidget()
        right_controls_widget.setLayout(controls_layout)

        # Main Layout (Cube on left, Controls on right)
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.cube_widget, stretch=2)
        main_layout.addWidget(right_controls_widget, stretch=1)

        # Set central layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Timer to update the current action label periodically
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(100)  # Update every 100 milliseconds

    def update_status(self):
        """Update the DOF status labels with color changes."""
        active_actions = self.cube_widget.current_action.lower().split(", ")
        action_map = {"tx": "translating x", "ty": "translating y", "tz": "translating z", "rx": "rotating x", "ry": "rotating y", "rz": "rotating z"}
        
        for axis, action_name in action_map.items():
            if action_name in active_actions:
                self.dof_status_labels[axis].setText(f"🟢 {self.dof_status_labels[axis].text()[2:]}")
            else:
                self.dof_status_labels[axis].setText(f"⚪ {self.dof_status_labels[axis].text()[2:]}")
