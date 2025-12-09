from fastapi import APIRouter
from typing import List
from pathlib import Path
import json

from models import BrowsingEvent

events_router = APIRouter()
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

with open(DATA_DIR / "browsing_history_fashion.json", "r", encoding="utf-8") as f:
    EVENTS: List[BrowsingEvent] = [BrowsingEvent(**e) for e in json.load(f)]


@events_router.get("/events", response_model=List[BrowsingEvent])
async def list_events():
    return EVENTS
