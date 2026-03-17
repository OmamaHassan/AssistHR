import os
import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_KEY")


async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SUPABASE_URL}/auth/v1/user",
                headers={
                    "Authorization" : f"Bearer {token}",
                    "apikey"        : SUPABASE_KEY
                }
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token"
            )

        user = response.json()
        return {
            "id"   : user.get("id"),
            "email": user.get("email")
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Could not validate token"
        )