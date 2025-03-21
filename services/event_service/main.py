from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGO_URI = "mongodb://localhost:27019/"
client = MongoClient(MONGO_URI)
db = client.event_service
events_collection = db.events

# Pydantic Model for Event
class Event(BaseModel):
    event_id: str
    name: str
    description: str
    date: str
    location: str
    available_tickets: int

# API to Create an Event
@app.post("/events/")
def create_event(event: Event):
    if events_collection.find_one({"event_id": event.event_id}):
        raise HTTPException(status_code=400, detail="Event ID already exists")
    events_collection.insert_one(event.dict())
    return {"message": "Event created successfully"}

# API to Get All Events
@app.get("/events/", response_model=List[Event])
def get_events():
    events = list(events_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return events

# API to Get Event Availability
@app.get("/events/{event_id}/availability")
def get_event_availability(event_id: str):
    event = events_collection.find_one({"event_id": event_id}, {"_id": 0})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"available_tickets": event["available_tickets"]}

# API to Update Event Tickets
@app.put("/events/{event_id}/update-tickets/")
def update_event_tickets(event_id: str, tickets_booked: int):
    event = events_collection.find_one({"event_id": event_id})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    updated_tickets = event["available_tickets"] - tickets_booked
    if updated_tickets < 0:
        raise HTTPException(status_code=400, detail="Not enough tickets available")
    events_collection.update_one({"event_id": event_id}, {"$set": {"available_tickets": updated_tickets}})
    return {"message": "Event tickets updated successfully"}
