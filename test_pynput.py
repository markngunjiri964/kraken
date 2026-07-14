#!/usr/bin/env python3
"""Simple test to verify pynput typing works"""

from pynput.keyboard import Controller
import time

print("KRAKEN PYNPUT TEST")
print("=" * 50)
print("This will type 'Hello from Kraken!' in 5 seconds.")
print("Quickly click on a text field!")
print("=" * 50)

keyboard = Controller()

for i in range(5, 0, -1):
    print(f"Typing in {i}...")
    time.sleep(1)

print("TYPING NOW!")

try:
    keyboard.type("Hello from Kraken!")
    print("✓ Typing completed successfully!")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
