
from datetime import date

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, model_validator


app = FastAPI(title="Campus Room Booking Service")



class Room(BaseModel):
    id: str = Field(min_length=1)
    building: str = Field(min_length=1)
    capacity: int = Field(ge=1)


class Booking(BaseModel):
    room_id: str
    booking_date: date
    start_hour: int = Field(ge=8, le=20)
    end_hour: int = Field(ge=8, le=20)
    purpose: str = Field(min_length=3)

    @model_validator(mode="after")
    def check_time(self):
        if self.end_hour <= self.start_hour:
            raise ValueError("End hour must be after start hour")
        return self



rooms: dict[str, Room] = {}
bookings: dict[str, Booking] = {}



@app.post("/rooms", status_code=201)
def create_room(room: Room):
    if room.id in rooms:
        raise HTTPException(
            status_code=409,
            detail="Room already exists"
        )

    rooms[room.id] = room
    return room



@app.get("/rooms")
def get_rooms():
    return list(rooms.values())



@app.get("/rooms/{room_id}")
def get_room(room_id: str):
    if room_id not in rooms:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    return rooms[room_id]



@app.put("/bookings/{booking_id}", status_code=201)
def create_booking(booking_id: str, booking: Booking, response: Response):

    
    if booking.room_id not in rooms:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    
    if booking_id in bookings:
        if bookings[booking_id] == booking:
            response.status_code = 200
            return {
                "booking_id": booking_id,
                **booking.model_dump()
            }

        raise HTTPException(
            status_code=409,
            detail="Booking ID already exists with different data"
        )

    
    for existing in bookings.values():
        if (
            existing.room_id == booking.room_id
            and existing.booking_date == booking.booking_date
            and booking.start_hour < existing.end_hour
            and existing.start_hour < booking.end_hour
        ):
            raise HTTPException(
                status_code=409,
                detail="Room is already booked during this time"
            )

    
    bookings[booking_id] = booking

    return {
        "booking_id": booking_id,
        **booking.model_dump()
    }



@app.get("/bookings/{booking_id}")
def get_booking(booking_id: str):
    if booking_id not in bookings:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return {
        "booking_id": booking_id,
        **bookings[booking_id].model_dump()
    }



@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking(booking_id: str):
    if booking_id not in bookings:
        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    del bookings[booking_id]
    return
