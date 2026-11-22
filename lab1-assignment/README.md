# Lab Assignment 1: Is the Service Up, Slow or Down?

## 1. Introduction

In this assignment, I created a simple monitoring program to check three services running on different ports (8001, 8002, and 8003).

The main idea is to know if each service is working normally, responding slowly, or not responding at all.

## 2. Running the Services

First, I added a `/health` endpoint to `service.py`. It returns the service status and the time since the service started.

Then, I ran three copies of the same service using three different ports: 8001, 8002, and 8003.

## 3. The Monitoring Program

I created `monitor.py` using the HTTPX library. The program sends a request to the `/health` endpoint of each service every two seconds.

I used these three states:

- **UP:** The service responds in less than or equal to 500 ms.
- **SLOW:** The service responds in more than 500 ms.
- **DOWN:** The service does not respond or returns an HTTP error.

I also set the timeout to 1 second, so the monitor does not wait too long for a response.

## 4. Testing the Services

I tested the monitor by changing the state of the services.

First, all three services were running. Then, I stopped the second service using `Ctrl + C`. The monitor showed that Service 2 was DOWN, while the other services were still working.

After that, I made Service 3 wait for 0.8 seconds before responding. The monitor detected it as SLOW.

One of the results I got was:

```text
Service 1: UP (3.4 ms)
Service 2: DOWN (No response)
Service 3: SLOW (804.7 ms)
```

This showed that the monitor could identify the three different service states.

## 5. Improving Failure Detection

At first, the monitor marked a service as DOWN after one failed check. However, one failed request does not always mean that the service has stopped. It could be a temporary network problem.

To improve this, I added a failure counter for each service. Now, the service is marked as DOWN only after three consecutive failed checks.

If the service responds successfully, its failure counter returns to zero.

## 6. Timeout and Failure Limit

I chose a timeout of 1 second because it gives the service some time to respond without making the monitor wait too long.

I also chose three consecutive failures before marking a service as DOWN.

A shorter timeout can detect problems faster, but it may report a slow service as unavailable. A longer timeout gives services more time to respond, but it makes failure detection slower.

Using three failed checks reduces false alarms, but it also means that detecting a real failure takes more time.