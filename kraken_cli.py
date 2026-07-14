#!/usr/bin/env python3
"""
KRAKEN CLI - The Devourer of Paste Restrictions
Command-line version for maximum compatibility
"""

import sys
import time
import random
import argparse
from pynput.keyboard import Controller, Key


class KrakenCLI:
    def __init__(self):
        self.keyboard = Controller()
    
    def type_text(self, text, speed=50, countdown=3, human_like=True, typos=False):
        """
        Type text with specified parameters
        
        Args:
            text: Text to type
            speed: Typing speed (1-100)
            countdown: Seconds to wait before typing
            human_like: Add random variations
            typos: Add occasional typos
        """
        # Countdown
        if countdown > 0:
            print(f"\n🐙 KRAKEN awakening...")
            for i in range(countdown, 0, -1):
                print(f"   Starting in {i}...", end='\r')
                time.sleep(1)
            print("   " + " " * 30)  # Clear line
        
        print("🌊 KRAKEN UNLEASHED! Typing in progress...")
        
        # Calculate base delay
        base_delay = 0.2 - (speed / 100) * 0.19
        
        total_chars = len(text)
        for idx, char in enumerate(text):
            # Add typo occasionally
            if typos and char.isalpha() and random.random() < 0.02:
                wrong_char = random.choice('qwertyuiopasdfghjklzxcvbnm')
                self.keyboard.type(wrong_char)
                time.sleep(base_delay * 0.5)
                self.keyboard.press(Key.backspace)
                self.keyboard.release(Key.backspace)
                time.sleep(base_delay * 0.3)
            
            # Type the character
            try:
                self.keyboard.type(char)
            except:
                pass
            
            # Progress indicator
            if (idx + 1) % 50 == 0 or idx == total_chars - 1:
                percent = ((idx + 1) / total_chars) * 100
                print(f"   Progress: {percent:.1f}% ({idx + 1}/{total_chars})", end='\r')
            
            # Delay
            delay = base_delay
            if human_like:
                delay += random.uniform(-0.02, 0.03)
            time.sleep(max(0.01, delay))
        
        print("\n✅ KRAKEN devoured all restrictions! Complete.")


def main():
    parser = argparse.ArgumentParser(
        description="🐙 KRAKEN - The Devourer of Paste Restrictions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Type from stdin with 3 second countdown
  echo "Hello World" | kraken.py
  
  # Type from file with fast speed
  cat mytext.txt | kraken.py --speed 80
  
  # Ultra-realistic with typos
  kraken.py --text "Important text" --typos --human-like
  
  # No countdown, beast mode
  kraken.py --text "Fast!" --countdown 0 --speed 100
        """
    )
    
    parser.add_argument(
        '-t', '--text',
        help='Text to type (if not provided, reads from stdin)'
    )
    parser.add_argument(
        '-s', '--speed',
        type=int,
        default=50,
        choices=range(1, 101),
        metavar='[1-100]',
        help='Typing speed: 1=slowest, 100=fastest (default: 50)'
    )
    parser.add_argument(
        '-c', '--countdown',
        type=int,
        default=3,
        choices=range(0, 16),
        metavar='[0-15]',
        help='Countdown before typing starts in seconds (default: 3)'
    )
    parser.add_argument(
        '--human-like',
        action='store_true',
        default=True,
        help='Add random micro-delays for human-like typing (default: enabled)'
    )
    parser.add_argument(
        '--no-human-like',
        action='store_false',
        dest='human_like',
        help='Disable human-like variations'
    )
    parser.add_argument(
        '--typos',
        action='store_true',
        help='Add occasional typos with corrections for ultra-realism'
    )
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress output messages'
    )
    
    args = parser.parse_args()
    
    # Get text
    if args.text:
        text = args.text
    else:
        if not sys.stdin.isatty():
            text = sys.stdin.read()
        else:
            print("Error: No text provided. Use --text or pipe text via stdin")
            print("Example: echo 'Hello' | python3 kraken.py")
            sys.exit(1)
    
    if not text.strip():
        print("Error: Empty text provided")
        sys.exit(1)
    
    # Show info
    if not args.quiet:
        print("=" * 60)
        print("🐙 KRAKEN - The Devourer of Paste Restrictions")
        print("=" * 60)
        print(f"Text length: {len(text)} characters")
        print(f"Speed: {args.speed}/100", end='')
        if args.speed < 20:
            print(" (Slow)")
        elif args.speed < 40:
            print(" (Relaxed)")
        elif args.speed < 60:
            print(" (Medium)")
        elif args.speed < 80:
            print(" (Fast)")
        else:
            print(" (BEAST MODE)")
        print(f"Countdown: {args.countdown} seconds")
        print(f"Human-like: {'Yes' if args.human_like else 'No'}")
        print(f"Typos: {'Yes' if args.typos else 'No'}")
        print("\n⚠️  Quickly click on the target field after countdown!")
        print("=" * 60)
    
    # Type it
    kraken = KrakenCLI()
    try:
        kraken.type_text(
            text,
            speed=args.speed,
            countdown=args.countdown,
            human_like=args.human_like,
            typos=args.typos
        )
    except KeyboardInterrupt:
        print("\n\n🛑 KRAKEN stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
