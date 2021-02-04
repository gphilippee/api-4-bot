from typing import Optional
from fastapi import FastAPI, Request
import requests

app = FastAPI()

@app.post("/", status_code=200)
async def index(request: Request):

    body = await request.json()

    return {"received_request_body": body}