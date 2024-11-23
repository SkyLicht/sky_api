from datetime import timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.api.endpoints import user_endpoint
from core.data.models.token_model import TokenModel
from core.security import auth
from core.security.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

app = FastAPI()

# Include endpoints
app.include_router(user_endpoint.router)
@app.get("/test/", response_model=List[dict])
def test():
    return [{"Hello": "World"}]




@app.post("/token", response_model=TokenModel)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(auth.get_db_session)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return TokenModel(access_token=access_token, token_type="bearer")
