import uvicorn
from fastapi import FastAPI
from app.routes import app

from fastapi.middleware.cors import CORSMiddleware


mainApp = FastAPI()

origins = [
    "http://localhost:5000",
]

mainApp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount your app under the "/" path
mainApp.mount("/", app)

if __name__ == "__main__":
    # Pass the application as a string 'main:mainApp' for reload support
    uvicorn.run("main:mainApp", host="0.0.0.0", port=8000, log_level="info", reload=True)
