from llama_cpp import Llama
import json

class SLMEngine:
    def __init__(self, model_path="phi-3-mini.gguf"):
        # Placeholder initialization for local SLM
        # self.llm = Llama(model_path=model_path, n_gpu_layers=-1, n_ctx=2048)
        pass
        
    def parse_intent(self, prompt, context_md, schemas):
        """
        Takes the user prompt, context, and available plugin schemas.
        Returns a structured JSON matching one of the schemas.
        """
        prompt_lower = prompt.lower()
        
        # Simple mock matching logic to find an existing agent
        for schema_name, schema_data in schemas.items():
            schema_name_normalized = schema_name.lower().replace("_", " ")
            if schema_name_normalized in prompt_lower:
                return {
                    "intent": schema_name,
                    "parameters": {
                        "input_data": prompt,
                        "file_path": "/tmp/mock_file"
                    }
                }
            
            # Match if the exact prompt is in the description (handles dynamic agents)
            if prompt_lower in schema_data.get("description", "").lower():
                return {
                    "intent": schema_name,
                    "parameters": {
                        "input_data": prompt,
                        "file_path": "/tmp/mock_file"
                    }
                }
                
            # Match keywords from description
            desc_words = schema_data.get("description", "").lower().split()
            match_count = sum(1 for word in desc_words if len(word) > 4 and word in prompt_lower)
            if match_count >= 2:
                return {
                    "intent": schema_name,
                    "parameters": {
                        "input_data": prompt,
                        "file_path": "/tmp/mock_file"
                    }
                }

        # If no match is found, signal to the orchestrator to create a new agent
        return {
            "intent": "create_agent",
            "parameters": {
                "query": prompt
            }
        }
