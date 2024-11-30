# main.py
import uvicorn
from fastapi import FastAPI
from app.routes import app

mainApp = FastAPI()
mainApp.mount("/api", app)  # your app routes will now be /api/{your-route-here}

if __name__ == "__main__":
    uvicorn.run(mainApp, host="0.0.0.0", log_level="info")