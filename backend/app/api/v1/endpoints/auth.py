from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Optional
import requests
from datetime import timedelta
from app.core.config import settings
from app.db.database import get_db
from app.models.oauth_account import OAuthAccount
from app.models.user import User
from app.schemas.token import Token
from app.core.security import create_access_token

router = APIRouter()

# GitHub OAuth
@router.get("/github/login")
def github_login(
    db: Session = Depends(get_db),
    redirect_uri: Optional[str] = Query(settings.GITHUB_REDIRECT_URI)
):
    state = "secure_random_state"
    auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=user:email"
        f"&state={state}"
    )
    return RedirectResponse(url=auth_url)

@router.get("/github/callback")
def github_callback(
    db: Session = Depends(get_db),
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    redirect_uri: Optional[str] = Query(settings.GITHUB_REDIRECT_URI)
):
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state parameter")

    if state != "secure_random_state":
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    token_response = requests.post(
        "https://github.com/login/oauth/access_token",
        headers={"Accept": "application/json"},
        data={
            "client_id": settings.GITHUB_CLIENT_ID,
            "client_secret": settings.GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect_uri
        }
    ).json()

    access_token = token_response.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Failed to retrieve GitHub access token")

    user_data = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"token {access_token}"}
    ).json()

    # Get raw integer user_id directly from scalar query
    # Fix: Use .first() to get actual user object instead of raw column
    user = db.query(User).filter(User.email == user_data.get("email")).first()
    user_id = user.id if user else None
        oauth_account = db.query(OAuthAccount).filter(
            OAuthAccount.provider == "github",
            OAuthAccount.provider_id == str(user_data["id"])
        ).first()

        if oauth_account:
            return {"message": "GitHub account already linked", "user_id": oauth_account.user_id}

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(user_id, expires_delta=access_token_expires)  # Use user_id (int)
        return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}
    # Create new user
    user = User(
        username=user_data["login"],
        email=user_data.get("email") or f"{user_data['login']}@github.com",
        full_name=user_data.get("name"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    # Link OAuth account
    oauth_account = OAuthAccount(
        provider="github",
        provider_id=str(user_data["id"]),
        user_id=user_id
    )
    db.add(oauth_account)
    db.commit()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user_id, expires_delta=access_token_expires)  # Use integer user_id
    return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}

    if not user_id:  # Fixed extra 'else' syntax error and added proper condition
            # Create new user
    user = User(
        username=user_data["login"],
        email=user_data.get("email") or f"{user_data['login']}@github.com",
        full_name=user_data.get("name"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id  # Now 'user' is properly scoped and defined
    user = User(
        username=user_data["login"],
        email=user_data.get("email") or f"{user_data['login']}@github.com",
        full_name=user_data.get("name"),
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id

    # Link OAuth account
    oauth_account = OAuthAccount(
        provider="github",
        provider_id=str(user_data["id"]),
        user_id=user_id
    )
    db.add(oauth_account)
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(int(user_id), expires_delta=access_token_expires)  # Explicit integer conversion to resolve Column type error
    return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}

# WeChat OAuth
@router.get("/wechat/login")
def wechat_login(
    db: Session = Depends(get_db),
    redirect_uri: Optional[str] = Query(settings.WECHAT_REDIRECT_URI)
):
    state = "secure_random_state"
    auth_url = (
        f"https://open.weixin.qq.com/connect/qrconnect"
        f"?appid={settings.WECHAT_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=snsapi_login"
        f"&state={state}#wechat_redirect"
    )
    return RedirectResponse(url=auth_url)

@router.get("/wechat/callback")
def wechat_callback(
    db: Session = Depends(get_db),
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    redirect_uri: Optional[str] = Query(settings.WECHAT_REDIRECT_URI)
):
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state parameter")

    if state != "secure_random_state":
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    token_response = requests.get(
        "https://api.weixin.qq.com/sns/oauth2/access_token",
        params={
            "appid": settings.WECHAT_CLIENT_ID,
            "secret": settings.WECHAT_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
    ).json()

    access_token = token_response.get("access_token")
    openid = token_response.get("openid")
    if not access_token or not openid:
        raise HTTPException(status_code=401, detail="Failed to retrieve WeChat access token")

    # Get raw integer user_id directly from scalar query
    # Fix: Use .first() to get actual user object instead of raw column
    user = db.query(User).filter(User.email == user_data.get("email")).first()
    user_id = user.id if user else None
    # Get user info from WeChat
    user_data = requests.get(
        "https://api.weixin.qq.com/sns/userinfo",
        params={"access_token": access_token, "openid": openid}
    ).json()

    # Get user object to retrieve actual integer ID (fixes Column type issue)
    # Fix: Ensure user_data is defined and user_id is integer
    user = db.query(User).filter(User.email == user_data.get("email")).first()
    user_id = user.id if user else None

    if user_id:
        oauth_account = db.query(OAuthAccount).filter(
            OAuthAccount.provider == "wechat",
            OAuthAccount.provider_id == openid
        ).first()

        if oauth_account:
            return {"message": "WeChat account already linked", "user_id": oauth_account.user_id}

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        user_id = user.id  # Ensure user is fully committed and refreshed
        token = create_access_token(user_id, expires_delta=access_token_expires)  # Use integer user_id
        return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}
    # Create new user
    username = user_data.get("nickname", f"wechat_{openid[:10]}")
    user = User(
        username=username,
        email=user_data.get("email") or f"{username}@wechat.com",
        full_name=username,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    # Link OAuth account
    oauth_account = OAuthAccount(
        provider="wechat",
        provider_id=openid,
        user_id=user_id
    )
    db.add(oauth_account)
    db.commit()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user_id, expires_delta=access_token_expires)  # Use integer user_id
    return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}

    # Create new user
    username = user_data.get("nickname", f"wechat_{openid[:10]}")
    user = User(
        username=username,
        email=user_data.get("email") or f"{username}@wechat.com",
        full_name=username,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Link OAuth account
    oauth_account = OAuthAccount(
        provider="wechat",
        provider_id=openid,
        user_id=user.id
    )
    db.add(oauth_account)
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    user_id = user.id
    token = create_access_token(user_id, expires_delta=access_token_expires)  # Use integer user_id
    token = create_access_token(user_id, expires_delta=access_token_expires)
    return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}

# QQ OAuth
@router.get("/qq/login")
def qq_login(
    db: Session = Depends(get_db),
    redirect_uri: Optional[str] = Query(settings.QQ_REDIRECT_URI)
):
    state = "secure_random_state"
    auth_url = (
        f"https://graph.qq.com/oauth2.0/authorize"
        f"?client_id={settings.QQ_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=get_user_info"
        f"&state={state}"
    )
    return RedirectResponse(url=auth_url)

@router.get("/qq/callback")
def qq_callback(
    db: Session = Depends(get_db),
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    redirect_uri: Optional[str] = Query(settings.QQ_REDIRECT_URI)
):
    if not code or not state:
        raise HTTPException(status_code=400, detail="Missing code or state parameter")

    if state != "secure_random_state":
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    token_response = requests.get(
        "https://graph.qq.com/oauth2.0/token",
        params={
            "client_id": settings.QQ_CLIENT_ID,
            "client_secret": settings.QQ_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
    ).text

    token_params = {}
    for param in token_response.split("&"):
        key_value = param.split("=")
        if len(key_value) == 2:
            token_params[key_value[0]] = key_value[1]

    access_token = token_params.get("access_token")
    openid = token_params.get("openid")
    expires_in = token_params.get("expires_in")
    if not access_token or not openid:
        raise HTTPException(status_code=401, detail="Failed to retrieve QQ access token")

    user_info_response = requests.get(
        f"https://graph.qq.com/user/get_user_info",
        params={
            "access_token": access_token,
            "oauth_consumer_key": settings.QQ_CLIENT_ID,
            "openid": openid,
        }
    ).json()

    if user_info_response.get("ret", -1) != -1:
        raise HTTPException(status_code=401, detail=f"QQ user info error: {user_info_response.get('msg', 'Unknown error')}")

    # Get raw integer user_id directly from scalar query
    # Fix: Use .first() to get actual user object instead of raw column
    user = db.query(User).filter(User.email == user_info_response.get("email")).first()
    user_id = user.id if user else 0

    if user_id:
        oauth_account = db.query(OAuthAccount).filter(
            OAuthAccount.provider == "qq",
            OAuthAccount.provider_id == openid
        ).first()

        if oauth_account:
            return {"message": "QQ account already linked", "user_id": oauth_account.user_id}

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token(user_id, expires_delta=access_token_expires)  # Use user_id (int)
        token = create_access_token(user_id, expires_delta=access_token_expires)  # Use user_id (int)
        return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}
    else:
        # Create new user
        username = user_info_response.get("nickname", f"qq_{openid[:10]}")
        email = user_info_response.get("email") or f"{username}@qq.com"
        user = User(
            username=username,
            email=email,
            full_name=username, is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id
    # Link OAuth account
    oauth_account = OAuthAccount(
        provider="qq",
        provider_id=openid,
        user_id=user_id
    )
    db.add(oauth_account)
    db.commit()
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user_id, expires_delta=access_token_expires)  # Use integer user_id
    return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}

    # Create new user
    username = user_info_response.get("nickname", f"qq_{openid[:10]}")
    email = user_info_response.get("email") or f"{username}@qq.com"
    user = User(
        username=username,
        email=email,
        full_name=username,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Link OAuth account
    oauth_account = OAuthAccount(
        provider="qq",
        provider_id=openid,
        user_id=user_id
    )
    db.add(oauth_account)
    db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user_id, expires_delta=access_token_expires)  # Use integer user_id
    return {"token": Token(access_token=token, expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)}