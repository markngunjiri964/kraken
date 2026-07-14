#!/usr/bin/env python3
"""
KRAKEN - The Devourer of Paste Restrictions
PyQt5 Edition - Stable and Professional
"""

import sys
import json
import os
import time
import random
import subprocess
import tempfile
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QTextEdit, QPushButton, 
                             QSlider, QComboBox, QCheckBox, QProgressBar,
                             QMessageBox, QInputDialog, QGroupBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QProcess
from PyQt5.QtGui import QFont, QPalette, QColor


class TypingThread(QThread):
    """Thread for typing text using CLI subprocess"""
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal()
    
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
        # Write text to temp file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
            f.write(self.text)
            temp_file = f.name
        
        try:
            # Build command
            cli_path = os.path.join(os.path.dirname(__file__), 'kraken_cli.py')
            cmd = [
                'python3', cli_path,
                '--file', temp_file,
                '--speed', str(self.speed),
                '--countdown', str(self.countdown)
            ]
            
            if self.human_like:
                cmd.append('--human-like')
            if self.typos:
                cmd.append('--typos')
            
            # Countdown manually
            for i in range(self.countdown, 0, -1):
                if self.should_stop:
                    return
                self.status.emit(f"🐙 Kraken awakening in {i}...")
                time.sleep(1)
            
            self.status.emit("🌊 KRAKEN UNLEASHED! Typing...")
            
            # Run CLI version
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
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
            
            if process.returncode == 0:
                self.status.emit("✅ Kraken devoured all restrictions!")
                self.progress.emit(100)
            else:
                self.status.emit(f"❌ Error: {stderr.strip()}")
        
        except Exception as e:
            self.status.emit(f"❌ Error: {str(e)}")
        
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_file)
            except:
                pass
            
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
        self.setMinimumSize(900, 800)
        self.resize(950, 850)
        
        # Apply dark theme
        self.set_dark_theme()
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 25, 30, 25)
        
        # Header
        title = QLabel("🐙 KRAKEN")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00d9ff; margin-bottom: 5px;")
        main_layout.addWidget(title)
        
        subtitle = QLabel("The Devourer of Paste Restrictions")
        subtitle.setFont(QFont("Arial", 11, QFont.StyleItalic))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #00ffc8; margin-bottom: 20px;")
        main_layout.addWidget(subtitle)
        
        # Text input
        text_label = QLabel("⚡ Text to Unleash:")
        text_label.setFont(QFont("Arial", 12, QFont.Bold))
        text_label.setStyleSheet("color: #e0f4ff;")
        main_layout.addWidget(text_label)
        
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Monospace", 10))
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #132a47;
                color: #e0f4ff;
                border: 2px solid #00d9ff;
                border-radius: 6px;
                padding: 10px;
            }
        """)
        self.text_edit.setMinimumHeight(250)
        main_layout.addWidget(self.text_edit)
        
        # Controls container
        controls_box = QWidget()
        controls_box.setStyleSheet("""
            QWidget {
                background-color: #0d1f36;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        controls_layout = QVBoxLayout(controls_box)
        controls_layout.setSpacing(15)
        controls_layout.setContentsMargins(20, 18, 20, 18)
        
        # Row 1: Countdown and Speed
        row1 = QHBoxLayout()
        row1.setSpacing(15)
        
        # Countdown
        countdown_label = QLabel("⏱️ Countdown:")
        countdown_label.setFont(QFont("Arial", 10, QFont.Bold))
        countdown_label.setStyleSheet("color: #e0f4ff;")
        row1.addWidget(countdown_label)
        
        self.countdown_combo = QComboBox()
        self.countdown_combo.addItems(["0", "3", "5", "10", "15"])
        self.countdown_combo.setCurrentText("3")
        self.countdown_combo.setMinimumHeight(32)
        self.countdown_combo.setStyleSheet("""
            QComboBox {
                background-color: #1a3557;
                color: #e0f4ff;
                border: 1px solid #00d9ff;
                padding: 6px 10px;
                border-radius: 4px;
                min-width: 70px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid #00d9ff;
                margin-right: 8px;
            }
        """)
        row1.addWidget(self.countdown_combo)
        
        sec_label = QLabel("sec")
        sec_label.setStyleSheet("color: #e0f4ff;")
        row1.addWidget(sec_label)
        
        row1.addSpacing(40)
        
        # Speed
        speed_label = QLabel("🚀 Speed:")
        speed_label.setFont(QFont("Arial", 10, QFont.Bold))
        speed_label.setStyleSheet("color: #e0f4ff;")
        row1.addWidget(speed_label)
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(100)
        self.speed_slider.setValue(50)
        self.speed_slider.setMinimumWidth(200)
        self.speed_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #1a3557;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #00d9ff;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #00ffc8;
            }
        """)
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        row1.addWidget(self.speed_slider)
        
        self.speed_label = QLabel("Medium")
        self.speed_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.speed_label.setStyleSheet("color: #00d9ff; min-width: 100px;")
        row1.addWidget(self.speed_label)
        
        row1.addStretch()
        controls_layout.addLayout(row1)
        
        # Row 2: Checkboxes
        row2 = QHBoxLayout()
        row2.setSpacing(20)
        
        self.human_check = QCheckBox("🎭 Human-like variations")
        self.human_check.setChecked(True)
        self.human_check.setFont(QFont("Arial", 10))
        self.human_check.setStyleSheet("""
            QCheckBox {
                color: #e0f4ff;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #00d9ff;
                border-radius: 4px;
                background-color: #1a3557;
            }
            QCheckBox::indicator:checked {
                background-color: #00d9ff;
                image: none;
            }
        """)
        row2.addWidget(self.human_check)
        
        self.typo_check = QCheckBox("💥 Occasional typos (ultra-realistic)")
        self.typo_check.setFont(QFont("Arial", 10))
        self.typo_check.setStyleSheet("""
            QCheckBox {
                color: #e0f4ff;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid #00d9ff;
                border-radius: 4px;
                background-color: #1a3557;
            }
            QCheckBox::indicator:checked {
                background-color: #00d9ff;
                image: none;
            }
        """)
        row2.addWidget(self.typo_check)
        
        row2.addStretch()
        controls_layout.addLayout(row2)
        
        main_layout.addWidget(controls_box)
        
        # Buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(15)
        
        self.start_btn = QPushButton("⚡ UNLEASH KRAKEN")
        self.start_btn.setFont(QFont("Arial", 13, QFont.Bold))
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d9ff;
                color: #0a1628;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #00ffc8;
            }
            QPushButton:pressed {
                background-color: #00b8cc;
            }
        """)
        self.start_btn.clicked.connect(self.start_typing)
        button_row.addWidget(self.start_btn)
        
        self.pause_btn = QPushButton("⏸️ PAUSE")
        self.pause_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.pause_btn.setMinimumHeight(50)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setCursor(Qt.PointingHandCursor)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #1a3557;
                color: #e0f4ff;
                border: none;
                border-radius: 8px;
                padding: 15px 25px;
            }
            QPushButton:hover:enabled {
                background-color: #2a4567;
            }
            QPushButton:disabled {
                background-color: #0d1f36;
                color: #555555;
            }
        """)
        self.pause_btn.clicked.connect(self.toggle_pause)
        button_row.addWidget(self.pause_btn)
        
        self.stop_btn = QPushButton("🛑 STOP")
        self.stop_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setCursor(Qt.PointingHandCursor)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff3366;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 25px;
            }
            QPushButton:hover:enabled {
                background-color: #ff4477;
            }
            QPushButton:disabled {
                background-color: #0d1f36;
                color: #555555;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_typing)
        button_row.addWidget(self.stop_btn)
        
        button_row.addStretch()
        main_layout.addLayout(button_row)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(30)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #1a3557;
                border-radius: 6px;
                text-align: center;
                background-color: #0d1f36;
                color: #e0f4ff;
                font-size: 12px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                                   stop:0 #00d9ff, stop:1 #00ffc8);
                border-radius: 4px;
            }
        """)
        main_layout.addWidget(self.progress_bar)
        
        # Status
        self.status_label = QLabel("🌊 Ready to devour paste restrictions...")
        self.status_label.setFont(QFont("Arial", 11))
        self.status_label.setStyleSheet("color: #00ffc8; padding: 8px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Snippets
        snippets_group = QGroupBox("📚 Saved Snippets")
        snippets_group.setFont(QFont("Arial", 11, QFont.Bold))
        snippets_group.setStyleSheet("""
            QGroupBox {
                color: #e0f4ff;
                border: 2px solid #1a3557;
                border-radius: 8px;
                margin-top: 20px;
                padding-top: 20px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px;
            }
        """)
        snippets_layout = QHBoxLayout()
        snippets_layout.setSpacing(12)
        snippets_layout.setContentsMargins(15, 20, 15, 15)
        
        self.snippet_combo = QComboBox()
        self.snippet_combo.addItems(list(self.snippets.keys()))
        self.snippet_combo.setMinimumHeight(36)
        self.snippet_combo.setStyleSheet("""
            QComboBox {
                background-color: #1a3557;
                color: #e0f4ff;
                border: 1px solid #00d9ff;
                padding: 8px 12px;
                border-radius: 5px;
                min-width: 250px;
            }
        """)
        snippets_layout.addWidget(self.snippet_combo)
        
        load_btn = QPushButton("📥 Load")
        load_btn.setMinimumHeight(36)
        load_btn.setCursor(Qt.PointingHandCursor)
        load_btn.setStyleSheet(self.get_button_style("#1a3557"))
        load_btn.clicked.connect(self.load_snippet)
        snippets_layout.addWidget(load_btn)
        
        save_btn = QPushButton("💾 Save")
        save_btn.setMinimumHeight(36)
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(self.get_button_style("#1a3557"))
        save_btn.clicked.connect(self.save_snippet)
        snippets_layout.addWidget(save_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.setMinimumHeight(36)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet(self.get_button_style("#ff3366"))
        delete_btn.clicked.connect(self.delete_snippet)
        snippets_layout.addWidget(delete_btn)
        
        snippets_layout.addStretch()
        snippets_group.setLayout(snippets_layout)
        main_layout.addWidget(snippets_group)
        
        # Footer
        footer = QLabel("⚠️ Click on target field after starting, Kraken will type there")
        footer.setFont(QFont("Arial", 9, QFont.StyleItalic))
        footer.setStyleSheet("color: #888888; padding: 10px;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)
    
    def set_dark_theme(self):
        """Apply dark theme"""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#0a1628"))
        palette.setColor(QPalette.WindowText, QColor("#e0f4ff"))
        palette.setColor(QPalette.Base, QColor("#132a47"))
        palette.setColor(QPalette.AlternateBase, QColor("#0a1628"))
        palette.setColor(QPalette.Text, QColor("#e0f4ff"))
        palette.setColor(QPalette.Button, QColor("#132a47"))
        palette.setColor(QPalette.ButtonText, QColor("#e0f4ff"))
        self.setPalette(palette)
    
    def get_button_style(self, bg_color):
        """Get button style"""
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: #e0f4ff;
                border: none;
                border-radius: 5px;
                padding: 10px 18px;
                font-size: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #2a4567;
            }}
            QPushButton:pressed {{
                background-color: #0d2438;
            }}
        """
    
    def update_speed_label(self, value):
        """Update speed label"""
        if value < 20:
            text = "Slow"
        elif value < 40:
            text = "Relaxed"
        elif value < 60:
            text = "Medium"
        elif value < 80:
            text = "Fast"
        else:
            text = "BEAST MODE"
        self.speed_label.setText(text)
    
    def start_typing(self):
        """Start typing"""
        text = self.text_edit.toPlainText()
        
        if not text.strip():
            QMessageBox.warning(self, "Empty Text", "Please enter text to type!")
            return
        
        speed = self.speed_slider.value()
        countdown = int(self.countdown_combo.currentText())
        human_like = self.human_check.isChecked()
        typos = self.typo_check.isChecked()
        
        self.typing_thread = TypingThread(text, speed, countdown, human_like, typos)
        self.typing_thread.progress.connect(self.progress_bar.setValue)
        self.typing_thread.status.connect(self.status_label.setText)
        self.typing_thread.finished.connect(self.typing_finished)
        
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(False)  # Pause not supported with subprocess
        self.stop_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        
        # CRITICAL: Minimize window so CLI can type into target application
        self.showMinimized()
        
        self.typing_thread.start()
    
    def toggle_pause(self):
        """Pause not supported with subprocess method"""
        pass
    
    def stop_typing(self):
        """Stop typing"""
        if self.typing_thread:
            self.typing_thread.stop()
            self.status_label.setText("🛑 Kraken stopped!")
    
    def typing_finished(self):
        """Reset UI after typing"""
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setText("⏸️ PAUSE")
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
            self.snippet_combo.clear()
            self.snippet_combo.addItems(list(self.snippets.keys()))
            self.status_label.setText(f"💾 Saved: {name}")
    
    def delete_snippet(self):
        """Delete selected snippet"""
        name = self.snippet_combo.currentText()
        if name and name in self.snippets:
            reply = QMessageBox.question(
                self, "Delete", f"Delete '{name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                del self.snippets[name]
                self.save_config()
                self.snippet_combo.clear()
                self.snippet_combo.addItems(list(self.snippets.keys()))
                self.status_label.setText(f"🗑️ Deleted: {name}")


def main():
    app = QApplication(sys.argv)
    window = KrakenWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
