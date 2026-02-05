import hmac
import hashlib
import time
import os
from typing import Optional

def generate_hmac_headers(secret: Optional[str] = None):
        if not secret:
            secret = os.getenv("HMAC_SECRET")

            if not secret:
                raise ValueError("HMAC variables not set")
            
        timestamp = int(time.time() * 1000)  
        payload = str(timestamp)
        
        signature = hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return {
            'x-signature': signature,
            'x-payload': payload,
            'Content-Type': 'application/json'
        }