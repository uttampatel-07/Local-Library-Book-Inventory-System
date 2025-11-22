#!/usr/bin/env python
"""
Local Library Book Inventory System - Server Runner
Double-click this file or run: python run.py
"""

import os
import sys
import subprocess

def main():
    print("=" * 50)
    print(" Local Library Book Inventory System")
    print("=" * 50)
    print()
    print("Starting Flask server...")
    print()
    print("The server will be available at:")
    print("http://localhost:5000")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 50)
    print()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Check if app.py exists
    if not os.path.exists('app.py'):
        print("ERROR: app.py not found!")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Run the Flask app
    try:
        import app
        app.app.run(debug=True)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
    except Exception as e:
        print(f"\nERROR: {e}")
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()

