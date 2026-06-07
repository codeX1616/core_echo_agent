import os
import json
import uuid

class AgentBuilder:
    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = plugins_dir
        os.makedirs(self.plugins_dir, exist_ok=True)
        
    def build_agent_from_query(self, query):
        """
        Dynamically generates a new agent plugin based on the user's query.
        In a real implementation, this would use an LLM to generate the code and manifest.
        """
        agent_id = str(uuid.uuid4())[:6]
        # create a safe agent name
        safe_query = "".join(c if c.isalnum() else "_" for c in query.lower())[:15]
        agent_name = f"agent_{safe_query}_{agent_id}"
        agent_dir = os.path.join(self.plugins_dir, agent_name)
        os.makedirs(agent_dir, exist_ok=True)
        
        # Create agent_manifest.json
        manifest = {
            "name": agent_name,
            "description": f"Dynamically generated agent for handling: {query}",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_data": {
                        "type": "string",
                        "description": "Information extracted from user query to be processed."
                    }
                },
                "required": ["input_data"]
            },
            "destructive": False
        }
        
        with open(os.path.join(agent_dir, "agent_manifest.json"), "w") as f:
            json.dump(manifest, f, indent=4)
            
        # Create plugin.py
        plugin_code = f'''import sys
import json

def main():
    if len(sys.argv) < 2:
        print(json.dumps({{"error": "No parameters provided"}}))
        sys.exit(1)
        
    try:
        params = json.loads(sys.argv[1])
        input_data = params.get("input_data", "No input data")
        
        # Generated agent logic
        result = f"Hello! I am a dynamically created agent to help with: '{query}'. I received: {{input_data}}"
        
        print(json.dumps({{"success": result}}))
        sys.exit(0)
    except Exception as e:
        print(json.dumps({{"error": str(e)}}))
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        with open(os.path.join(agent_dir, "plugin.py"), "w") as f:
            f.write(plugin_code)
            
        return agent_name, manifest
