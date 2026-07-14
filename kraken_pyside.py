#!/usr/bin/env python3
"""
KRAKEN - The Devourer of Paste Restrictions
PySide6 Edition - Ubuntu Native Stack
"""

import sys
import json
import os
import time
import subprocess
import tempfile
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                               QSlider, QComboBox, QCheckBox, QProgressBar,
                               QMessageBox, QInputDialog, QGroupBox, QGridLayout)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QPalette, QColor

try:
    from Xlib import display, X
    from Xlib.error import DisplayError
    XLIB_AVAILABLE = True
except ImportError:
    XLIB_AVAILABLE = False


class TypingThread(QThread):
    """Thread for typing text using CLI subprocess"""
    progress = Signal(int)
    status = Signal(str)
    finished = Signal()
    
    def __init__(self, text, speed, countdown, human_like, typos):
        super().__init__()
        self.text = text
        self.speed = speed
        self.countdown = countdown
        self.human_like = human_like
        self.typos = typos
        self.should_stop = False
    
    def run(self):
        """Execute typing via CLI subprocess"""
        try:
            # Build command
            cli_path = os.path.join(os.path.dirname(__file__), 'kraken_cli.py')
            cmd = [
                'python3', cli_path,
                '--text', self.text,
                '--speed', str(self.speed),
                '--countdown', '0',  # Countdown handled in GUI
                '--quiet'  # Suppress CLI output
            ]
            
            if self.human_like:
                cmd.append('--human-like')
            else:
                cmd.append('--no-human-like')
            
            if self.typos:
                cmd.append('--typos')
            
            print(f"[DEBUG] Text length: {len(self.text)}")
            
            # Countdown manually
            for i in range(self.countdown, 0, -1):
                if self.should_stop:
                    return
                self.status.emit(f"🐙 Kraken awakening in {i}... (Click target field!)")
                time.sleep(1)
            
            self.status.emit("🌊 KRAKEN UNLEASHED! Typing...")
            
            # Run CLI version
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"[DEBUG] Process started with PID: {process.pid}")
            
            # Monitor progress
            total = len(self.text)
            typed = 0
            
            while process.poll() is None:
                if self.should_stop:
                    process.terminate()
                    break
                
                # Estimate progress
                typed = min(typed + 5, total)
                progress_val = int((typed / total) * 100)
                self.progress.emit(progress_val)
                time.sleep(0.1)
            
            stdout, stderr = process.communicate()
            
            print(f"[DEBUG] Process exited with code: {process.returncode}")
            print(f"[DEBUG] STDOUT: {stdout}")
            print(f"[DEBUG] STDERR: {stderr}")
            
            if process.returncode == 0:
                self.status.emit("✅ Kraken devoured all restrictions!")
                self.progress.emit(100)
            else:
                error_msg = stderr.strip() if stderr.strip() else "Unknown error"
                self.status.emit(f"❌ Error: {error_msg}")
                print(f"[ERROR] CLI failed: {error_msg}")
        
        except Exception as e:
            self.status.emit(f"❌ Error: {str(e)}")
            print(f"[EXCEPTION] {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.finished.emit()
    
    def stop(self):
        """Stop typing"""
        self.should_stop = True


class KrakenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.typing_thread = None
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.snippets = self.load_config()
        self.init_ui()
        
        # Check X11 session
        self.check_display_server()
    
    def check_display_server(self):
        """Check if running on X11"""
        session_type = os.environ.get('XDG_SESSION_TYPE', 'unknown')
        if session_type == 'wayland':
            QMessageBox.warning(
                self,
                "⚠️ Wayland Detected",
                "You're on Wayland. KRAKEN requires X11 for reliable typing.\n\n"
                "To switch:\n"
                "1. Log out\n"
                "2. Click the gear icon at login\n"
                "3. Select 'Ubuntu on Xorg'\n\n"
                "KRAKEN may not work properly on Wayland."
            )
        elif not XLIB_AVAILABLE:
            self.status_label.setText("⚠️ python-xlib not found (install: sudo apt install python3-xlib)")
    
    def get_active_window_name(self):
        """Get active window name using X11"""
        if not XLIB_AVAILABLE:
            return None
        
        try:
            disp = display.Display()
            window = disp.get_input_focus().focus
            wmname = window.get_wm_name()
            wmclass = window.get_wm_class()
            return (wmname, wmclass)
        except Exception:
            return None
    
    def load_config(self):
        """Load snippets"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        """Save snippets"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.snippets, f, indent=2)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save: {e}")
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("🐙 KRAKEN - The Devourer of Paste Restrictions")
        self.setMinimumSize(700, 650)
        self.resize(850, 750)
        
        # Apply dark theme
        self.set_dark_theme()
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(25, 20, 25, 20)
        
        # Header
        title = QLabel("🐙 KRAKEN")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #00d9ff, stop:1 #00ffc8);
            margin-bottom: 2px;
            padding: 5px;
        """)
        main_layout.addWidget(title)
        
        subtitle = QLabel("The Devourer of Paste Restrictions")
        subtitle_font = QFont("Arial", 10)
        subtitle_font.setItalic(True)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #00ffc8; margin-bottom: 5px;")
        main_layout.addWidget(subtitle)
        
        # Display server indicator
        session_type = os.environ.get('XDG_SESSION_TYPE', 'X11')
        display_label = QLabel(f"📺 {session_type.upper()}")
        display_label.setFont(QFont("Monospace", 8))
        if session_type == 'wayland':
            display_label.setStyleSheet("""
                color: #ff4444;
                background-color: rgba(255, 68, 68, 0.1);
                border: 1px solid #ff4444;
                border-radius: 12px;
                padding: 4px 12px;
            """)
        else:
            display_label.setStyleSheet("""
                color: #00ff88;
                background-color: rgba(0, 255, 136, 0.1);
                border: 1px solid #00ff88;
                border-radius: 12px;
                padding: 4px 12px;
            """)
        display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(display_label)
        
        # Text input section
        main_layout.addSpacing(8)
        text_label = QLabel("⚡ Text to Unleash:")
        text_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        text_label.setStyleSheet("color: #00d9ff;")
        main_layout.addWidget(text_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Monospace", 10))
        self.text_edit.setPlaceholderText("Enter or paste your text here...\n\nKRAKEN will simulate typing to bypass paste restrictions.")
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #0f1f35;
                color: #e0f4ff;
                border: 2px solid #1a4a7a;
                border-radius: 6px;
                padding: 10px;
                selection-background-color: #00d9ff;
                selection-color: #001122;
            }
            QTextEdit:focus {
                border: 2px solid #00d9ff;
                background-color: #132a47;
            }
        """)
        self.text_edit.setMinimumHeight(120)
        main_layout.addWidget(self.text_edit)
        
        # Controls container - Clean organized layout
        main_layout.addSpacing(8)
        controls_box = QGroupBox()
        controls_box.setMinimumHeight(100)
        controls_box.setStyleSheet("""
            QGroupBox {
                background-color: #0d1f36;
                border: 1px solid #1a4a7a;
                border-radius: 6px;
            }
        """)
        
        controls_main = QVBoxLayout(controls_box)
        controls_main.setSpacing(16)
        controls_main.setContentsMargins(22, 20, 22, 22)
        
        # Top row: Speed and Delay side by side
        top_row = QHBoxLayout()
        top_row.setSpacing(25)
        
        # Speed control (left column)
        speed_container = QVBoxLayout()
        speed_container.setSpacing(8)
        
        speed_label = QLabel("⚡ Speed")
        speed_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        speed_label.setStyleSheet("color: #00d9ff;")
        speed_container.addWidget(speed_label)
        
        speed_control = QHBoxLayout()
        speed_control.setSpacing(10)
        
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setMinimumHeight(32)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #0a1a2e;
                border: 1px solid #1a4a7a;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00d9ff;
                width: 20px;
                height: 20px;
                margin: -6px 0;
                border-radius: 10px;
                border: 2px solid #00ffc8;
            }
            QSlider::handle:horizontal:hover {
                background: #00ffc8;
            }
        """)
        speed_control.addWidget(self.speed_slider, 1)
        
        self.speed_value = QLabel("50")
        self.speed_value.setFont(QFont("Monospace", 11, QFont.Weight.Bold))
        self.speed_value.setStyleSheet("""
            color: #00ffc8;
            background-color: #0a1a2e;
            border: 1px solid #1a4a7a;
            border-radius: 4px;
            padding: 6px 10px;
        """)
        self.speed_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.speed_value.setFixedWidth(45)
        speed_control.addWidget(self.speed_value)
        
        speed_container.addLayout(speed_control)
        top_row.addLayout(speed_container, 1)
        
        # Delay control (right column)
        delay_container = QVBoxLayout()
        delay_container.setSpacing(8)
        
        delay_label = QLabel("⏰ Delay")
        delay_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        delay_label.setStyleSheet("color: #00d9ff;")
        delay_container.addWidget(delay_label)
        
        delay_control = QHBoxLayout()
        delay_control.setSpacing(8)
        
        self.countdown_combo = QComboBox()
        self.countdown_combo.addItems(['0', '1', '2', '3', '5', '10'])
        self.countdown_combo.setCurrentText('3')
        self.countdown_combo.setFixedWidth(70)
        self.countdown_combo.setMinimumHeight(32)
        self.countdown_combo.setStyleSheet("""
            QComboBox {
                background-color: #0a1a2e;
                color: #e0f4ff;
                border: 1px solid #1a4a7a;
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 10pt;
                font-weight: bold;
            }
            QComboBox:hover {
                border: 1px solid #00d9ff;
                background-color: #132a47;
            }
            QComboBox::drop-down {
                border: none;
                width: 22px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #00d9ff;
            }
            QComboBox QAbstractItemView {
                background-color: #0a1a2e;
                color: #e0f4ff;
                border: 1px solid #00d9ff;
                selection-background-color: #00d9ff;
                selection-color: #001122;
                padding: 6px;
            }
        """)
        delay_control.addWidget(self.countdown_combo)
        
        delay_sec = QLabel("seconds")
        delay_sec.setStyleSheet("color: #6a9abf; font-size: 9pt;")
        delay_control.addWidget(delay_sec)
        delay_control.addStretch()
        
        delay_container.addLayout(delay_control)
        top_row.addLayout(delay_container, 1)
        
        controls_main.addLayout(top_row)
        
        self.speed_slider.valueChanged.connect(lambda v: self.speed_value.setText(str(v)))
        
        main_layout.addWidget(controls_box)
        main_layout.addSpacing(18)
        
        
        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.start_btn = QPushButton("🐙 UNLEASH KRAKEN")
        self.start_btn.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.start_btn.setMinimumHeight(42)
        self.start_btn.setMaximumWidth(350)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00e5ff, stop:1 #00b8d4);
                color: #001122;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00ffc8, stop:1 #00d9a0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #00b8d4, stop:1 #008fa5);
            }
            QPushButton:disabled {
                background-color: #1a3a5f;
                color: #4a6a8f;
            }
        """)
        self.start_btn.clicked.connect(self.start_typing)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("🛑 STOP")
        self.stop_btn.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        self.stop_btn.setMinimumHeight(42)
        self.stop_btn.setMaximumWidth(200)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff4444, stop:1 #cc0000);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6666, stop:1 #ff2222);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #cc0000, stop:1 #990000);
            }
            QPushButton:disabled {
                background-color: #1a3a5f;
                color: #4a6a8f;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_typing)
        button_layout.addWidget(self.stop_btn)
        
        main_layout.addLayout(button_layout)
        
        # Options row below buttons
        options_layout = QHBoxLayout()
        options_layout.setSpacing(30)
        
        self.human_check = QCheckBox("🤖 Human-like variations")
        self.human_check.setChecked(True)
        self.human_check.setFont(QFont("Arial", 10))
        self.human_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.human_check.setStyleSheet("""
            QCheckBox {
                color: #e0f4ff;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 1px solid #1a4a7a;
                border-radius: 4px;
                background-color: #0a1a2e;
            }
            QCheckBox::indicator:hover {
                border: 1px solid #00d9ff;
            }
            QCheckBox::indicator:checked {
                background: #00d9ff;
                border: 1px solid #00ffc8;
            }
        """)
        options_layout.addWidget(self.human_check)
        
        self.typo_check = QCheckBox("❌ Random typos")
        self.typo_check.setChecked(False)
        self.typo_check.setFont(QFont("Arial", 10))
        self.typo_check.setCursor(Qt.CursorShape.PointingHandCursor)
        self.typo_check.setStyleSheet(self.human_check.styleSheet())
        options_layout.addWidget(self.typo_check)
        
        options_layout.addStretch()
        main_layout.addLayout(options_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(28)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1a4a7a;
                border-radius: 8px;
                text-align: center;
                color: #ffffff;
                font-size: 12pt;
                font-weight: bold;
                background-color: #0f1f35;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d9ff, stop:0.5 #00ffc8, stop:1 #00d9ff);
                border-radius: 6px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("🌊 Ready to unleash the Kraken...")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("""
            color: #00ffc8;
            background-color: rgba(0, 217, 255, 0.05);
            padding: 8px;
            border-radius: 4px;
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        main_layout.addWidget(self.status_label)
        
        # Snippets section
        snippets_group = QGroupBox("💾 Saved Snippets")
        snippets_group.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        snippets_group.setStyleSheet("""
            QGroupBox {
                color: #e0f4ff;
                border: 2px solid #00d9ff;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
        """)
        snippets_layout = QVBoxLayout()
        
        snippet_controls = QHBoxLayout()
        snippet_controls.setSpacing(12)
        
        self.snippet_combo = QComboBox()
        self.snippet_combo.setMinimumHeight(36)
        self.snippet_combo.setStyleSheet("""
            QComboBox {
                background-color: #0a1a2e;
                color: #e0f4ff;
                border: 1px solid #1a4a7a;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 10pt;
            }
            QComboBox:hover {
                border: 1px solid #00d9ff;
                background-color: #132a47;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #00d9ff;
            }
            QComboBox QAbstractItemView {
                background-color: #0a1a2e;
                color: #e0f4ff;
                border: 1px solid #00d9ff;
                selection-background-color: #00d9ff;
                selection-color: #001122;
                padding: 6px;
            }
        """)
        self.update_snippet_list()
        snippet_controls.addWidget(self.snippet_combo, 2)
        
        load_btn = QPushButton("📥 Load")
        load_btn.setMinimumHeight(36)
        load_btn.setMinimumWidth(90)
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a3a5f;
                color: #00d9ff;
                border: 2px solid #00d9ff;
                border-radius: 6px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #2a4a6f;
                border-color: #00ffc8;
            }
        """)
        load_btn.clicked.connect(self.load_snippet)
        snippet_controls.addWidget(load_btn)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setMinimumHeight(36)
        save_btn.setMinimumWidth(90)
        save_btn.setStyleSheet(load_btn.styleSheet())
        save_btn.clicked.connect(self.save_snippet)
        snippet_controls.addWidget(save_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setMinimumHeight(36)
        delete_btn.setMinimumWidth(100)
        delete_btn.setStyleSheet(load_btn.styleSheet())
        delete_btn.clicked.connect(self.delete_snippet)
        snippet_controls.addWidget(delete_btn)
        
        snippets_layout.addLayout(snippet_controls)
        snippets_group.setLayout(snippets_layout)
        main_layout.addWidget(snippets_group)
        
        # Footer
        footer = QLabel("Built with PySide6 • X11 Required • Ubuntu Native")
        footer.setFont(QFont("Arial", 8))
        footer.setStyleSheet("color: #4a6a8f; margin-top: 10px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(footer)
    
    def set_dark_theme(self):
        """Apply dark theme"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(13, 31, 54))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(224, 244, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(19, 42, 71))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(26, 58, 95))
        palette.setColor(QPalette.ColorRole.Text, QColor(224, 244, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(26, 58, 95))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 217, 255))
        self.setPalette(palette)
    
    def start_typing(self):
        """Start typing"""
        text = self.text_edit.toPlainText()
        
        if not text.strip():
            QMessageBox.warning(self, "Empty Text", "Please enter text to type!")
            return
        
        # Check active window
        if XLIB_AVAILABLE:
            window_info = self.get_active_window_name()
            if window_info:
                wmname, wmclass = window_info
                print(f"[INFO] Active window: {wmname} ({wmclass})")
        
        speed = self.speed_slider.value()
        countdown = int(self.countdown_combo.currentText())
        human_like = self.human_check.isChecked()
        typos = self.typo_check.isChecked()
        
        self.typing_thread = TypingThread(text, speed, countdown, human_like, typos)
        self.typing_thread.progress.connect(self.progress_bar.setValue)
        self.typing_thread.status.connect(self.status_label.setText)
        self.typing_thread.finished.connect(self.typing_finished)
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # CRITICAL: Minimize window so CLI can type into target application
        self.showMinimized()
        
        self.typing_thread.start()
    
    def stop_typing(self):
        """Stop typing"""
        if self.typing_thread:
            self.typing_thread.stop()
            self.status_label.setText("🛑 Kraken stopped!")
    
    def typing_finished(self):
        """Reset UI after typing"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Restore window
        self.showNormal()
        self.activateWindow()
    
    def load_snippet(self):
        """Load selected snippet"""
        name = self.snippet_combo.currentText()
        if name and name in self.snippets:
            self.text_edit.setPlainText(self.snippets[name])
            self.status_label.setText(f"📥 Loaded: {name}")
    
    def save_snippet(self):
        """Save current text as snippet"""
        text = self.text_edit.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Empty", "Cannot save empty snippet!")
            return
        
        name, ok = QInputDialog.getText(self, "Save Snippet", "Enter snippet name:")
        if ok and name:
            self.snippets[name] = text
            self.save_config()
            self.update_snippet_list()
            self.snippet_combo.setCurrentText(name)
            self.status_label.setText(f"💾 Saved: {name}")
    
    def delete_snippet(self):
        """Delete selected snippet"""
        name = self.snippet_combo.currentText()
        if not name or name not in self.snippets:
            return
        
        reply = QMessageBox.question(
            self, "Delete Snippet",
            f"Delete '{name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.snippets[name]
            self.save_config()
            self.update_snippet_list()
            self.status_label.setText(f"🗑️ Deleted: {name}")
    
    def update_snippet_list(self):
        """Update snippet dropdown"""
        current = self.snippet_combo.currentText()
        self.snippet_combo.clear()
        self.snippet_combo.addItems(sorted(self.snippets.keys()))
        if current in self.snippets:
            self.snippet_combo.setCurrentText(current)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("KRAKEN")
    
    window = KrakenWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
