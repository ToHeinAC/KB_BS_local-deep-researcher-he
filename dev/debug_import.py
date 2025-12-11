import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    print("Attempting to import src.rag_helpers...")
    import src.rag_helpers
    print(f"Imported src.rag_helpers from {src.rag_helpers.__file__}")
    
    print("Checking for get_license_content...")
    if hasattr(src.rag_helpers, 'get_license_content'):
        print("get_license_content exists!")
    else:
        print("get_license_content DOES NOT exist!")
        print("Available attributes:", dir(src.rag_helpers))
        
    from src.rag_helpers import get_license_content
    print("Successfully imported get_license_content directly")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
