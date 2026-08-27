There are two primary ways to remember a user after they log in: traditional **Session-Based Authentication** and modern **Token-Based (JWT) Authentication**.

**Session-Based Authentication (The Old School Way)**

* **The Process:** The user logs in. The server creates a "session" and saves it in its own memory or a database. The server sends a small, random string (a Session ID cookie) back to the user's browser.
* **The Catch:** Every time the user makes a new request, the server has to take that Session ID, query the database, and ask, *"Who does this belong to again?"*
* **The Problem:** Because the server has to actively memorize every single logged-in user, it consumes a ton of server memory. It is notoriously difficult to scale across multiple backend servers and doesn't play nicely with mobile apps.

**Token-Based Authentication (The Modern API Way)**

* **The Process:** The user logs in. The server cryptographically signs a JSON Web Token (JWT) containing the user's ID and hands it back. *Then, the server completely forgets who the user is.*
* **The Catch:** On the next request, the user sends the JWT back to the server. The server doesn't query a database to check if they are logged in—it just checks the cryptographic math on the token's signature. If the math checks out, the server knows the token is authentic and hasn't been tampered with.
* **The Advantage:** It is completely **stateless**. The server uses zero memory tracking logins, scaling infinitely and working perfectly with mobile apps, React frontends, and third-party integrations.

| Feature | Session-Based | Token-Based (JWT) |
| --- | --- | --- |
| **State** | Stateful (Server remembers sessions) | Stateless (Server remembers nothing) |
| **Storage Location** | Server Memory / Database | Client-side (Browser/App Storage) |
| **Scalability** | Hard (Requires syncing sessions across servers) | Easy (Math can be verified on any server) |
| **Best For** | Traditional monolithic websites (e.g., standard Django/PHP) | Modern REST APIs, Mobile Apps, Microservices |

Since we are building a decoupled REST API with FastAPI, JWT is the absolute industry standard.


**Bonus**

Authentication
│
├── 1. Session-Based Authentication
│
├── 2. Token-Based Authentication
│      │
│      ├── JWT
│      └── Opaque Tokens
│
├── 3. API Keys
│
└── 4. OAuth 2.0 / OpenID Connect
       │
       ├── Google
       ├── GitHub
       └── Microsoft
