#!/usr/bin/env python3
"""
KRAKEN - The Devourer of Paste Restrictions
A typing automation tool that simulates human-like keyboard input
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import threading
import time
import random
from pynput.keyboard import Controller, Key


class KrakenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐙 KRAKEN - The Devourer of Paste Restrictions")
        self.root.geometry("750x650")
        self.root.resizable(False, False)
        
        # Theme colors
        self.colors = {
            'bg_dark': '#0a1628',
            'bg_medium': '#132a47',
            'accent_cyan': '#00d9ff',
            'accent_teal': '#00ffc8',
            'text': '#e0f4ff',
            'danger': '#ff3366'
        }
        
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Keyboard controller
        self.keyboard = Controller()
        
        # State
        self.is_typing = False
        self.pause_typing = False
        self.typing_thread = None
        
        # Config
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self.snippets = self.load_config()
        
        self.build_ui()
    
    def load_config(self):
        """Load snippets from config file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        """Save snippets to config file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.snippets, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")
    
    def build_ui(self):
        """Build the user interface"""
        
        # Header
        header = tk.Frame(self.root, bg=self.colors['bg_dark'])
        header.pack(pady=15, fill='x')
        
        tk.Label(
            header,
            text="🐙 KRAKEN",
            font=('Arial', 26, 'bold'),
            fg=self.colors['accent_cyan'],
            bg=self.colors['bg_dark']
        ).pack()
        
        tk.Label(
            header,
            text="The Devourer of Paste Restrictions",
            font=('Arial', 10, 'italic'),
            fg=self.colors['accent_teal'],
            bg=self.colors['bg_dark']
        ).pack()
        
        # Main container
        container = tk.Frame(self.root, bg=self.colors['bg_dark'])
        container.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Text input section
        tk.Label(
            container,
            text="⚡ Text to Unleash:",
            font=('Arial', 11, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        ).pack(anchor='w', pady=(0, 5))
        
        # Text widget with frame for border effect
        text_frame = tk.Frame(container, bg=self.colors['accent_cyan'])
        text_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.text_area = tk.Text(
            text_frame,
            height=12,
            font=('Monospace', 10),
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            insertbackground=self.colors['accent_cyan'],
            relief='flat',
            padx=5,
            pady=5,
            wrap='word'
        )
        self.text_area.pack(padx=2, pady=2, fill='both', expand=True)
        
        # Controls
        controls = tk.Frame(container, bg=self.colors['bg_dark'])
        controls.pack(fill='x', pady=10)
        
        # Left side - countdown and speed
        left_controls = tk.Frame(controls, bg=self.colors['bg_dark'])
        left_controls.pack(side='left')
        
        # Countdown
        tk.Label(
            left_controls,
            text="⏱️ Countdown:",
            font=('Arial', 9, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        ).pack(side='left', padx=(0, 5))
        
        self.countdown_var = tk.StringVar(value="3")
        countdown = ttk.Combobox(
            left_controls,
            textvariable=self.countdown_var,
            values=['0', '3', '5', '10', '15'],
            width=4,
            state='readonly'
        )
        countdown.pack(side='left', padx=(0, 3))
        
        tk.Label(
            left_controls,
            text="sec",
            font=('Arial', 8),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        ).pack(side='left', padx=(0, 15))
        
        # Speed
        tk.Label(
            left_controls,
            text="🚀 Speed:",
            font=('Arial', 9, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        ).pack(side='left', padx=(0, 5))
        
        self.speed_var = tk.IntVar(value=50)
        speed_slider = tk.Scale(
            left_controls,
            from_=1,
            to=100,
            orient='horizontal',
            variable=self.speed_var,
            length=140,
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            troughcolor=self.colors['bg_dark'],
            highlightthickness=0,
            command=self.update_speed_label
        )
        speed_slider.pack(side='left', padx=(0, 5))
        
        self.speed_label = tk.Label(
            left_controls,
            text="Medium",
            font=('Arial', 8),
            fg=self.colors['accent_cyan'],
            bg=self.colors['bg_dark'],
            width=9
        )
        self.speed_label.pack(side='left')
        
        # Options
        options = tk.Frame(container, bg=self.colors['bg_dark'])
        options.pack(fill='x', pady=5)
        
        self.human_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            options,
            text="🎭 Human-like variations",
            variable=self.human_var,
            font=('Arial', 9),
            fg=self.colors['text'],
            bg=self.colors['bg_dark'],
            selectcolor=self.colors['bg_medium'],
            activebackground=self.colors['bg_dark']
        ).pack(anchor='w')
        
        self.typo_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            options,
            text="💥 Occasional typos (ultra-realistic)",
            variable=self.typo_var,
            font=('Arial', 9),
            fg=self.colors['text'],
            bg=self.colors['bg_dark'],
            selectcolor=self.colors['bg_medium'],
            activebackground=self.colors['bg_dark']
        ).pack(anchor='w')
        
        # Action buttons
        buttons = tk.Frame(container, bg=self.colors['bg_dark'])
        buttons.pack(fill='x', pady=15)
        
        self.start_btn = tk.Button(
            buttons,
            text="⚡ UNLEASH KRAKEN",
            font=('Arial', 11, 'bold'),
            bg=self.colors['accent_cyan'],
            fg=self.colors['bg_dark'],
            activebackground=self.colors['accent_teal'],
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.start_typing
        )
        self.start_btn.pack(side='left', padx=(0, 8))
        
        self.pause_btn = tk.Button(
            buttons,
            text="⏸️ PAUSE",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            relief='flat',
            padx=15,
            pady=8,
            state='disabled',
            command=self.toggle_pause
        )
        self.pause_btn.pack(side='left', padx=(0, 8))
        
        self.stop_btn = tk.Button(
            buttons,
            text="🛑 STOP",
            font=('Arial', 10, 'bold'),
            bg=self.colors['danger'],
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            state='disabled',
            command=self.stop_typing
        )
        self.stop_btn.pack(side='left')
        
        # Progress
        self.progress = ttk.Progressbar(
            container,
            mode='determinate',
            length=400
        )
        self.progress.pack(fill='x', pady=8)
        
        # Status
        self.status = tk.Label(
            container,
            text="🌊 Ready to devour paste restrictions...",
            font=('Arial', 9),
            fg=self.colors['accent_teal'],
            bg=self.colors['bg_dark']
        )
        self.status.pack(pady=5)
        
        # Snippets
        snippets_frame = tk.LabelFrame(
            container,
            text="📚 Saved Snippets",
            font=('Arial', 9, 'bold'),
            fg=self.colors['text'],
            bg=self.colors['bg_dark']
        )
        snippets_frame.pack(fill='x', pady=10)
        
        snippet_controls = tk.Frame(snippets_frame, bg=self.colors['bg_dark'])
        snippet_controls.pack(fill='x', padx=8, pady=8)
        
        self.snippet_var = tk.StringVar()
        self.snippet_combo = ttk.Combobox(
            snippet_controls,
            textvariable=self.snippet_var,
            values=list(self.snippets.keys()),
            width=22,
            state='readonly'
        )
        self.snippet_combo.pack(side='left', padx=(0, 5))
        
        tk.Button(
            snippet_controls,
            text="📥 Load",
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            relief='flat',
            padx=10,
            pady=2,
            command=self.load_snippet
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            snippet_controls,
            text="💾 Save",
            bg=self.colors['bg_medium'],
            fg=self.colors['text'],
            relief='flat',
            padx=10,
            pady=2,
            command=self.save_snippet
        ).pack(side='left', padx=(0, 5))
        
        tk.Button(
            snippet_controls,
            text="🗑️ Delete",
            bg=self.colors['danger'],
            fg='white',
            relief='flat',
            padx=10,
            pady=2,
            command=self.delete_snippet
        ).pack(side='left')
        
        # Footer
        tk.Label(
            self.root,
            text="⚠️ Click on target field after starting, Kraken will type there",
            font=('Arial', 8, 'italic'),
            fg='#888888',
            bg=self.colors['bg_dark']
        ).pack(pady=(0, 10))
    
    def update_speed_label(self, value):
        """Update speed label"""
        speed = int(float(value))
        labels = [(20, "Slow"), (40, "Relaxed"), (60, "Medium"), (80, "Fast"), (101, "BEAST MODE")]
        label = next(text for threshold, text in labels if speed < threshold)
        self.speed_label.config(text=label)
    
    def calculate_delay(self):
        """Calculate typing delay"""
        speed = self.speed_var.get()
        base = 0.2 - (speed / 100) * 0.19
        
        if self.human_var.get():
            return max(0.01, base + random.uniform(-0.02, 0.03))
        return base
    
    def should_typo(self):
        """Check if should add typo"""
        return self.typo_var.get() and random.random() < 0.02
    
    def start_typing(self):
        """Start typing"""
        text = self.text_area.get('1.0', 'end-1c')
        
        if not text.strip():
            messagebox.showwarning("Empty Text", "Please enter text to type!")
            return
        
        self.is_typing = True
        self.pause_typing = False
        
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal', text="⏸️ PAUSE")
        self.stop_btn.config(state='normal')
        self.progress['value'] = 0
        
        self.typing_thread = threading.Thread(target=self.type_text, args=(text,), daemon=True)
        self.typing_thread.start()
    
    def type_text(self, text):
        """Type text with delays"""
        # Countdown
        countdown = int(self.countdown_var.get())
        for i in range(countdown, 0, -1):
            if not self.is_typing:
                return
            self.status.config(text=f"🐙 Kraken awakening in {i}...")
            time.sleep(1)
        
        self.status.config(text="🌊 KRAKEN UNLEASHED! Typing...")
        
        total = len(text)
        for idx, char in enumerate(text):
            if not self.is_typing:
                break
            
            # Handle pause
            while self.pause_typing and self.is_typing:
                time.sleep(0.1)
            
            if not self.is_typing:
                break
            
            # Simulate typo
            if self.should_typo() and char.isalpha():
                wrong = random.choice('qwertyuiopasdfghjklzxcvbnm')
                self.keyboard.type(wrong)
                time.sleep(self.calculate_delay() * 0.5)
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
                time.sleep(self.calculate_delay() * 0.3)
            
            # Type character
            try:
                self.keyboard.type(char)
            except:
                pass
            
            # Update progress
            self.progress['value'] = ((idx + 1) / total) * 100
            time.sleep(self.calculate_delay())
        
        if self.is_typing:
            self.status.config(text="✅ Kraken devoured all restrictions!")
            self.progress['value'] = 100
        
        self.is_typing = False
        self.root.after(0, self.reset_ui)
    
    def toggle_pause(self):
        """Toggle pause/resume"""
        self.pause_typing = not self.pause_typing
        if self.pause_typing:
            self.pause_btn.config(text="▶️ RESUME")
            self.status.config(text="⏸️ Kraken paused...")
        else:
            self.pause_btn.config(text="⏸️ PAUSE")
            self.status.config(text="🌊 Typing resumed...")
    
    def stop_typing(self):
        """Stop typing"""
        self.is_typing = False
        self.pause_typing = False
        self.status.config(text="🛑 Kraken stopped!")
    
    def reset_ui(self):
        """Reset UI after typing"""
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled', text="⏸️ PAUSE")
        self.stop_btn.config(state='disabled')
    
    def load_snippet(self):
        """Load selected snippet"""
        name = self.snippet_var.get()
        if name and name in self.snippets:
            self.text_area.delete('1.0', 'end')
            self.text_area.insert('1.0', self.snippets[name])
            self.status.config(text=f"📥 Loaded: {name}")
    
    def save_snippet(self):
        """Save current text as snippet"""
        text = self.text_area.get('1.0', 'end-1c')
        if not text.strip():
            messagebox.showwarning("Empty", "Cannot save empty snippet!")
            return
        
        # Simple dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Snippet")
        dialog.geometry("300x100")
        dialog.configure(bg=self.colors['bg_dark'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(
            dialog,
            text="Snippet Name:",
            bg=self.colors['bg_dark'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        entry = tk.Entry(dialog, width=30)
        entry.pack(pady=5)
        entry.focus()
        
        def save():
            name = entry.get().strip()
            if name:
                self.snippets[name] = text
                self.save_config()
                self.snippet_combo['values'] = list(self.snippets.keys())
                self.status.config(text=f"💾 Saved: {name}")
                dialog.destroy()
        
        tk.Button(
            dialog,
            text="Save",
            command=save,
            bg=self.colors['accent_cyan'],
            fg=self.colors['bg_dark'],
            relief='flat',
            padx=20
        ).pack(pady=10)
        
        entry.bind('<Return>', lambda e: save())
    
    def delete_snippet(self):
        """Delete selected snippet"""
        name = self.snippet_var.get()
        if name and name in self.snippets:
            if messagebox.askyesno("Delete", f"Delete '{name}'?"):
                del self.snippets[name]
                self.save_config()
                self.snippet_combo['values'] = list(self.snippets.keys())
                self.snippet_var.set('')
                self.status.config(text=f"🗑️ Deleted: {name}")


def main():
    root = tk.Tk()
    app = KrakenApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
