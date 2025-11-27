from fastapi import FastAPI

from classes import TrackerRequest
from getreports import fetch_reports

app = FastAPI()

print("listening on port 6970 (hopefully)")

@app.post("/findmy/")
async def create_item(request: TrackerRequest):
    return await fetch_reports(request)