import os
import asyncio
import httpx

from datetime import date
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, model_validator

app = FastAPI(title="Exam Scheduler Service")

ROOM_BOOKING_URL = os.getenv(
    "ROOM_BOOKING_URL",
    "http://127.0.0.1:8001"
)

ROOM_BOOKING_TIMEOUT = float(
    os.getenv("ROOM_BOOKING_TIMEOUT", "2")
)

ROOM_BOOKING_MAX_RETRIES = int(
    os.getenv("ROOM_BOOKING_MAX_RETRIES", "3")
)

@app.get("/config")
def get_config():
    return {
        "room_booking_url": ROOM_BOOKING_URL,
        "timeout": ROOM_BOOKING_TIMEOUT,
        "max_retries": ROOM_BOOKING_MAX_RETRIES
    }

class Exam(BaseModel):
    exam_id: str = Field(min_length=1)
    course_code: str = Field(min_length=1)
    day: date
    start_hour: int = Field(ge=8, le=20)
    end_hour: int = Field(ge=8, le=20)
    students: int = Field(ge=1)

    @model_validator(mode="after")
    def check_time(self):
        if self.end_hour <= self.start_hour:
            raise ValueError("End hour must be after start hour")
        return self


async def call_room_booking(method, path, json_data=None):
    async with httpx.AsyncClient(
        timeout=ROOM_BOOKING_TIMEOUT
    ) as client:

        for attempt in range(ROOM_BOOKING_MAX_RETRIES + 1):
            try:
                response = await client.request(
                    method,
                    f"{ROOM_BOOKING_URL}{path}",
                    json=json_data
                )

                if response.status_code >= 500:
                    if attempt < ROOM_BOOKING_MAX_RETRIES:
                        await asyncio.sleep(0.5 * (2 ** attempt))
                        continue

                    raise HTTPException(
                        status_code=503,
                        detail="Room Booking Service is unavailable"
                    )

                return response

            except (httpx.TimeoutException, httpx.ConnectError):
                if attempt < ROOM_BOOKING_MAX_RETRIES:
                    await asyncio.sleep(0.5 * (2 ** attempt))
                    continue

                raise HTTPException(
                    status_code=503,
                    detail="Room Booking Service is unavailable"
                )


@app.post("/exams", status_code=201)
async def create_exam(exam: Exam):

    
    response = await call_room_booking("GET", "/rooms")

    rooms = response.json()

   
    suitable_rooms = [
        room for room in rooms
        if room["capacity"] >= exam.students
    ]

    
    suitable_rooms.sort(key=lambda room: room["capacity"])

    
    for room in suitable_rooms:

        booking_data = {
            "room_id": room["id"],
            "booking_date": exam.day.isoformat(),
            "start_hour": exam.start_hour,
            "end_hour": exam.end_hour,
            "purpose": f"Exam {exam.course_code}"
        }

        booking_response = await call_room_booking(
            "PUT",
            f"/bookings/{exam.exam_id}",
            booking_data
        )

        if booking_response.status_code in [200, 201]:
            return {
                "message": "Exam room booked successfully",
                "exam_id": exam.exam_id,
                "course_code": exam.course_code,
                "room": room
            }

        if booking_response.status_code == 409:
            continue

        raise HTTPException(
            status_code=502,
            detail="Unexpected response from Room Booking Service"
        )

    raise HTTPException(
        status_code=409,
        detail="No free room large enough for this exam"
    )