import logging
import os
import hmac
import hashlib
import time
logger = logging.getLogger(__name__)

def verify_hmac_ws(signature: str, payload: str) -> bool:
    """
    Verify HMAC signature for WebSocket connections.
    """
    secret = os.getenv("HMAC_SECRET")
    if not secret:
        logger.error("HMAC variables not set")
        return False
    
    if not signature or not payload:
        logger.error(f"Missing signature or payload, ::: signature: {signature} ::: payload: {payload}")
        return False
    
    try:
        timestamp = int(payload)

    except ValueError:
        logger.error(f"Invalid timestamp ::: timestamp: {timestamp}")
        return False
    
    current_time = int(time.time() * 1000)
    allowed_drift = 60_000

    if abs(current_time - timestamp) > allowed_drift:
        logger.error(f"Expired ::: timestamp: {timestamp}, ::: current_time: {current_time}")
        return False
    
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(signature, expected):
        logger.error(f"Comparison failed ::: expected: {expected} ::: received: {signature}")
        return False
    
    return True