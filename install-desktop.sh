#!/bin/bash
# Install Kraken as a Linux Desktop Application

echo "🐙 Installing KRAKEN as a Linux Application..."
echo "=============================================="
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make launcher executable
chmod +x "$SCRIPT_DIR/kraken-launcher.sh"

# Create desktop applications directory if it doesn't exist
mkdir -p ~/.local/share/applications

# Copy desktop file to user applications directory
cp "$SCRIPT_DIR/kraken.desktop" ~/.local/share/applications/

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now launch Kraken from:"
echo "  • Your application menu (search for 'Kraken')"
echo "  • The Activities overview (press Super key and type 'Kraken')"
echo ""
echo "To uninstall, run: ./uninstall-desktop.sh"
