from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.helper import helper
from v1.api import router as api_router
from testing.api import router as testing_router

from core.settings import app_settings
import uvicorn

#Start App
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routes
app.include_router(api_router)
app.include_router(testing_router)

@app.get("/")
async def root():
    return {  
        "app_name": app_settings.app_name,
        "project": app_settings.gcp_project
    }


if __name__ == "__main__":
    # Enable Logging
    helper.Configure_Logging()

    # Build VM List
    helper.build_vm_info()

    # Run Web App
    uvicorn.run(app, host="0.0.0.0", port=8080)