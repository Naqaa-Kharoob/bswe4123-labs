# Lab Assignment 2 – Campus Room Booking Service

## 1. Introduction

In this assignment, I created a simple REST API for managing university rooms and their bookings.

The main idea is to allow students and staff to book rooms for meetings, study groups, and other activities without having two bookings for the same room at the same time.

I used Python, FastAPI, and Pydantic to build the service.

## 2. API Design

I designed the API with the following operations for managing rooms and bookings.

| Method | URI | Request Body | Description | Success Code | Error Codes |
|---|---|---|---|---|---|
| POST | `/rooms` | Room details (id, building, capacity) | Add a new room | 201 | 409, 422 |
| GET | `/rooms` | None | Get all rooms | 200 | — |
| GET | `/rooms/{room_id}` | None | Get a room by its ID | 200 | 404 |
| PUT | `/bookings/{booking_id}` | Booking details (room_id, booking_date, start_hour, end_hour, purpose) | Create a booking | 201 | 404, 409, 422 |
| GET | `/bookings/{booking_id}` | None | Get a booking by its ID | 200 | 404 |
| DELETE | `/bookings/{booking_id}` | None | Delete a booking | 204 | 404 |

When the same booking request is sent again with the same ID and data, the service returns 200 instead of creating another booking.

## 3. Data Validation

I used Pydantic models to check the data before saving it.

For example:
- Room capacity must be at least 1.
- Booking hours must be between 8 and 20.
- The end hour must be greater than the start hour.
- The room must exist before creating a booking.

The service returns different status codes depending on the problem:
- `422`: When the entered data is invalid.
- `404`: When the room or booking does not exist.
- `409`: When the room is already booked at the requested time or the room ID already exists.

## 4. Preventing Overlapping Bookings

One important part of this assignment was preventing two bookings from using the same room at overlapping times.

Before saving a new booking, I check the existing bookings. If the room and date are the same and the times overlap, the service rejects the new booking with `409 Conflict`.

For example, if a room is booked from 10:00 to 12:00, another booking from 11:00 to 13:00 is not allowed. But a booking from 12:00 to 13:00 is allowed.

## 5. Safe Retry

I used the PUT method and allowed the client to choose the booking ID.

If the same request is sent twice with the same ID and the same data, the service returns the existing booking with status code `200` without saving it again.

I tested this by sending the same booking request twice. The first request returned `201`, and the second returned `200`.

## 6. Testing

I created a Python client file called `test_bookings.py` and used the HTTPX library to test the API.

The tests include:
- Adding rooms and getting room information.
- Trying to add the same room twice.
- Testing invalid room data.
- Creating and retrieving bookings.
- Testing overlapping and adjacent bookings.
- Testing invalid booking times.
- Trying to book a room that does not exist.
- Sending the same booking request twice.
- Deleting bookings.

### Test Results

I ran the client using:

```bash
python test_bookings.py
```

**Output:**

Create room: 201
{'id': 'C301', 'building': 'Computer Science', 'capacity': 25}
----------------------------------------
Duplicate room: 409
{'detail': 'Room already exists'}
----------------------------------------
Invalid room data: 422
----------------------------------------
Get all rooms: 200
[{'id': 'C301', 'building': 'Computer Science', 'capacity': 25}]
----------------------------------------
Get existing room: 200
{'id': 'C301', 'building': 'Computer Science', 'capacity': 25}
----------------------------------------
Get unknown room: 404
{'detail': 'Room not found'}
----------------------------------------
Create booking: 201
{'booking_id': 'TEST001', 'room_id': 'C301', 'booking_date': '2026-11-25', 'start_hour': 10, 'end_hour': 12, 'purpose': 'Project meeting'}
----------------------------------------
Repeat same booking: 200
{'room_id': 'C301', 'booking_date': '2026-11-25', 'start_hour': 10, 'end_hour': 12, 'purpose': 'Project meeting'}
----------------------------------------
Overlapping booking: 409
{'detail': 'Room is already booked during this time'}
----------------------------------------
Adjacent booking: 201
{'booking_id': 'TEST003', 'room_id': 'C301', 'booking_date': '2026-11-25', 'start_hour': 12, 'end_hour': 13, 'purpose': 'Project discussion'}
----------------------------------------
Invalid booking time: 422
----------------------------------------
Booking with unknown room: 404
{'detail': 'Room not found'}
----------------------------------------
Get existing booking: 200
{'booking_id': 'TEST001', 'room_id': 'C301', 'booking_date': '2026-11-25', 'start_hour': 10, 'end_hour': 12, 'purpose': 'Project meeting'}
----------------------------------------
Get unknown booking: 404
{'detail': 'Booking not found'}
----------------------------------------
Delete booking: 204
----------------------------------------
Delete unknown booking: 404
{'detail': 'Booking not found'}
----------------------------------------

## 7. Tools Used

- Python
- FastAPI
- Pydantic
- HTTPX