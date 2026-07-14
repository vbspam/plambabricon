#!/usr/bin/env python3
import sys
import json
import gettext
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QSlider, QPushButton, QGroupBox)
from PyQt6.QtCore import Qt

# --- I18N SETUP ---
# Set up translation directory lookup (looks inside './locale' directory)
LOCALE_DIR = Path(__file__).parent / "locale"
try:
    translation = gettext.translation("ambient_gui", localedir=str(LOCALE_DIR), fallback=True)
    _ = translation.gettext
except Exception:
    _ = lambda s: s  # Fallback to English if translation catalog is missing
# ------------------

CONFIG_DIR = Path.home() / ".config" / "plambabricon"
CONFIG_PATH = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "min_brightness": 10,
    "max_brightness": 100,
    "max_lux": 1000,
    "hysteresis": 3
}

class AmbientGui(QWidget):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.init_ui()

    def load_config(self):
        """Loads configuration from JSON file."""
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, "r") as f:
                    return {**DEFAULT_CONFIG, **json.load(f)}
            except Exception:
                pass
        return DEFAULT_CONFIG.copy()

    def save_config(self):
        """Saves current configuration to JSON file."""
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.config, f, indent=4)

    def init_ui(self):
        self.setWindowTitle(_("Ambient Brightness Settings"))
        self.resize(400, 300)
        
        layout = QVBoxLayout()

        # --- BRIGHTNESS LIMITS GROUP ---
        group_brightness = QGroupBox(_("Brightness Limits (%)"))
        gb_layout = QVBoxLayout()

        # Minimum Brightness
        self.min_label = QLabel()
        self.min_slider = QSlider(Qt.Orientation.Horizontal)
        self.min_slider.setRange(1, 100)
        self.min_slider.setValue(self.config["min_brightness"])
        self.min_slider.valueChanged.connect(self.update_min_brightness)
        self.update_min_label(self.config["min_brightness"])
        gb_layout.addWidget(self.min_label)
        gb_layout.addWidget(self.min_slider)

        # Maximum Brightness
        self.max_label = QLabel()
        self.max_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_slider.setRange(1, 100)
        self.max_slider.setValue(self.config["max_brightness"])
        self.max_slider.valueChanged.connect(self.update_max_brightness)
        self.update_max_label(self.config["max_brightness"])
        gb_layout.addWidget(self.max_label)
        gb_layout.addWidget(self.max_slider)

        group_brightness.setLayout(gb_layout)
        layout.addWidget(group_brightness)

        # --- SENSOR SENSITIVITY GROUP ---
        group_sens = QGroupBox(_("Sensor Sensitivity"))
        gs_layout = QVBoxLayout()

        # Maximum Lux
        self.lux_label = QLabel()
        self.lux_slider = QSlider(Qt.Orientation.Horizontal)
        self.lux_slider.setRange(50, 500)
        self.lux_slider.setSingleStep(100)
        self.lux_slider.setValue(self.config["max_lux"])
        self.lux_slider.valueChanged.connect(self.update_lux)
        self.update_lux_label(self.config["max_lux"])
        gs_layout.addWidget(self.lux_label)
        gs_layout.addWidget(self.lux_slider)

        group_sens.setLayout(gs_layout)
        layout.addWidget(group_sens)

        # --- BUTTONS ---
        btn_layout = QHBoxLayout()
        save_btn = QPushButton(_("Save and Apply"))
        save_btn.clicked.connect(self.save_and_close)
        cancel_btn = QPushButton(_("Cancel"))
        cancel_btn.clicked.connect(self.close)
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_min_label(self, val):
        self.min_label.setText(_("Minimum brightness: {}%").format(val))

    def update_min_brightness(self, val):
        if val > self.max_slider.value():
            self.max_slider.setValue(val)
        self.config["min_brightness"] = val
        self.update_min_label(val)

    def update_max_label(self, val):
        self.max_label.setText(_("Maximum brightness: {}%").format(val))

    def update_max_brightness(self, val):
        if val < self.min_slider.value():
            self.min_slider.setValue(val)
        self.config["max_brightness"] = val
        self.update_max_label(val)

    def update_lux_label(self, val):
        self.lux_label.setText(_("100% brightness at: {} Lux").format(val))

    def update_lux(self, val):
        self.config["max_lux"] = val
        self.update_lux_label(val)

    def save_and_close(self):
        self.save_config()
        print("Configuration saved.")
        self.close()

def main():
    app = QApplication(sys.argv)
    gui = AmbientGui()
    gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()