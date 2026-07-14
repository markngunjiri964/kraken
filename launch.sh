#!/bin/bash
# KRAKEN Launcher Script

echo "🐙 KRAKEN - The Devourer of Paste Restrictions"
echo "=============================================="
echo ""
echo "Which version would you like to run?"
echo ""
echo "1) GUI Version (requires X11/display)"
echo "2) CLI Version (works everywhere)"
echo "3) Exit"
echo ""
read -p "Select (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Launching GUI version..."
        python3 "$(dirname "$0")/kraken.py"
        ;;
    2)
        echo ""
        echo "Launching CLI version..."
        echo "Enter your text (Ctrl+D when done):"
        text=$(cat)
        if [ -n "$text" ]; then
            echo "$text" | python3 "$(dirname "$0")/kraken_cli.py"
        else
            echo "No text provided!"
        fi
        ;;
    3)
        echo "Goodbye! 🌊"
        exit 0
        ;;
    *)
        echo "Invalid choice!"
        exit 1
        ;;
esac
