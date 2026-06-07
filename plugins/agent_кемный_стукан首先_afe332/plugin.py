import sys
import json

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No parameters provided"}))
        sys.exit(1)
        
    try:
        params = json.loads(sys.argv[1])
        input_data = params.get("input_data", "No input data")
        
        # Generated agent logic
        result = f"Hello! I am a dynamically created agent to help with: 'Кемный стукан首先 Qiтбитку Трженка Joeva уже Estate gym workout, А craко roller-почка'. I received: {input_data}"
        
        print(json.dumps({"success": result}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
