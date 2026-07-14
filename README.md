# 🐙 KRAKEN - The Devourer of Paste Restrictions

**Ubuntu Native Edition - Built with PySide6**

A beast-mode typing automation tool that simulates human-like keyboard input to bypass paste restrictions on websites and applications. Fully migrated to PySide6 for seamless Ubuntu integration.

## 🌊 Features

- **Human-like Typing**: Random micro-delays between keystrokes for realistic simulation
- **Countdown Timer**: Configurable delay (0-10 seconds) before typing starts
- **Speed Control**: Adjustable typing speed from 1 to 100
- **Typo Simulation**: Optional realistic typos with automatic correction
- **Snippet Library**: Save and load frequently used text snippets
- **Progress Tracking**: Visual progress bar and status updates
- **Modern Dark Theme**: Deep sea Kraken aesthetic with cyan/teal gradients
- **X11 Native**: Optimized for Ubuntu with X11 session detection
- **Auto-minimize**: Window minimizes during typing to avoid focus issues

## 📦 Installation

### Prerequisites
Ubuntu 22.04 LTS or later with X11 session (required)

### 1. Install System Dependencies
```bash
sudo apt update
sudo apt install -y python3 python3-pip libxcb-cursor0
```

### 2. Install Python Dependencies
```bash
cd ~/tools/kraken
pip3 install --user -r requirements.txt
```

The `requirements.txt` includes:
- `pynput>=1.7.6` - Keyboard input simulation
- `python-xlib>=0.31` - X11 window detection

PySide6 will be installed automatically via pip.

## 🚀 Usage

### PySide6 GUI (Main Interface)
```bash
cd ~/tools/kraken
python3 kraken_pyside.py
```

**Using the GUI:**
1. **Enter or paste text** in the text area
2. **Configure controls**:
   - **Speed**: Slide from 1 (slow) to 100 (fast)
   - **Delay**: Choose countdown (0, 1, 2, 3, 5, or 10 seconds)
3. **Optional settings**:
   - ✅ Human-like variations (adds natural rhythm)
   - ✅ Random typos (with auto-correction)
4. **Click "🐙 UNLEASH KRAKEN"**
5. **Quickly click the target field** where you want text typed
6. **Watch Kraken work!** - Window auto-minimizes during typing

### CLI Version (Headless/Script Usage)
```bash
# Basic usage
python3 kraken_cli.py --text "Your text here"

# From file
cat myfile.txt | python3 kraken_cli.py

# Fast typing with 5 second countdown
python3 kraken_cli.py --text "Quick text" --speed 90 --countdown 5

# Ultra-realistic with typos
python3 kraken_cli.py --text "Message" --human-like --typos --speed 60

# Quiet mode (no output)
python3 kraken_cli.py --text "Silent typing" --quiet

# See all options
python3 kraken_cli.py --help
```

**CLI Options:**
- `-t, --text` - Text to type
- `-s, --speed` - Typing speed (1-100, default: 50)
- `-c, --countdown` - Delay before typing (0-15 seconds, default: 3)
- `--human-like` / `--no-human-like` - Natural variations (default: on)
- `--typos` - Enable realistic typos
- `--quiet` - Suppress output messages

## 💾 Snippets

**Save frequently used text:**
1. Enter text in the main text area
2. Click "💾 Save"
3. Enter a name for your snippet
4. Snippet saved to `config.json`

**Load saved snippets:**
1. Select snippet from dropdown
2. Click "📥 Load"
3. Text appears in text area

**Delete snippets:**
1. Select snippet from dropdown
2. Click "🗑️ Delete"

Snippets persist between sessions and are stored in JSON format.

## ⚙️ How It Works

**Architecture:**
- **GUI Layer**: PySide6 (Qt for Python) provides the modern interface
- **Typing Engine**: pynput library simulates keyboard events at OS level
- **Hybrid Design**: GUI spawns CLI subprocess to avoid QThread conflicts with pynput
- **X11 Integration**: python-xlib detects active windows and session type

