import asyncio
import logging
from app.services.broker.rpc import RPCService, RPCPayloadType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestResponder:
    """Test responder for RPC"""
    
    @staticmethod
    async def respond_rpc(request_payload: RPCPayloadType) -> dict:
        """Echo back the request data with a test response"""
        logger.info(f"Received request: {request_payload}")
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
        logger.info("Sending test request...")
        response = await RPCService.request(
            service_rpc="rpc_queue",  # This should match your RPC_QUEUE value
            request_payload=test_payload,
            timeout=5
        )
        
        # Log the response
        logger.info(f"Received response: {response}")
        
        # Verify the response
        assert response["status"] == "success"
        assert response["echo"]["message"] == "Hello RPC!"
        logger.info("Test completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
    finally:
        # Cancel the responder task
        responder_task.cancel()
        try:
            await responder_task
        except asyncio.CancelledError:
            pass

if __name__ == "__main__":
    asyncio.run(run_test()) 