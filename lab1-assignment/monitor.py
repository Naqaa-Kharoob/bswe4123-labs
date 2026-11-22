
import time
import httpx

SERVICES = {
    
    "Service 1": "http://127.0.0.1:8001/health",
    "Service 2": "http://127.0.0.1:8002/health",
    "Service 3": "http://127.0.0.1:8003/health?delay=0.8",
}

FAILURE_LIMIT = 3

failure_counts = {
    name: 0 for name in SERVICES
}

INTERVAL = 2
TIMEOUT = 1.0
SLOW_THRESHOLD = 0.5


def check_service(client, name, url):
    start = time.perf_counter()

    try:
        response = client.get(url)
        response.raise_for_status()

        elapsed = time.perf_counter() - start
        milliseconds = elapsed * 1000

        # Reset failures after a successful response
        failure_counts[name] = 0

        if elapsed > SLOW_THRESHOLD:
            status = "SLOW"
        else:
            status = "UP"

        return f"{name}: {status} ({milliseconds:.1f} ms)"

    except (httpx.RequestError, httpx.HTTPStatusError):
        failure_counts[name] += 1

        if failure_counts[name] >= FAILURE_LIMIT:
            return f"{name}: DOWN (Failed {failure_counts[name]} times)"

        return f"{name}: CHECKING ({failure_counts[name]}/{FAILURE_LIMIT} failures)"


def main():
    print("Starting service monitor...")

    start_time = time.monotonic()

    with httpx.Client(timeout=TIMEOUT) as client:
        round_number = 1

        while time.monotonic() - start_time < 60:
            print(f"\n--- Round {round_number} ---")

            for name, url in SERVICES.items():
                result = check_service(client, name, url)
                print(result)

            round_number += 1
            time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
