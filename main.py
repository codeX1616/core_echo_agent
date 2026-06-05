import asyncio
import os
import uvicorn
from core.audio.pipeline import AudioPipeline
from core.memory.db import ContextDB
from core.memory.slm import SLMEngine
from core.memory.router import IntentRouter
from dashboard.app import app, broadcast_state
from execution.sandbox import SandboxRunner
from execution.hitl import HITLEngine

class CoreEcho:
    def __init__(self):
        self.audio = AudioPipeline()
        self.db = ContextDB()
        self.slm = SLMEngine()
        self.router = IntentRouter()
        self.sandbox = SandboxRunner()
        self.hitl = HITLEngine(broadcast_callback=broadcast_state)
        
    async def handle_audio_text(self, text):
        print(f"Heard: {text}")
        await broadcast_state("listening", {})
        
        # 1. Store in DB
        self.db.add_memory("user", text)
        context = self.db.get_markdown_context()
        
        # 2. Parse Intent
        parsed_intent = self.slm.parse_intent(text, context, self.router.schemas)
        
        if not parsed_intent:
            await broadcast_state("idle", {})
            return
            
        # 3. Route Intent
        schema = self.router.route(parsed_intent)
        if not schema:
            print("No matching schema found.")
            await broadcast_state("idle", {})
            return
            
        # 4. Check HITL
        if schema.get("destructive", False):
            confirmed = await self.hitl.require_confirmation({
                "description": schema["description"],
                "parameters": parsed_intent.get("parameters")
            })
            if not confirmed:
                print("HITL aborted.")
                await broadcast_state("idle", {})
                return
                
        # 5. Execute
        await broadcast_state("datacard", {
            "title": f"Executing: {schema['name']}",
            "data": parsed_intent.get("parameters")
        })
        
        # Find plugin.py path (simplified)
        plugin_path = os.path.join("plugins", "base_plugin", "plugin.py") # Mock routing logic for base_plugin
        
        result = self.sandbox.execute_plugin(plugin_path, parsed_intent.get("parameters"))
        
        self.db.add_memory("system", str(result))
        await asyncio.sleep(2) # Keep datashow up briefly
        await broadcast_state("idle", {})

    async def run(self):
        # Start Dashboard Server
        server_config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_level="info")
        server = uvicorn.Server(server_config)
        
        # Run everything concurrently
        await asyncio.gather(
            server.serve(),
            self.audio.run(self.handle_audio_text)
        )

if __name__ == "__main__":
    echo = CoreEcho()
    try:
        asyncio.run(echo.run())
    except KeyboardInterrupt:
        print("Shutting down...")
