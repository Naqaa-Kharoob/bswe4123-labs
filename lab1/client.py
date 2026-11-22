

import sys
import time

import httpx


def main():
    base_url = sys.argv[1].rstrip("/")
    url = f"{base_url}/info"

    with httpx.Client(timeout=5.0) as client:
        client.get(url)  

        start = time.perf_counter()
        response = client.get(url)
        end = time.perf_counter()

        response.raise_for_status()

        data = response.json()
        rtt_ms = (end - start) * 1000

        print("Server response:", data)
        print(f"Round-trip time: {rtt_ms:.2f} ms")


if __name__ == "__main__":
    main()
