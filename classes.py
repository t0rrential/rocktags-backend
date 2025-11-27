from pydantic import BaseModel

class tracker():
    name: str
    privateKey: str

class trackerRequest(BaseModel):
    trackers: list[tracker]

