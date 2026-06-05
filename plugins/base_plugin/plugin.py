import sys
import json
import os

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No parameters provided"}))
        sys.exit(1)
        
    try:
        params = json.loads(sys.argv[1])
        file_path = params.get("file_path")
        
        if not file_path or not os.path.exists(file_path):
            print(json.dumps({"error": f"File not found: {file_path}"}))
            sys.exit(1)
            
        # Mock opening file
        print(json.dumps({"success": f"Opened file {file_path}"}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
