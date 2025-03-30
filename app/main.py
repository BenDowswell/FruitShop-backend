from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import users, fruits, carts, auth

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
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Fruit Shop API"}
