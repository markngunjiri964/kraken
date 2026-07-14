#!/bin/bash
# Uninstall Kraken Desktop Application

echo "🐙 Uninstalling KRAKEN Desktop Application..."

# Remove desktop file
rm -f ~/.local/share/applications/kraken.desktop

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications
fi

echo "✅ Uninstalled successfully!"
