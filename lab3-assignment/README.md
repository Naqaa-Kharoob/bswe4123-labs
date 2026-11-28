# Lab Assignment 3 – Exam Scheduler Service

## 1. Introduction

In this lab, I worked on building an Exam Scheduler Service using FastAPI.

The main idea is to make the process of booking rooms for exams easier. Instead of choosing a room manually, the service checks the available rooms and selects the smallest room that can fit all students.

The project contains two services:

- **Room Booking Service:** Used to manage rooms and their bookings.
- **Exam Scheduler Service:** Receives exam information and chooses a suitable room by communicating with the Room Booking Service.

## 2. Project Structure

The project contains the following files:

```text
lab3-assignment/
├── room_booking_service/
│   ├── service.py
│   └── requirements.txt
├── exam_scheduler_service/
│   ├── service.py
│   └── requirements.txt
└── README.md
```

## 3. Running the Services

I used two different ports to run the services.

### First: Room Booking Service

I opened a terminal and ran:

```powershell
cd lab3-assignment/room_booking_service
uvicorn service:app --reload --port 8001
```

The service runs on:

http://127.0.0.1:8001/docs

### Second: Exam Scheduler Service

I opened another terminal and ran:

```powershell
cd lab3-assignment/exam_scheduler_service
uvicorn service:app --reload --port 8002
```

The service runs on:

http://127.0.0.1:8002/docs

I kept both services running at the same time so they could communicate with each other.

## 4. Environment Variables and Configuration

I used environment variables to control the connection settings between the two services.

The settings are:

- `ROOM_BOOKING_URL`: The address of the Room Booking Service.
- `ROOM_BOOKING_TIMEOUT`: The maximum time to wait for a response.
- `ROOM_BOOKING_MAX_RETRIES`: The maximum number of additional attempts.

I also added a `GET /config` endpoint to show the settings currently used by the Exam Scheduler Service.

To check the configuration, I opened:

http://127.0.0.1:8002/config

## 5. Retry Mechanism

I added a retry mechanism to handle temporary problems when communicating with the Room Booking Service.

When a request fails because of a timeout, connection error, or a server error (5xx), the Exam Scheduler Service tries again.

The waiting time increases with every retry:

- First retry: 0.5 seconds.
- Second retry: 1 second.
- Third retry: 2 seconds.

The service does not retry requests that return 404 or 409.

### Why is the booking request safe to retry?

I used the exam ID as the booking ID when sending the booking request.

The Room Booking Service uses the PUT method and checks whether the booking ID already exists. If the same ID is sent again with the same booking information, it returns the existing booking instead of creating another one.

This helps prevent the same exam from being booked twice.

### Retry Test

I tested this by following these steps:

1. I stopped the Room Booking Service.
2. I sent a new exam request through the Exam Scheduler Service.
3. The connection failed because the Room Booking Service was stopped.
4. I restarted the Room Booking Service while the scheduler was retrying.
5. The request succeeded after the service became available again.

The final result was a successful booking with status code `201`.

## 6. Adding Delay to the Room Booking Service

I added a delay to the Room Booking Service using the environment variable:

`ROOM_BOOKING_DELAY`

This helped me test how the Exam Scheduler Service behaves when the other service is slow.

I used different delay and timeout values to compare the results.

## 7. Experiment Results

I tested three different combinations of delay and timeout.

| Experiment | Delay | Timeout | Status Code | Response Time |
|---|---:|---:|---:|---:|
| 1 | 0.5 s | 2 s | 201 | 1.24 s |
| 2 | 3 s | 1 s | 503 | 8.15 s |
| 3 | 3 s | 5 s | 201 | 6.18 s |

### Explanation of the Results

**Experiment 1:**

The delay was 0.5 seconds and the timeout was 2 seconds. The request succeeded and returned `201` because the service responded within the allowed time.

**Experiment 2:**

The delay was 3 seconds and the timeout was only 1 second. The request timed out, so the scheduler tried again. After all retry attempts failed, the service returned `503`.

The total response time was longer because of the retry attempts and the increasing waiting time between them.

**Experiment 3:**

The delay was 3 seconds and the timeout was 5 seconds. The request succeeded and returned `201`.

The response time was about 6.18 seconds because the scheduler made two requests to the Room Booking Service: one to get the rooms and another to book the selected room. Each request had a delay of 3 seconds.

### What I noticed

From these experiments, I noticed that the timeout value affects whether the request succeeds or fails when the other service is slow.

A short timeout makes the service respond with an error sooner, but it may cause requests to fail even when the other service is still working.

A longer timeout gives the other service more time to respond, but the user may have to wait longer.

## 8. Conclusion

In this lab, I learned how to make two FastAPI services communicate using HTTP requests.

I also practiced using environment variables, handling connection errors and timeouts, implementing retries with exponential backoff, and measuring response times.

The experiments helped me understand how delays and timeout settings affect communication between services.