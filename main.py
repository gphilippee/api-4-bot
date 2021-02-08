from typing import Optional
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import json
import os
import wikipedia

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

@app.post("/mars", status_code=200)
async def mars_weather(request: Request):
    r = requests.get("https://api.nasa.gov/insight_weather/?api_key=" + os.environ["API_KEY"] + "&feedtype=json&ver=1.0")
    r_json = r.json()

    last_sols = r_json['sol_keys'][-1]

    season = r_json[last_sols]['Season']
    if(season == "Winter"):
        season = "hiver"
    elif(season == "Autumn"):
        season = "automne"
    elif(season == "Summer"):
        season = "été"
    elif(season == "Spring"):
        season = "printemps"

    if('PRE' in r_json[last_sols]):
        pression = r_json[last_sols]['PRE']['av']
    else:
        pression = "inconnue"


    if('AT' in r_json[last_sols]):
         temp = r_json[last_sols]['AT']['av']
    else:
        temp = "inconnue"

    return {
        "season": season,
        "pression": pression,
        "temp": temp
    }

class Planet(BaseModel):
    name: str

@app.post("/wiki", status_code=200)
async def wiki(planet: Planet):
    wikipedia.set_lang("fr")
    summary = wikipedia.summary(planet)
    
    return { 
        "text": summary
    }