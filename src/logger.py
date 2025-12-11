import os
import datetime
import json
from typing import Any

DEBUG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dev', 'debugging_info.txt')

def log_debug(step: str, data: Any):
    """
    Log debug information to the dev/debugging_info.txt file.
    
    Args:
        step: The name of the step or component logging the info.
        data: The data to log (string, dict, or object).
    """
    try:
        # Create dev directory if it doesn't exist (though it should)
        os.makedirs(os.path.dirname(DEBUG_FILE_PATH), exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(DEBUG_FILE_PATH, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{step}]\n")
            
            if isinstance(data, (dict, list)):
                try:
                    f.write(json.dumps(data, indent=2, default=str))
                except:
                    f.write(str(data))
            else:
                f.write(str(data))
                
            f.write("\n" + "-"*50 + "\n")
            
    except Exception as e:
        print(f"Failed to log debug info: {e}")
