Absolutely bro 🔥. **Before implementing JWT in FastAPI, let's understand JWT itself deeply.** No FastAPI magic yet.

# 🔐 JWT — JSON Web Token

JWT is a **compact, signed token format** that lets a server transmit claims about a user between parties.

The key idea:

> **The server creates a token, signs it, and later verifies that signature to determine whether the token was issued by a trusted server and hasn't been modified.**

---

# 1. What problem does JWT solve?

Imagine you log in:

```text
POST /login

{
    "email": "imran@example.com",
    "password": "secret123"
}
```

The server verifies your credentials.

Now you make another request:

```text
GET /posts
```

The server needs to know:

> "Who is making this request?"

We don't want to send the password every time. ❌

So the server gives you a token:

```text
Login
  ↓
Verify credentials
  ↓
Create JWT
  ↓
Client receives JWT
```

Then:

```text
GET /posts

Authorization: Bearer <JWT>
```

The server verifies the JWT and identifies the user.

---

# 2. What does a JWT look like?

You've probably seen something like:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjMiLCJleHAiOjE3ODAwMDAwMDB9.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

It looks like random garbage 😂.

But it's actually:

```text
HEADER.PAYLOAD.SIGNATURE
```

**Three parts.**

---

# 3. JWT Part #1 — Header

The first section:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
```

decodes conceptually to:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

The header tells us things like:

```text
alg → signing algorithm
typ → token type
```

For example:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

means:

> This JWT uses the HS256 algorithm.

---

# 4. JWT Part #2 — Payload

The second section contains **claims**.

For example:

```json
{
    "sub": "123",
    "exp": 1780000000
}
```

Maybe:

```text
sub = user ID
exp = expiration time
```

You can have other claims too:

```json
{
    "sub": "123",
    "role": "admin",
    "exp": 1780000000
}
```

These are just pieces of information about the token/user/context.

---

# 🚨 VERY IMPORTANT: JWT payload isn't secret

This is one of the biggest JWT misconceptions.

JWT payload is typically **encoded, not encrypted**.

Anyone who possesses the token can decode the header and payload.

So don't put:

```json
{
    "password": "secret123"
}
```

inside a JWT.

Instead:

```json
{
    "sub": "123",
    "role": "admin"
}
```

is reasonable if appropriate.

Think:

```text
Encoding ≠ Encryption
```

---

# 5. JWT Part #3 — Signature

This is the really important part.

The server signs the token.

Conceptually:

```text
HEADER
   +
PAYLOAD
   +
SECRET KEY
   ↓
SIGNATURE
```

For HMAC/HS256, conceptually:

```text
HMAC-SHA256(
    base64url(header)
    + "."
    + base64url(payload),
    SECRET_KEY
)
```

You don't normally calculate this yourself; a JWT library does it.

The resulting signature becomes the third section:

```text
HEADER.PAYLOAD.SIGNATURE
```

---

# 6. Why do we need the signature?

Because the client can see the payload.

Suppose the token says:

```json
{
    "sub": "123",
    "role": "user"
}
```

A malicious client might try changing it to:

```json
{
    "sub": "123",
    "role": "admin"
}
```

They can modify the encoded payload.

But they **can't create a valid signature** without the signing secret/private key.

So the server calculates the expected signature again.

```text
Received JWT
     │
     ▼
Read Header + Payload
     │
     ▼
Calculate expected signature
     │
     ├──────────────┐
     │              │
   Match          Don't Match
     │              │
     ▼              ▼
  Valid            ❌
```

That's the fundamental security mechanism.

---

# 7. The complete JWT flow

Now put everything together.

### Login

```text
Client
  │
  │ email + password
  ▼
FastAPI
  │
  │ verify password hash
  ▼
User authenticated
  │
  │
  ▼
Create JWT
  │
  ├── Header
  ├── Payload
  └── Signature
  │
  ▼
Client
```

The client now has:

```text
JWT
```

---

# 8. Then the client requests a protected resource

```text
Client
   │
   │ GET /posts
   │
   │ Authorization: Bearer <JWT>
   ▼
FastAPI
```

FastAPI:

```text
JWT
 │
 ▼
Decode
 │
 ▼
Verify signature
 │
 ▼
Check expiration
 │
 ▼
Read user ID (`sub`)
 │
 ▼
Find user
 │
 ▼
Allow request
```

🔥 That's authentication using JWT.

---

# 9. What is `Bearer`?

You'll eventually write:

```text
Authorization: Bearer eyJhbGci...
```

`Bearer` basically means:

> "The person presenting this token is using it as their credential."

So:

```text
Authorization:
    Bearer <token>
```

has two parts:

```text
Authorization
      │
      └── Bearer <JWT>
