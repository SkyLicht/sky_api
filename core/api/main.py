from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from core.api.endpoints import user_endpoint, hbh_endpoint, work_plan_endpoint, line_endpoint, layout_endpoint, \
    cycle_time_endpoint, platform_endpoint
from core.data.models.token_model import TokenModel
from core.security import auth
from core.security.auth import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

app = FastAPI()
# Allow CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","http://10.13.33.46:3000"],  # Adjust origins as needed
    # allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
# Include endpoints
app.include_router(user_endpoint.router)
app.include_router(hbh_endpoint.router)

app.include_router(work_plan_endpoint.router)

app.include_router(line_endpoint.router)
app.include_router(layout_endpoint.router)
app.include_router(platform_endpoint.router)
app.include_router(cycle_time_endpoint.router)
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
