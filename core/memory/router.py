from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import json
import os

class IntentRouter:
    def __init__(self, plugins_dir="plugins"):
        self.client = QdrantClient(":memory:")
        self.plugins_dir = plugins_dir
        self.schemas = {}
        
        self.client.recreate_collection(
            collection_name="intents",
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        self.load_schemas()
        
    def load_schemas(self):
        if not os.path.exists(self.plugins_dir):
            return
            
        for root, _, files in os.walk(self.plugins_dir):
            if "agent_manifest.json" in files:
                with open(os.path.join(root, "agent_manifest.json"), "r") as f:
                    manifest = json.load(f)
                    manifest["plugin_dir"] = root
                    self.schemas[manifest["name"]] = manifest
                    # In a real scenario, embed the description and store in Qdrant
                    
    def route(self, parsed_json):
        intent_name = parsed_json.get("intent")
        if intent_name in self.schemas:
            return self.schemas[intent_name]
        return None
