from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.helper import helper
from testing.api import router as testing_router

from core.settings import app_settings
from core.gcp import gcp
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

    # Build Policy List
    helper.build_policy_list()

    # Build fake running vm list
    app_settings.build_running_vm_list()

    # #Build Zone List
    # gcp.get_zones()

    # # Setup Firebase
    # helper.init_firebase()

    # Run Web App
    uvicorn.run(app, host="0.0.0.0", port=8081)