from fastapi import FastAPI
from core.settings import Settings
from core.helper import helper
from v1.api import router as api_router

from core.gcp import gce
import core.settings as settings
import uvicorn

#Start App
settings = Settings()
app = FastAPI()

# Include Routes
app.include_router(api_router)

@app.get("/")
async def root():
    return {  
        "app_name": settings.app_name,
        "project": settings.gcp_project
    }




if __name__ == "__main__":
    # Enable Logging
    helper.Configure_Logging()

    # Build Values
    helper.GetConfig()

    # Run Web App
    uvicorn.run(app, host="0.0.0.0", port=8080)