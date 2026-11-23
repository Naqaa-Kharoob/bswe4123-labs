
import httpx

BASE_URL = "http://127.0.0.1:8000"


def show_result(label, response):
    print(f"{label}: {response.status_code}")

    if response.content:
        print(response.json())

    print("-" * 40)



response = httpx.post(
    f"{BASE_URL}/rooms",
    json={
        "id": "C301",
        "building": "Computer Science",
        "capacity": 25
    }
)
show_result("Create room", response)



response = httpx.post(
    f"{BASE_URL}/rooms",
    json={
        "id": "C301",
        "building": "Computer Science",
        "capacity": 25
    }
)
show_result("Duplicate room", response)



response = httpx.post(
    f"{BASE_URL}/rooms",
    json={
        "id": "C302",
        "building": "Computer Science",
        "capacity": 0
    }
)
show_result("Invalid room data", response)



response = httpx.get(f"{BASE_URL}/rooms")
show_result("Get all rooms", response)



response = httpx.get(f"{BASE_URL}/rooms/C301")
show_result("Get existing room", response)



response = httpx.get(f"{BASE_URL}/rooms/UNKNOWN")
show_result("Get unknown room", response)



booking_data = {
    "room_id": "C301",
    "booking_date": "2026-11-25",
    "start_hour": 10,
    "end_hour": 12,
    "purpose": "Project meeting"
}



response = httpx.put(
    f"{BASE_URL}/bookings/TEST001",
    json=booking_data
)
show_result("Create booking", response)



response = httpx.put(
    f"{BASE_URL}/bookings/TEST001",
    json=booking_data
)
show_result("Repeat same booking", response)



response = httpx.put(
    f"{BASE_URL}/bookings/TEST002",
    json={
        "room_id": "C301",
        "booking_date": "2026-11-25",
        "start_hour": 11,
        "end_hour": 13,
        "purpose": "Another meeting"
    }
)
show_result("Overlapping booking", response)



response = httpx.put(
    f"{BASE_URL}/bookings/TEST003",
    json={
        "room_id": "C301",
        "booking_date": "2026-11-25",
        "start_hour": 12,
        "end_hour": 13,
        "purpose": "Project discussion"
    }
)
show_result("Adjacent booking", response)



response = httpx.put(
    f"{BASE_URL}/bookings/TEST004",
    json={
        "room_id": "C301",
        "booking_date": "2026-11-25",
        "start_hour": 14,
        "end_hour": 10,
        "purpose": "Invalid meeting"
    }
)
show_result("Invalid booking time", response)



response = httpx.put(
    f"{BASE_URL}/bookings/TEST005",
    json={
        "room_id": "UNKNOWN",
        "booking_date": "2026-11-25",
        "start_hour": 14,
        "end_hour": 16,
        "purpose": "Unknown room meeting"
    }
)
show_result("Booking with unknown room", response)



response = httpx.get(
    f"{BASE_URL}/bookings/TEST001"
)
show_result("Get existing booking", response)



response = httpx.get(
    f"{BASE_URL}/bookings/UNKNOWN"
)
show_result("Get unknown booking", response)



response = httpx.delete(
    f"{BASE_URL}/bookings/TEST003"
)
show_result("Delete booking", response)



response = httpx.delete(
    f"{BASE_URL}/bookings/UNKNOWN"
)
show_result("Delete unknown booking", response)
