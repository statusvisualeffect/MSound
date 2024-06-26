import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QWidget,
    QFileDialog, QLabel, QDialog, QRadioButton, QButtonGroup, QMessageBox, QComboBox, QSlider
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pynput import mouse, keyboard
import pygame

# Initialize pygame mixer
pygame.mixer.init()

CONFIG_PATH = "config.json"

# Define the default paths to your sound files
default_sound_paths = {
    "left": "sounds\\LMouseClick.wav",
    "right": "sounds\\RMouseClick.wav",
    "middle": "sounds\\MButton.wav",
    "keyboard": "sounds\\KB.mp3"
}

# Load configuration
def load_config():
    default_config = {
        "left": True, "right": True, "middle": True, "keyboard": True,
        "left_path": default_sound_paths["left"],
        "right_path": default_sound_paths["right"],
        "middle_path": default_sound_paths["middle"],
        "keyboard_path": default_sound_paths["keyboard"],
        "theme": "light",
        "toggle_keys": ["r", "y", "h"],
        "volume": 100
    }
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            # Ensure all keys are present in the config
            for key in default_config:
                if key not in config:
                    config[key] = default_config[key]
            return config
    return default_config

# Save configuration
def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

config = load_config()

special_keys = {
    "space": " ",
    "enter": "\n",
    "tab": "\t",
    "escape": chr(27),
    "backspace": chr(8),
    "delete": chr(127),
    "left": keyboard.Key.left,
    "right": keyboard.Key.right,
    "up": keyboard.Key.up,
    "down": keyboard.Key.down,
    "shift": keyboard.Key.shift,
    "ctrl": keyboard.Key.ctrl,
    "alt": keyboard.Key.alt,
    "caps_lock": keyboard.Key.caps_lock,
    "f1": keyboard.Key.f1,
    "f2": keyboard.Key.f2,
    "f3": keyboard.Key.f3,
    "f4": keyboard.Key.f4,
    "f5": keyboard.Key.f5,
    "f6": keyboard.Key.f6,
    "f7": keyboard.Key.f7,
    "f8": keyboard.Key.f8,
    "f9": keyboard.Key.f9,
    "f10": keyboard.Key.f10,
    "f11": keyboard.Key.f11,
    "f12": keyboard.Key.f12,
}

def get_key_name(key):
    if hasattr(key, 'char'):
        return key.char
    else:
        for name, k in special_keys.items():
            if key == k:
                return name
        return str(key)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        self.theme_group = QButtonGroup(self)
        self.light_theme = QRadioButton("Light Theme")
        self.dark_theme = QRadioButton("Dark Theme")

        self.theme_group.addButton(self.light_theme)
        self.theme_group.addButton(self.dark_theme)

        if config["theme"] == "light":
            self.light_theme.setChecked(True)
        else:
            self.dark_theme.setChecked(True)

        self.light_theme.toggled.connect(self.update_theme)
        self.dark_theme.toggled.connect(self.update_theme)

        layout.addWidget(self.light_theme)
        layout.addWidget(self.dark_theme)

        # Key combination settings
        key_layout = QHBoxLayout()
        self.key_comboboxes = []
        all_keys = list("abcdefghijklmnopqrstuvwxyz1234567890") + list(special_keys.keys())
        for i in range(3):
            combobox = QComboBox()
            combobox.addItems(all_keys)
            combobox.setCurrentText(config["toggle_keys"][i])
            self.key_comboboxes.append(combobox)
            key_layout.addWidget(combobox)
        layout.addLayout(key_layout)

        # Volume control
        layout.addWidget(QLabel("Volume"))
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(1, 100)
        self.volume_slider.setValue(config["volume"])
        self.volume_slider.setTickInterval(1)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        layout.addWidget(self.volume_slider)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def update_theme(self):
        if self.light_theme.isChecked():
            config["theme"] = "light"
        else:
            config["theme"] = "dark"
        save_config(config)
        self.parent().apply_theme()

    def save_settings(self):
        keys = [combobox.currentText() for combobox in self.key_comboboxes]
        for i, key in enumerate(keys):
            if key in special_keys:
                keys[i] = special_keys[key]
        config["toggle_keys"] = keys
        config["volume"] = self.volume_slider.value()
        save_config(config)
        self.close()

