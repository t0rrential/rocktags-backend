from fastapi import FastAPI

from classes import TrackerRequest
from getreports import fetch_reports

app = FastAPI()

@app.post("/findmy/")
async def create_item(request: TrackerRequest):
    return await fetch_reports(request)