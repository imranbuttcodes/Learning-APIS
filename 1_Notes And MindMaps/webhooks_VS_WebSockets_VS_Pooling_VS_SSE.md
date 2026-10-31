# Polling vs Server-Sent Events (SSE) vs WebSockets vs Webhooks

## 1. Introduction

Polling, Server-Sent Events (SSE), WebSockets, and Webhooks are communication mechanisms used by applications to exchange information between clients, servers, and external services.

Although they can achieve similar goals, their communication models and use cases are different.

The fundamental differences are:

- **Polling:** The client repeatedly asks the server for updates.
- **SSE:** The server continuously sends updates to the client over an HTTP connection.
- **WebSockets:** The client and server communicate bidirectionally over a persistent connection.
- **Webhooks:** An application sends an HTTP request to another application's endpoint when a specific event occurs.

---

# 2. Polling (HTTP Polling)

## What is Polling?

Polling is a communication technique in which a client repeatedly sends HTTP requests to a server at regular intervals to check whether new information is available.

The client initiates every request.

### How It Works

1. The client sends an HTTP request to the server.
2. The server checks for new information.
3. The server sends a response.
4. The client waits for a specified interval.
5. The client sends another request.

### Architecture

```text
Client                         Server
   |                              |
   |--------- Request ----------->|
   |<-------- Response -----------|
   |                              |
   |         Wait 3 seconds       |
   |                              |
   |--------- Request ----------->|
   |<-------- New Data -----------|
   |                              |
   |         Wait 3 seconds       |
   |                              |
   |--------- Request ----------->|
   |<-------- Response -----------|
```

### Example

Imagine a task-processing application.

The frontend needs to know whether a background task has finished.

It periodically requests:

```http
GET /api/task/123/status
```

The server responds:

```json
{
    "status": "processing"
}
```

After a few seconds, the client sends another request.

Eventually, the server responds:

```json
{
    "status": "completed"
}
```

### Advantages

- Easy to implement.
- Uses standard HTTP requests.
- Compatible with almost all HTTP servers.
- No persistent connection required.

### Disadvantages

- Generates unnecessary requests when no updates are available.
- Updates are delayed until the next polling interval.
- Can increase server load.
- Frequent polling wastes network resources.

### Use Cases

- Checking background task status.
- Periodically refreshing dashboards.
- Checking notification counts.
- Monitoring long-running operations.

## 2.1 Long Polling

Long Polling is an improved variation of traditional polling.

Instead of immediately responding when no new information is available, the server keeps the HTTP request open until:

- New information becomes available.
- A timeout occurs.

After receiving a response, the client sends another request.

```text
Client                         Server
   |                              |
   |--------- Request ----------->|
   |                              |
   |       Server waits...         |
   |                              |
   |       New event occurs        |
   |                              |
   |<-------- New Data -----------|
   |                              |
   |--------- Request ----------->|
```

**Main difference:**

- Traditional Polling: The server responds immediately.
- Long Polling: The server waits for new information before responding.

Long Polling reduces unnecessary requests when compared with frequent traditional polling.

---

# 3. Server-Sent Events (SSE)

## What is SSE?

Server-Sent Events (SSE) is a communication mechanism that allows a server to continuously send real-time updates to a client through a persistent HTTP connection.

SSE provides one-way communication:

**Server → Client**

The client establishes the connection, and the server sends events whenever new information becomes available.

### How It Works

1. The client establishes an SSE connection.
2. The server accepts the connection.
3. The connection remains open.
4. The server sends events whenever updates are available.
5. The client receives and processes these events.

### Architecture

```text
Client                         Server
   |                              |
   |------ Establish SSE -------->|
   |<--------- Connected ---------|
   |                              |
   |<--------- Event 1 ------------|
   |                              |
   |<--------- Event 2 ------------|
   |                              |
   |<--------- Event 3 ------------|
   |                              |
   |<--------- Event 4 ------------|
```

Unlike Polling, the client does not repeatedly request updates.

### Example

Imagine an AI application that generates responses using an LLM.

Instead of waiting for the entire response, the server streams generated content progressively.

```text
Server → "Artificial"
Server → " Intelligence"
Server → " is"
Server → " a field"
Server → " of computer science..."
```

The frontend displays the response as it arrives.

### SSE Technical Details

SSE uses the HTTP protocol and typically uses the following content type:

```http
Content-Type: text/event-stream
```

Events are sent as text in a specific format:

```text
data: Hello

data: World

```

Each event is separated by a blank line.

### Browser Implementation

The browser provides the `EventSource` API.

