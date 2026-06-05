import asyncio

class HITLEngine:
    def __init__(self, broadcast_callback):
        self.broadcast = broadcast_callback
        
    async def require_confirmation(self, action_details):
        """Halts execution and waits for human confirmation."""
        print(f"HITL Warning: {action_details}")
        
        await self.broadcast("hitl", {"message": f"Confirm action: {action_details['description']}"})
        
        # Simulate waiting for confirmation (e.g., from UI websocket or audio)
        # In a real system, this would await a specific event triggered by spacebar or voice
        await asyncio.sleep(5) 
        
        print("HITL Confirmed via timeout simulation.")
        await self.broadcast("idle", {})
        return True
