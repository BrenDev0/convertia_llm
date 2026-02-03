import os
import logging
import hmac
import hashlib
import time
from fastapi import Request
from src.security.domain.exceptions import HMACException
logger = logging.getLogger(__name__)

EXCLUDED_PATHS = [
    "/graphql",  # GraphQL IDE/playground
]

async def verify_hmac(request: Request) -> bool:
    """
    Verify HMAC signature for incoming requests
    Use with Depends() on specific routes that need HMAC verification
    """

    ## disactivate for development
    project_enviornment = os.getenv("ENVIRONMENT")
    if project_enviornment != "PRODUCTION":
        return

    ## 
    
    secret = os.getenv("HMAC_SECRET")
    if not secret:
        raise ValueError("Missing HMAC_SECRET environment variable")
    
    ## Skip HMAC for GET requests to /graphql (GraphQL IDE)
    if request.url.path == "/graphql" and request.method == "GET":
        return True
    
    logger.debug(f"Headers: {request.headers}")
    signature = request.headers.get('x-signature')
    payload = request.headers.get('x-payload')
    
    if not signature or not payload:
        logger.debug(f"Missing signature or payload, ::: signature: {signature} ::: payload: {payload}")
        raise HMACException(detail="HMAC verification failed")
    
    # Validate timestamp
    try:
        timestamp = int(payload)
    except ValueError:
        logger.debug(f"Invalid timestamp ::: timestamp: {timestamp}")
        raise HMACException(detail="HMAC verification failed")
    
    current_time = int(time.time() * 1000)  # Current time in milliseconds
    allowed_drift = 60_000  # 60 seconds
    
    if abs(current_time - timestamp) > allowed_drift:
        logger.debug(f"Expired ::: timestamp: {timestamp}, ::: current_time: {current_time}")
        raise HMACException(detail="HMAC verification failed")
    
    # Generate expected signature
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures using constant-time comparison
    if not hmac.compare_digest(signature, expected):
        logger.debug(f"Comparison failed ::: expected: {expected} ::: received: {signature}")
        raise HMACException(detail="HMAC verification failed")
    
    return True