```javascript
const source = new EventSource("/stream");

source.onmessage = (event) => {
    console.log(event.data);
};

source.onerror = (error) => {
    console.log("Connection error", error);
};
```

The browser automatically attempts to reconnect when the connection is interrupted.

### FastAPI Implementation

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()

@app.get("/stream")
async def stream():

    async def generate():

        for i in range(5):
            yield f"data: Update {i}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

### Advantages

- Real-time server-to-client communication.
- No repeated polling requests.
- Uses standard HTTP.
- Automatic reconnection through the browser's EventSource API.
- Useful for streaming text and notifications.

### Disadvantages

- One-way communication only.
- Primarily designed for text-based event streams.
- Browser EventSource does not support arbitrary custom authorization headers.
- Requires proper connection and resource management.

### Use Cases

- Streaming AI-generated responses.
- Live notifications.
- Stock price updates.
- Background task progress.
- Real-time dashboards.

---

# 4. WebSockets

## What are WebSockets?

WebSockets provide full-duplex, bidirectional communication between a client and a server through a persistent connection.

Full-duplex means both sides can send and receive messages independently.

**Client ↔ Server**

Unlike SSE, WebSockets allow both the client and server to initiate communication at any time.

### How It Works

1. The client initiates a WebSocket handshake over HTTP.
2. The server accepts the handshake.
3. The connection is upgraded to the WebSocket protocol.
4. The connection remains open.
5. Both sides can exchange messages independently.

### Architecture

```text
Client                         Server
   |                              |
   |--------- Handshake --------->|
   |<-------- Connection ---------|
   |                              |
   |---------- Message ----------->|
   |<--------- Response -----------|
   |                              |
   |<--------- Notification -------|
   |                              |
   |---------- Message ----------->|
   |                              |
   |<--------- New Message --------|
```

### WebSocket Protocol

WebSockets use the following URI schemes:

```text
ws://
wss://
```

- `ws://` : WebSocket connection without transport encryption.
- `wss://` : WebSocket connection secured using TLS.

The WebSocket protocol is standardized by RFC 6455.

### FastAPI Implementation

```python
from fastapi import FastAPI, WebSocket

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    while True:

        message = await websocket.receive_text()

        await websocket.send_text(
            f"Server received: {message}"
        )
```

### Client-Side JavaScript

```javascript
const socket = new WebSocket("ws://localhost:8000/ws");

socket.onopen = () => {
    socket.send("Hello Server!");
};

socket.onmessage = (event) => {
    console.log(event.data);
};

socket.onclose = () => {
    console.log("Connection closed");
};
```

### Advantages

- Bidirectional communication.
- Low-latency message exchange.
- Persistent connection.
- Supports text and binary data.
- Suitable for interactive real-time applications.

### Disadvantages

- More complex to implement than ordinary HTTP requests.
- Requires connection lifecycle management.
- Reconnection logic must generally be implemented by the application.
- Scaling requires managing concurrent connections.
- Message delivery, ordering, and persistence may require additional application-level mechanisms.

### Use Cases

- Real-time chat applications.
- Multiplayer games.
- Collaborative document editors.
- Live trading platforms.
- Interactive dashboards.

---

# 5. Webhooks

## What is a Webhook?

A Webhook is an event-driven communication mechanism that allows one application to notify another application automatically when a specific event occurs.

The event-producing application sends an HTTP request, usually a POST request, to an endpoint exposed by the receiving application.

In simple terms:

**When something happens, send an HTTP request to notify another application.**

Unlike Polling, the receiving application does not need to repeatedly ask whether an event has occurred.

### How It Works

Imagine an e-commerce application using Stripe for payment processing.

1. A customer makes a payment.
2. Stripe processes the payment.
3. Stripe detects a successful payment event.
4. Stripe sends an HTTP POST request to your backend.
5. Your backend receives the event.
6. Your backend updates the order status.

### Architecture

```text
Customer
   |
   | Makes Payment
   |
   v
Stripe Payment Service
   |
   | Detects payment_success event
   |
   |------ HTTP POST Request ------>|
                                    |
                              FastAPI Backend
                                    |
                                    |
                              Verify Signature
                                    |
                                    |
                              Process Event
                                    |
                                    |
                              Update Database
```

### Example

Your FastAPI backend exposes a webhook endpoint:

```python
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/webhooks/payment")
async def payment_webhook(request: Request):

    data = await request.json()

    if data["event"] == "payment_success":

        print("Payment successful!")

        # Update order in database

    return {"received": True}
```

The external service sends an HTTP request:

```http
POST /webhooks/payment
Content-Type: application/json
```

With a JSON payload:

