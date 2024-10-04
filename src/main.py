from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.docs.docs import tags_metadata
from src.router import image, user

app = FastAPI(openapi_tags=tags_metadata)

origins = ["http://localhost", "http://localhost:8000", "http://localhost:3000", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image.router)
app.include_router(user.router)


# Just for testing the public IP
@app.get("/", tags=["Testing"])
def read_root():
    return {"Hello": "World"}
