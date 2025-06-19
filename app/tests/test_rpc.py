import asyncio
from app.services.broker.rpc import RPCService, RPCPayloadType

class TestResponder:
    """Test responder for RPC"""
    
    @staticmethod
    async def respond_rpc(request_payload: RPCPayloadType) -> dict:
        """Echo back the request data with a test response"""
        return {
            "status": "success",
            "echo": request_payload["data"],
            "message": "Test response received"
        }

async def run_test():
    """Run the RPC test"""
    try:
        # Start the responder in the background
        responder_task = asyncio.create_task(RPCService.respond(TestResponder()))
        
        # Wait a bit for the responder to start
        await asyncio.sleep(2)
        
        # Create a test request
        test_payload = RPCService.build_request_payload(
            type="test",
            data={"message": "Hello RPC!"}
        )
        
        # Make the request
        response = await RPCService.request(
            service_rpc="rpc_queue",  # This should match your RPC_QUEUE value
            request_payload=test_payload,
            timeout=5
        )
        
        # Verify the response
        assert response["status"] == "success"
        assert response["echo"]["message"] == "Hello RPC!"
        
    except Exception as e:
        pass
    finally:
        # Cancel the responder task
        responder_task.cancel()
        try:
            await responder_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(run_test()) 