```

The JWT is the credential.

---

# 10. JWT claims you should know

You don't need to memorize every possible claim.

These are the important ones:

### `sub`

Subject.

Usually we use it for the user's identifier:

```json
{
    "sub": "123"
}
```

Meaning:

```text
This token belongs to user 123.
```

---

### `exp`

Expiration time.

```json
{
    "exp": 1780000000
}
```

After this time, the token should no longer be accepted.

---

### `iat`

Issued-at time.

```json
{
    "iat": 1779990000
}
```

When the token was created.

---

### `iss`

Issuer.

```json
{
    "iss": "my-api"
}
```

Identifies who issued the token.

---

### `aud`

Audience.

```json
{
    "aud": "my-api-users"
}
```

Identifies the intended recipient/audience.

---

# 11. Why do we use `sub` for user ID?

You'll see this constantly in FastAPI tutorials:

```python
{
    "sub": str(user.id)
}
```

Why?

Because `sub` means **subject**.

The subject of the token is:

```text
User #42
```

So:

```json
{
    "sub": "42"
}
```

means:

> This token represents subject 42.

Later:

```python
user_id = payload.get("sub")
```

and we can find:

```text
User #42
```

in PostgreSQL.

---

# 12. JWT doesn't automatically mean "authentication"

This distinction is important.

JWT itself is just a **token format**.

You can put:

```json
{
    "sub": "123"
}
```

inside a JWT.

But your application still has to decide:

```text
Is the signature valid?
Is it expired?
Does this user exist?
Is this user allowed to do this?
```

JWT gives you a mechanism for carrying/verifying claims.

Your application provides the authentication/authorization logic around it.

---

# 13. JWT vs Session

Now you'll understand the difference much better.

### Session

```text
Client
  │
  │ session_id
  ▼
Server
  │
  ▼
Session Store
  │
  ▼
User
```

The server remembers the session.

### JWT

```text
Client
  │
  │ JWT
  ▼
Server
  │
  ├── verify signature
  ├── check expiration
  └── read claims
```

The token itself carries claims.

---

# 14. JWT doesn't mean "stateless everything"

You'll often hear:

> "JWT makes your API stateless."

That's an oversimplification.

You can validate a JWT without a session store, which can reduce server-side session state.

But your application might **still query PostgreSQL**:

```text
JWT
 ↓
sub = 42
 ↓
SELECT user WHERE id = 42
```

So:

```text
JWT ≠ No Database
```

It means you don't necessarily need a **server-side session record for every token**.

---

# 15. HS256 vs RS256

You'll encounter these.

### HS256

Symmetric signing:

```text
        SECRET
       /      \
      /        \
Server       Server
```

The same secret is used to sign and verify.

Good for a simple single-service setup.

### RS256

Asymmetric cryptography:

```text
Private Key
    ↓
  Sign

Public Key
    ↓
 Verify
```

This becomes useful when multiple services need to verify tokens without having access to the private signing key.

For our learning project, we'll likely start with **HS256** because it's simpler to understand.

---

# 16. The biggest JWT misconceptions

Keep these straight:

```text
❌ JWT is encryption
✅ JWT is usually signed, not encrypted

❌ JWT hides the payload
✅ JWT payload is readable

❌ JWT automatically authenticates users
✅ Your application verifies the token and uses its claims

❌ JWT means no database
✅ You may still query your database

❌ JWT is always better than sessions
✅ Both have tradeoffs
```

---

# 🧠 The entire thing in one diagram

```text
                     LOGIN
                       │
                       ▼
              Email + Password
                       │
                       ▼
                Verify Password
                       │
                       ▼
                 Create JWT
                       │
              ┌────────┴────────┐
              │                 │
           HEADER             PAYLOAD
              │                 │
          alg: HS256          sub: 42
          typ: JWT             exp: ...
              │                 │
              └────────┬────────┘
                       │
                       ▼
                  SIGNATURE
                       │
                       ▼
             HEADER.PAYLOAD.SIGNATURE
                       │
                       ▼
                     CLIENT
                       │
                       │ Authorization:
                       │ Bearer <JWT>
                       ▼
                    FastAPI
                       │
                       ▼
                Verify Signature
                       │
                 ┌─────┴─────┐
                 │           │
               Valid       Invalid
                 │           │
                 ▼           ▼
            Check `exp`      401
                 │
                 ▼
            Read `sub`
                 │
                 ▼
             User #42
                 │
                 ▼
          Authorization check
                 │
                 ▼
            Protected API
```

## 🔥 The one sentence I want you to remember

> **A JWT is a signed token containing claims; the server verifies its signature and validity, then uses those claims—often `sub`—to identify the requester.**
