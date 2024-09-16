from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.auth_controller import router as auth_router
from controllers.token_controller import router as token_router
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/service/auth", tags=["Authentication Management"])
app.include_router(token_router, prefix="/service/token", tags=["Token Management"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Authentication Service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.RELOAD)
