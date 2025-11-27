import requests
from fastapi import Header, HTTPException
from typing import Optional

from models import AuthedUser

GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def get_current_user(
    authorization: str = Header(None, alias="Authorization")
) -> AuthedUser:
    """
    Extract Google OAuth token from Authorization header and
    fetch user profile from Google's OIDC userinfo endpoint.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ", 1)[1]

    # Ask Google who this token belongs to
    resp = requests.get(
        GOOGLE_USERINFO_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=5,
    )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Google token")

    data = resp.json()
    # data should contain: sub, email, name, etc.
    return AuthedUser(
        google_sub=data["sub"],
        email=data["email"],
        name=data.get("name"),
    )