class MainWindow(QMainWindow):
    toggle_visibility_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("MSound")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()
        
        self.create_sound_control(layout, "Left Click Sound", "left")
        self.create_sound_control(layout, "Right Click Sound", "right")
        self.create_sound_control(layout, "Middle Click Sound", "middle")
        self.create_sound_control(layout, "Keyboard Sound", "keyboard")

        settings_button = QPushButton("Settings")
        settings_button.clicked.connect(self.open_settings)
        layout.addWidget(settings_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.apply_theme()
        self.hide()  # Start with the window hidden

        self.toggle_visibility_signal.connect(self.toggle_visibility)
    
    def create_sound_control(self, layout, label_text, config_key):
        control_layout = QVBoxLayout()

        control_layout.addWidget(QLabel(label_text))
        
        checkbox = QCheckBox("Enable")
        checkbox.setChecked(config[config_key])
        checkbox.stateChanged.connect(self.update_config)
        setattr(self, f"{config_key}_checkbox", checkbox)
        
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(lambda: self.browse_sound(config_key))
        
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(lambda: self.reset_sound(config_key))

        h_layout = QHBoxLayout()
        h_layout.addWidget(checkbox)
        h_layout.addWidget(browse_button)
        h_layout.addWidget(reset_button)
        
        control_layout.addLayout(h_layout)
        layout.addLayout(control_layout)
    
    def update_config(self):
        config["left"] = self.left_checkbox.isChecked()
        config["right"] = self.right_checkbox.isChecked()
        config["middle"] = self.middle_checkbox.isChecked()
        config["keyboard"] = self.keyboard_checkbox.isChecked()
        save_config(config)
    
    def browse_sound(self, config_key):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Sound File", "", "Sound Files (*.wav *.mp3);;All Files (*)", options=options)
        if file_path:
            config[f"{config_key}_path"] = file_path
            save_config(config)
    
    def reset_sound(self, config_key):
        config[f"{config_key}_path"] = default_sound_paths[config_key]
        save_config(config)
    
    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()

    def apply_theme(self):
        if config["theme"] == "light":
            self.setStyleSheet("")
        else:
            self.setStyleSheet("background-color: #2e2e2e; color: #ffffff;")

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()

    def closeEvent(self, event):
        reply = QMessageBox.information(self, "Close",
                                        f"Чтобы закрыть нажмите {', '.join(config['toggle_keys'])}",
                                        QMessageBox.Ok)
        event.ignore()

class KeyListenerThread(QThread):
    key_pressed_signal = pyqtSignal(object)
    play_sound_signal = pyqtSignal(str)

    def run(self):
        pressed_keys = set()

        def on_press(key):
            key_name = get_key_name(key)
            if key_name in config["toggle_keys"]:
                pressed_keys.add(key_name)
                if all(k in pressed_keys for k in config["toggle_keys"]):
                    self.key_pressed_signal.emit(key)
            if config["keyboard"]:
                self.play_sound_signal.emit(config["keyboard_path"])

        def on_release(key):
            key_name = get_key_name(key)
            if key_name in pressed_keys:
                pressed_keys.remove(key_name)

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

def play_sound(path):
    try:
        volume = config.get("volume", 100) / 100.0
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
    except pygame.error as e:
        print(f"Error playing sound: {e}")

def on_click(x, y, button, pressed):
    if pressed:
        if button == mouse.Button.left and config["left"]:
            play_sound(config["left_path"])
        elif button == mouse.Button.right and config["right"]:
            play_sound(config["right_path"])
        elif button == mouse.Button.middle and config["middle"]:
            play_sound(config["middle_path"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    mouse_listener = mouse.Listener(on_click=on_click)
    mouse_listener.start()

    key_listener_thread = KeyListenerThread()
    key_listener_thread.key_pressed_signal.connect(window.toggle_visibility_signal)
    key_listener_thread.play_sound_signal.connect(play_sound)
    key_listener_thread.start()

    sys.exit(app.exec_())
