from pydantic import BaseModel

class Tracker(BaseModel):
    name: str
    privateKey: str

class TrackerRequest(BaseModel):
    trackers: list[Tracker]

