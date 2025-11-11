import os

import jwt
from fastapi import Depends, HTTPException, status  # noqa: F401
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWKClient

URL = os.getenv("BACKEND_URL", "backend.joinastra.app")
PORT = int(os.getenv("PORT", "443"))

FF_NEW_AI = os.getenv("FF_NEW_AI", "true").lower() == "true"
FF_REMI_AI = os.getenv("FF_REMI_AI", "false").lower() == "true"

# Auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE", "astra.auth.backend")
CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", f"https://{URL}/callback")

if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET]):
    raise ValueError("Auth0 environment variables are missing")

jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
jwks_client = PyJWKClient(jwks_url)


def is_token_valid(token: str):
    """Verify JWT token validity against Auth0."""
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        # ✅ 5. Decode and verify the signature
        payload = jwt.decode(
            token,
            signing_key,
            algorithms=["RS256"],
            audience=AUTH0_API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )

        is_valid = payload.get("azp") == AUTH0_CLIENT_ID
        auth0_id = payload.get("sub")
        return is_valid, auth0_id

    except jwt.ExpiredSignatureError:
        print("❌ Token expired")
    except jwt.InvalidTokenError as e:
        print(f"❌ Invalid token: {e}")
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")

    return False, ""


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Extract and verify the user from the Authorization header."""
    token = credentials.credentials
    valid, auth0_id = is_token_valid(token)
    if not valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"auth0_id": auth0_id}
