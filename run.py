import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from src.main import main
except ImportError as e:
    print(f"Error importing app: {e}")
    # Fallback/Debug info
    print(f"Current Path: {sys.path}")
    input("Press Enter to exit...")
    sys.exit(1)

if __name__ == "__main__":
    main()
