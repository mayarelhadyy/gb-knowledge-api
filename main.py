from fastapi import FastAPI, Request
import time
from fastapi.middleware.cors import CORSMiddleware


from routes import (
    search,
    documents,
    upload,
    chat,
    auth
)
from services.database_service import initialize_database

app = FastAPI(
    title="GB Knowledge API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

initialize_database()

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(upload.router)
app.include_router(search.router)

@app.get("/")
def home():
    return {
        "message": "GB Knowledge API is running!"
    }


@app.middleware("http")
async def log_request_time(request: Request, call_next):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    print(
        f"Request: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.4f} seconds"
    )

    return response