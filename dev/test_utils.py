import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.utils import get_configured_llm_model, parse_output
    from src.configuration import get_config_instance
    
    print("Testing Utils...")
    
    # Test Config
    config = get_config_instance()
    print(f"Config loaded. Report LLM: {config.report_llm}")
    
    # Test Parse Output
    json_text = '{"response": "test response", "reasoning": "test thinking"}'
    parsed = parse_output(json_text)
    assert parsed["response"] == "test response"
    print("parse_output JSON test passed")
    
    xml_think = '<think>thinking...</think> response text'
    parsed = parse_output(xml_think)
    assert parsed["reasoning"] == "thinking..."
    assert parsed["response"] == "response text"
    print("parse_output XML test passed")

    print("ALL UTILS TESTS PASSED")
except Exception as e:
    print(f"TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
