from fastapi import FastAPI
from app.api.routes.auth import router as auth_router
from app.api.routes.announcements import router as announcements_router
from app.api.routes.events import router as events_router
from app.api.routes.timetable import router as timetable_router
from app.api.routes.notifications import router as notifications_router

app = FastAPI(
    title="BaseCampus Dz API",
    version="1.0.0"
)
app.include_router(auth_router)
app.include_router(announcements_router)
app.include_router(events_router)
app.include_router(timetable_router)
app.include_router(notifications_router)

@app.get("/")
def root():
    return {"message": "BaseCampus Dz API is running!"}