**Why it works everywhere:**
- ✅ Operates at OS keyboard driver level
- ✅ Bypasses JavaScript paste blockers
- ✅ Works with ANY application (browsers, forms, terminals, VMs)
- ✅ Simulates actual keyboard events
- ✅ Undetectable by most paste-blocking mechanisms

## 🎮 Speed Settings

| Range | Description | Use Case |
|-------|-------------|----------|
| 1-20 | Slow & Deliberate | Long forms, careful input |
| 21-40 | Relaxed Pace | General usage |
| 41-60 | Medium Speed | Standard forms |
| 61-80 | Fast Typing | Quick input |
| 81-100 | BEAST MODE | Maximum speed |

**Recommen & Best Practices

1. **Countdown is crucial**: Use 3-5 seconds to give yourself time to click the target field
2. **Test the speed**: Try different speeds on test fields first - some apps can't handle max speed
3. **Browser forms**: Excels at forms that block Ctrl+V or right-click paste
4. **Focus matters**: Target field MUST have focus when typing begins
5. **X11 required**: Won't work on Wayland sessions (app will warn you)
6. **Window minimizes**: GUI auto-minimizes during typing to prevent focus conflicts
7. **Long texts**: Use medium speed (40-60) for texts over 500 characters

## 🐛 Troubleshooting

**"Module not found: PySide6"**:
```bash
pip3 install --user PySide6
```

**"xcb plugin" error**:
```bash
sudo apt install libxcb-cursor0
```

**"python-xlib not found"**:
```bash
pip3 install --user python-xlib
```

**Typing doesn't work**:
- Ensure you're on X11 (not Wayland): `echo $XDG_SESSION_TYPE`
- Click target field AFTER pressing Unleash button
- Wait for countdown to complete
- Check terminal for error messages

**Window won't minimize**:
- Normal behavior - CLI subprocess handles typing
- Check if xdotool is installed: `sudo apt install xdotool`
� Project Structure

```
kraken/
├── kraken_pyside.py    # Main PySide6 GUI application
├── kraken_cli.py       # CLI backend (called by GUI)
├── requirements.txt    # Python dependencies
├── config.json         # Saved snippets (auto-created)
└── README.md          # This file
```

## 🤝 Contributing

Feel free to fork and improve! Areas for enhancement:
- Wayland support (challenging due to security restrictions)
- Custom typing patterns/profiles
- Hotkey support for quick activation
- Multi-language keyboard layouts
- Clipboard monitoring mode

## 📜 License

Free to use and modify. Part of the beast-mode automation tools collection.

---

**Built with PySide6 • X11 Required • Ubuntu Native***Language**: Python 3.10+
- **Platform**: Ubuntu 22.04 LTS (X11 session required)

**Why PySide6?**
- Official Qt bindings (LGPL licensed)
- Native Ubuntu/Linux integration
- Better maintained than PyQt5
- Proper X11 support out of the box

## 🔮 Known Limitations

- ❌ Does not work on Wayland sessions (X11 only)
- ❌ Cannot type special characters not on keyboard layout
- ❌ Some protected fields (password managers) may still block input
- ❌ Very fast speeds (>90) may cause buffer overflow on slow app
**Permission issues on Linux**:
```bash
# May need to run with appropriate permissions for input simulation
# Or add your user to the input group
```

**Typing doesn't start**:
- Make sure you clicked on the target field after pressing "Unleash"
- Check that the countdown finished
- Verify the application window has focus

## 🔮 Future Enhancements

- Global hotkey support
- Multiple language support
- Clipboard monitoring
- Auto-detect and break text into natural chunks
- Custom typing patterns/profiles

## 📜 License

Free to use and modify. Part of the beast-mode tools collection.

---

**Created with 🐙 by the depths of automation**
