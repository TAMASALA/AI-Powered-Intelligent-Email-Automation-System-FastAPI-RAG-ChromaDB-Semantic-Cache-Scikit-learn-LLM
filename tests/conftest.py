import sys
from pathlib import Path

# Add the parent directory to the Python path so tests can import the app module
sys.path.insert(0, str(Path(__file__).parent.parent))
