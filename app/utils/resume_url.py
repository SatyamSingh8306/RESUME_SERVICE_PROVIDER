from typing import Dict, Any
from app.services.broker.rpc import RPCService, RPCPayloadType


async def get_resume_url(user_id: str) -> str:
    """
    Fetch just the resume URL for a given user ID using RPC service
    
    Args:
        user_id: The user ID to fetch the resume URL for
        
    Returns:
        The URL to the user's resume PDF
    """
    try:
        response = await RPCService.request(
            "USER_RPC",
            RPCService.build_request_payload(
                type=RPCPayloadType.GET_USER_RESUME,
                data={"userId": user_id},
            ),
        )
        
        if not response or "data" not in response or "url" not in response["data"]:
            raise ValueError(f"Invalid response format or missing URL for user {user_id}")
        
        # Return just the URL
        return response["data"]
        
    except Exception as e:
        raise Exception(f"Failed to fetch resume URL: {str(e)}")

