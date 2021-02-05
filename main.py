from typing import Optional
from fastapi import FastAPI, Request
import requests
import json
import os

app = FastAPI()

@app.post("/", status_code=200)
async def index(request: Request):

    r = requests.get("https://api.nasa.gov/planetary/apod?api_key=" + os.environ["API_KEY"] + "&count=3")

    response = []
    for astro in r.json():
        response.append({
        "imageUrl": astro['url'],
        "title": astro['title'],
        "subtitle": astro['explanation']
        })
    return response

@app.post("/errors", status_code=200)
async def errors(request: Request):
    return await request.json()