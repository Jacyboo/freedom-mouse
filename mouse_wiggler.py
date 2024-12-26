import random, time, math, sys, pyautogui, keyboard
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

# Version 2.0.0 - Now with 100% more wiggles and 50% less work
VERSION = "2.0.0"

class MouseWigglerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Freedom Mouse - v{VERSION}")
        # Smol window for maximum stealth
        self.setFixedSize(400, 600)
        
        # Variables go brrrrr
        self.is_running = False
        self.total_moves = 0  # Achievement unlocked: Mouse Marathoner
        self.total_distance = 0  # In pixels we trust
        self.active_time = 0  # Time is an illusion, lunch time doubly so
        self.active_timer = QTimer()
        self.active_timer.timeout.connect(self.update_active_time)
        
        # UI assembly required (batteries not included)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # The crown jewel of procrastination
        title = QLabel("Freedom Mouse")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Choose your weapon
        pattern_label = QLabel("Movement Pattern")
        pattern_label.setStyleSheet("color: white;")
        layout.addWidget(pattern_label)
        
        self.pattern_combo = QComboBox()
        # Warning: These moves not suitable for dance floors
        self.pattern_combo.addItems(["Random", "Circle", "Figure 8", "Square"])
        self.pattern_combo.setStyleSheet("""
            QComboBox {
                background-color: #2F353D;
                color: white;
                padding: 5px;
                border: 1px solid #444C56;
            }
            QComboBox QAbstractItemView {
                background-color: #2F353D;
                color: white;
                selection-background-color: #1F6FEB;
            }
        """)
        layout.addWidget(self.pattern_combo)
        
        # How far can your mouse run?
        range_label = QLabel("Movement Range")
        range_label.setStyleSheet("color: white;")
        layout.addWidget(range_label)
        
        # Slide to the left, slide to the right
        range_layout = QHBoxLayout()
        self.range_slider = QSlider(Qt.Horizontal)
        self.range_slider.setMinimum(10)  # Barely a twitch
        self.range_slider.setMaximum(200)  # YEET mode activated
        self.range_slider.setValue(50)
        self.range_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #2F353D;
                height: 4px;
            }
            QSlider::handle:horizontal {
                background: #58A6FF;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }
        """)
        
        self.range_label = QLabel("50 pixels")
        self.range_label.setStyleSheet("color: white;")
        self.range_slider.valueChanged.connect(
            lambda v: self.range_label.setText(f"{v} pixels"))
        
        range_layout.addWidget(self.range_slider)
        range_layout.addWidget(self.range_label)
        layout.addLayout(range_layout)
        
        # Time between zoomies
        interval_label = QLabel("Movement Interval")
        interval_label.setStyleSheet("color: white;")
        layout.addWidget(interval_label)
        
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 60)  # From "zoom" to "snoooooze"
        self.interval_spin.setValue(5)
        self.interval_spin.setSuffix(" seconds")
        self.interval_spin.setStyleSheet("""
            QSpinBox {
                background-color: #2F353D;
                color: white;
                padding: 5px;
                border: 1px solid #444C56;
            }
        """)
        layout.addWidget(self.interval_spin)
        
        # Spicy settings for the brave
        self.random_interval_check = QCheckBox("Randomize intervals")
        self.prevent_sleep_check = QCheckBox("Prevent system sleep")
        self.prevent_sleep_check.setChecked(True)  # Coffee machine mode: ON
        
        for checkbox in [self.random_interval_check, self.prevent_sleep_check]:
            checkbox.setStyleSheet("""
                QCheckBox {
                    color: white;
                }
                QCheckBox::indicator {
                    width: 16px;
                    height: 16px;
                    border: 1px solid #444C56;
                    background: #2F353D;
                }
                QCheckBox::indicator:checked {
                    background: #1F6FEB;
                }
            """)
            layout.addWidget(checkbox)
        
        layout.addSpacing(20)
        
        # Numbers that go up = dopamine go brrr
        stats_layout = QHBoxLayout()
        
        # How many times did we bamboozle the system?
        moves_layout = QVBoxLayout()
        moves_label = QLabel("Total Moves")
        moves_label.setStyleSheet("color: #8B949E;")
        self.moves_value = QLabel("0")
        self.moves_value.setStyleSheet("color: white; font-size: 18px;")
        moves_layout.addWidget(moves_label)
        moves_layout.addWidget(self.moves_value)
        stats_layout.addLayout(moves_layout)
        
        # The mouse has walked to Mordor and back
        distance_layout = QVBoxLayout()
        distance_label = QLabel("Total Distance")
        distance_label.setStyleSheet("color: #8B949E;")
        self.distance_value = QLabel("0 px")
        self.distance_value.setStyleSheet("color: white; font-size: 18px;")
        distance_layout.addWidget(distance_label)
        distance_layout.addWidget(self.distance_value)
        stats_layout.addLayout(distance_layout)
        
        # Time flies when you're pretending to work
        time_layout = QVBoxLayout()
        time_label = QLabel("Active Time")
        time_label.setStyleSheet("color: #8B949E;")
        self.time_value = QLabel("0:00:00")
        self.time_value.setStyleSheet("color: white; font-size: 18px;")
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_value)
        stats_layout.addLayout(time_layout)
        
        layout.addLayout(stats_layout)
        
        layout.addSpacing(20)
        
        # The buttons of destiny
        buttons_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Freedom")  # Unleash the chaos
        self.start_button.clicked.connect(self.toggle_wiggling)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #238636;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2EA043;
            }
        """)
        
        self.stop_button = QPushButton("Stop")  # Panic button
        self.stop_button.clicked.connect(self.stop_wiggling)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #DA3633;
                color: white;
                border: none;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F85149;
            }
            QPushButton:disabled {
                background-color: #21262D;
                color: #8B949E;
            }
        """)
        
        buttons_layout.addWidget(self.start_button)
        buttons_layout.addWidget(self.stop_button)
        layout.addLayout(buttons_layout)
        
        # Current mission status
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: white;
            background-color: #30363D;
            padding: 5px;
            border-radius: 3px;
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Escape hatch for emergencies
        keyboard.on_press_key('esc', lambda _: self.stop_wiggling_with_notification())
        
        # Dark mode because light attracts managers
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0D1117;
            }
            QWidget {
                font-family: 'Segoe UI', Arial;
            }
        """)

    # Time waits for no mouse
    def update_active_time(self):
        self.active_time += 1
        hours = self.active_time // 3600
        minutes = (self.active_time % 3600) // 60
        seconds = self.active_time % 60
        self.time_value.setText(f"{hours}:{minutes:02d}:{seconds:02d}")
        
    # Schrodinger's productivity: simultaneously working and not working
    def toggle_wiggling(self):
        if not self.is_running:
            self.start_wiggling()
        else:
            self.stop_wiggling()
            
    # Release the kraken!
    def start_wiggling(self):
        self.is_running = True
        self.start_button.setText("Pause")
        self.stop_button.setEnabled(True)
        self.status_label.setText("Active")
        self.status_label.setStyleSheet("""
            color: white;
            background-color: #238636;
            padding: 5px;
            border-radius: 3px;
        """)
        
        interval = self.interval_spin.value() * 1000
        if self.random_interval_check.isChecked():
            interval = random.randint(interval // 2, interval * 2)
        
        self.active_timer.start(1000)
        self.move_mouse()
        QTimer.singleShot(interval, self.move_mouse)
        
    # Mission abort! Abort!
    def stop_wiggling(self):
        self.is_running = False
        self.start_button.setText("Start Freedom")
        self.stop_button.setEnabled(False)
        self.status_label.setText("Stopped")
        self.status_label.setStyleSheet("""
            color: white;
            background-color: #DA3633;
            padding: 5px;
            border-radius: 3px;
        """)
        self.active_timer.stop()
            
    # Ninja vanish!
    def stop_wiggling_with_notification(self):
        if self.is_running:
            self.stop_wiggling()
            self.showNormal()
            self.activateWindow()
            
            msg = QMessageBox(self)
            msg.setWindowTitle("Freedom Mouse - Deactivated")
            msg.setText("Mouse movement has been stopped.\nYou're back in control!")
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #0D1117;
                }
                QLabel {
                    color: white;
                }
                QPushButton {
                    background-color: #238636;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                }
            """)
            msg.exec_()
            
    # Mouse.exe has achieved sentience
    def move_mouse(self):
        if not self.is_running:
            return
            
        current_x, current_y = pyautogui.position()
        movement_range = self.range_slider.value()
        pattern = self.pattern_combo.currentText()
        
        # Dance moves that would make a robot proud
        if pattern == "Random":
            new_x = current_x + random.randint(-movement_range, movement_range)
            new_y = current_y + random.randint(-movement_range, movement_range)
        elif pattern == "Circle":
            angle = time.time() * 2
            new_x = current_x + int(movement_range * math.cos(angle))
            new_y = current_y + int(movement_range * math.sin(angle))
        elif pattern == "Figure 8":
            t = time.time() * 2
            new_x = current_x + int(movement_range * math.cos(t))
            new_y = current_y + int(movement_range/2 * math.sin(2*t))
        else:  # Square - because circles are overrated
            t = time.time() % 4
            if t < 1:
                new_x = current_x + movement_range
                new_y = current_y
            elif t < 2:
                new_x = current_x
                new_y = current_y + movement_range
            elif t < 3:
                new_x = current_x - movement_range
                new_y = current_y
            else:
                new_x = current_x
                new_y = current_y - movement_range
                
        # Keep the mouse in bounds (it's not a bird)
        screen_width, screen_height = pyautogui.size()
        new_x = max(0, min(new_x, screen_width))
        new_y = max(0, min(new_y, screen_height))
        
        # Math magic (don't question it)
        distance = int(((new_x - current_x) ** 2 + (new_y - current_y) ** 2) ** 0.5)
        self.total_distance += distance
        self.total_moves += 1
        
        # Numbers go up = happiness
        self.moves_value.setText(str(self.total_moves))
        self.distance_value.setText(f"{self.total_distance} px")
        
        # Sneaky sneaky mouse moves
        pyautogui.moveTo(new_x, new_y, duration=0.5)
        
        # Queue up the next adventure
        if self.is_running:
            interval = self.interval_spin.value() * 1000
            if self.random_interval_check.isChecked():
                interval = random.randint(interval // 2, interval * 2)
            QTimer.singleShot(interval, self.move_mouse)

# Let the chaos begin!
if __name__ == '__main__':
    pyautogui.FAILSAFE = True  # Because yolo isn't always the answer
    
    app = QApplication(sys.argv)
    window = MouseWigglerApp()
    window.show()
    
    sys.exit(app.exec_()) 