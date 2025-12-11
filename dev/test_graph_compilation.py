import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.graph import create_hitl_graph, create_main_graph
    print("Successfully imported graph creators")
    
    print("Compiling HITL Graph...")
    hitl = create_hitl_graph()
    print("HITL Graph compiled successfully")
    
    print("Compiling Main Graph...")
    main = create_main_graph()
    print("Main Graph compiled successfully")
    
    print("ALL TESTS PASSED")
except Exception as e:
    print(f"TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
