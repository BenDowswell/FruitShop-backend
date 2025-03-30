from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import crud, models, schemas
from .database import SessionLocal, engine
from .routes import users, fruits, carts
from .crud import authenticate_user
from .schemas import Token, Login
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.openapi.models import SecurityScheme as SecuritySchemeModel
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(fruits.router)
app.include_router(carts.router)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = "your_secret_key"  # Replace with a secure key from .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/logout")
def logout():
    return {"message": "Logout successful"}


@app.get("/users", response_model=list[schemas.User])
def list_users(db: Session = Depends(get_db)):
    """
    API endpoint to list all users.
    """
    return crud.list_all_users(db)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Fruit Shop API"}


# Add OAuth2 security scheme to OpenAPI documentation
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Fruit Shop API",
        version="1.0.0",
        description="API for managing the Fruit Shop",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "token",
                    "scopes": {},
                }
            },
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