```json
{
    "event": "payment_success",
    "payment_id": "pay_123",
    "amount": 5000,
    "currency": "PKR"
}
```

Your application receives and processes the event.

**Important:** This is a simplified example. In production, always verify the webhook signature before trusting the payload. Also account for retries, duplicate events, and idempotency.

### Real-World Examples

| Service | Event | Webhook Action |
|---|---|---|
| Stripe | Payment successful | Notify backend |
| GitHub | Code pushed | Trigger CI/CD pipeline |
| Twilio | SMS received | Notify application |
| Shopify | New order created | Update external system |

### Advantages

- Event-driven communication.
- No continuous polling required.
- Efficient for application-to-application integrations.
- Uses standard HTTP requests.
- Can trigger automated workflows.

### Disadvantages

- Receiving application needs a publicly reachable endpoint in typical integrations.
- Requires signature verification and security measures.
- Events may be delivered more than once.
- Failed deliveries may require retries.
- Delivery order is not always guaranteed.

### Use Cases

- Payment notifications.
- GitHub CI/CD automation.
- Third-party API integrations.
- Order processing.
- Event-driven workflows.
- Application integrations.

---

# 6. Side-by-Side Comparison

| Feature | Polling | SSE | WebSockets | Webhooks |
|---|---|---|---|---|
| Communication | Repeated requests | Server → Client | Bidirectional | App → App |
| Initiator | Client | Client establishes connection | Client establishes connection | Event source |
| Connection | Repeated HTTP requests | Persistent HTTP | Persistent WebSocket | Individual HTTP requests |
| Real-time | Interval-dependent | Yes | Yes | Event-triggered |
| Bidirectional | No | No | Yes | Not inherently |
| Protocol | HTTP | HTTP | WebSocket | HTTP |
| Automatic reconnection | No | Browser API supports it | Application handles it | Sender retries, depending on provider |
| Complexity | Low | Medium | Higher | Medium |
| Main purpose | Check for updates | Stream updates | Interactive communication | Notify external applications |

---

# 7. Understanding the Fundamental Differences

### Polling

The client keeps asking:

```text
"Is there anything new?"
"Is there anything new?"
"Is there anything new?"
```

### SSE

The client establishes a connection, and the server keeps sending:

```text
Server → Update 1
Server → Update 2
Server → Update 3
```

### WebSockets

Both sides communicate independently:

```text
Client → Message
Server → Response
Server → Notification
Client → Another Message
```

### Webhooks

An external application sends an HTTP request when an event occurs:

```text
Event Occurs
     |
     v
External Application
     |
     | HTTP POST
     v
Your Application's Endpoint
     |
     v
Process Event
```

---

# 8. When Should You Use Each?

| Scenario | Recommended Technology |
|---|---|
| Checking background task status every 10 seconds | Polling |
| Streaming LLM-generated responses | SSE |
| Live notifications from server | SSE |
| Real-time chat application | WebSockets |
| Multiplayer game | WebSockets |
| Collaborative text editor | WebSockets |
| GitHub push event triggering CI/CD | Webhooks |
| Stripe payment confirmation | Webhooks |
| Periodically refreshing a dashboard | Polling |

---

# 9. Can These Technologies Work Together?

Yes!

These technologies are not necessarily alternatives to one another. A single application can use multiple communication mechanisms.

### Example: AI-Powered Document Processing Application

Imagine a user uploads a PDF to an AI application.

The backend processes the document, extracts text, generates embeddings, and stores them in a vector database.

Different communication mechanisms can handle different responsibilities:

| Requirement | Technology |
|---|---|
| Check whether document processing has finished | Polling |
| Stream document processing progress to frontend | SSE |
| Allow interactive real-time communication | WebSockets |
| Notify an external application when processing finishes | Webhooks |

This demonstrates that each technology solves a different communication problem.

---

# 10. Final Takeaways

Remember these four fundamental concepts:

1. **Polling:** Client repeatedly asks the server for updates.
2. **SSE:** Server continuously sends updates to the client.
3. **WebSockets:** Client and server communicate bidirectionally over a persistent connection.
4. **Webhooks:** An application sends an HTTP request to another application's endpoint when a particular event occurs.

The most important distinction is the communication model, not simply whether a technology is real-time.

## Further Learning

- HTTP: https://developer.mozilla.org/en-US/docs/Web/HTTP
- Server-Sent Events: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events
- WebSockets: https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API
- Webhooks: https://docs.github.com/en/webhooks
- FastAPI WebSockets: https://fastapi.tiangolo.com/advanced/websockets/
- FastAPI StreamingResponse: https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
