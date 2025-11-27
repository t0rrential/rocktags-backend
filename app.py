from fastapi import FastAPI

from classes import trackerRequest
from getreports import fetch_reports

app = FastAPI()

@app.post("/findmy/")
async def create_item(request: trackerRequest):
    return fetch_reports(trackerRequest)