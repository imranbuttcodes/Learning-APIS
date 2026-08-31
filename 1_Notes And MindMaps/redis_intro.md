# Redis — Learning & Command Cheat Sheet

## 1. What is Redis?

**Redis (Remote Dictionary Server)** is an **in-memory data store**.

In simple terms:

> Redis stores data primarily in **RAM**, allowing applications to read and write data extremely quickly.

It works mainly using **keys and values**:

```text
KEY              VALUE
──────────────────────────
name             "Imran"
age              21
city             "Lahore"
```

For example:

```redis
SET name "Imran"
```

stores:

```text
name → Imran
```

and:

```redis
GET name
```

retrieves:

```text
"Imran"
```

---

## 2. Why Do We Use Redis?

The main reason is **speed**.

A typical application might look like:

```text
Client
   │
   ▼
FastAPI / Backend
   │
   ▼
PostgreSQL / MySQL
   │
   ▼
Disk
```

Databases such as PostgreSQL are designed for **durable, structured, persistent data**.

But sometimes your application needs to access the same piece of data **thousands or millions of times**.

Instead of repeatedly asking the database:

```text
Application
    │
    ├──► Database
    ├──► Database
    ├──► Database
    ├──► Database
    └──► Database
```

we can use Redis as a fast layer:

```text
                 ┌──────────────┐
                 │    Redis     │
                 │    RAM       │
                 └──────▲───────┘
                        │
Client ──► FastAPI ─────┤
                        │
                 Cache Miss
                        │
                        ▼
                 ┌──────────────┐
                 │  PostgreSQL  │
                 │    Disk      │
                 └──────────────┘
```

The application first checks Redis.

If the data is there:

```text
FastAPI → Redis → Data
```

If it isn't:

```text
FastAPI → Redis → MISS
              ↓
          PostgreSQL
              ↓
          Redis stores it
              ↓
          FastAPI gets it
```

This is called **caching**.

---

# 3. Redis vs Traditional Database

Redis and PostgreSQL aren't competitors in the simple sense.

They are often used **together**.

| Redis                            | PostgreSQL                        |
| -------------------------------- | --------------------------------- |
| Primarily in-memory              | Primarily disk-based              |
| Extremely fast                   | Very powerful relational database |
| Great for temporary/hot data     | Great for permanent data          |
| Key-value & rich data structures | Tables, rows, relationships       |
| Caching                          | Primary application database      |
| Sessions                         | Permanent user records            |
| Rate limiting                    | Complex queries                   |
| Queues                           | Transactions & relational data    |

A common architecture is:

```text
              ┌──────────────┐
              │   FastAPI    │
              └──────┬───────┘
                     │
             ┌───────┴───────┐
             ▼               ▼
       ┌──────────┐    ┌────────────┐
       │  Redis   │    │ PostgreSQL │
       └──────────┘    └────────────┘
          Fast             Persistent
```

---

# 4. Common Redis Use Cases

Redis is commonly used for:

### ⚡ Caching

Store frequently accessed data.

```text
API → Redis → cached response
```

### 🔐 Sessions

Store temporary login/session information.

```text
session:abc123 → user:101
```

### 🚦 Rate Limiting

Track how many requests a user has made.

```text
requests:user:101 → 47
```

### 📬 Queues

Store jobs waiting for workers.

```text
Redis List
   ↓
job1
job2
job3
```

### 🏆 Leaderboards

Sorted Sets can maintain rankings.

```text
Imran → 950
Ali   → 900
Ahmed → 870
```

### ⏱️ Temporary Data

Redis supports automatic expiration.

```text
OTP → 123456
TTL → 60 seconds
```

After 60 seconds, Redis can automatically remove it.

---

# 5. Redis Data Structures

Redis isn't limited to simple strings.

It provides several useful data structures:

```text
Redis
│
├── String
├── List
├── Hash
├── Set
└── Sorted Set
```

Think of them as different tools for different problems.

```text
STRING
  ↓
Simple values / counters

LIST
  ↓
Ordered collections / queues

HASH
  ↓
Objects / records

SET
  ↓
Unique values

SORTED SET
  ↓
Rankings / leaderboards
```

---

# 6. Redis CLI

Start the Redis command-line client:

```bash
redis-cli
```

You should see:

```text
127.0.0.1:6379>
```

Meaning:

```text
127.0.0.1 → Redis is running locally
6379      → Redis default port
```

Test the connection:

```redis
PING
```

Response:

```text
PONG
```

---

# 7. Strings

Strings are Redis's simplest data type.

## SET

Store a value.

```redis
SET name "Imran"
```

## GET

Retrieve a value.

```redis
GET name
```

## DEL

Delete a key.

```redis
DEL name
```

---

## MSET

Set multiple values at once.

```redis
MSET name "Imran" age 21 city "Lahore"
```

## MGET

Retrieve multiple values at once.

```redis
MGET name age city
```

---

## STRLEN

Get the length of a string.

```redis
SET name "Imran"
STRLEN name
```

Result:

```text
5
```

---

## GETRANGE

Retrieve part of a string.

```redis
SET name "Imran"
GETRANGE name 0 2
```

Result:

```text
"Ima"
```

Indexes start at `0`:

```text
I  m  r  a  n
0  1  2  3  4
```

---

# 8. Numeric Operations

Redis Strings can represent numbers.

## INCR

Increase by `1`.

```redis
SET count 10
INCR count
```

```text
10 → 11
```

---

## DECR

Decrease by `1`.

```redis
DECR count
```

```text
11 → 10
```

---

## INCRBY

Increase by a specific amount.

```redis
INCRBY count 5
```

```text
10 → 15
```

---

## DECRBY

Decrease by a specific amount.

```redis
DECRBY count 3
```

```text
15 → 12
```

---

## INCRBYFLOAT

Increase a floating-point value.

```redis
SET price 10.5
INCRBYFLOAT price 2.5
```

Result:

```text
13
```

---

# 9. Expiration / TTL

One of Redis's very useful features is **automatic expiration**.

## EXPIRE

Set expiration time in seconds.

```redis
SET session "logged_in"
EXPIRE session 60
```

The key expires after 60 seconds.

---

## TTL

Check remaining time.

```redis
TTL session
```

Example:

```text
(integer) 42
```

Special values:

```text
-1 → key exists but has no expiration
-2 → key doesn't exist
```

---

## SETEX

Set a value with an expiration time.

```redis
SETEX session 60 "logged_in"
```

Modern Redis code commonly uses:

```redis
SET session "logged_in" EX 60
```

---

# 10. Key Management

## KEYS

Find keys matching a pattern.

```redis
KEYS *
```

Find user keys:

```redis
KEYS user:*
```

⚠️ **Don't use `KEYS *` on a large production Redis database.**

It can block Redis while scanning all matching keys.

For production, use:

```redis
SCAN 0
```

We'll learn `SCAN` later.

---

## DEL

Delete a key.

```redis
DEL user:1
```

---

# 11. Lists

A Redis List is an **ordered collection**.

Think of it as:

```text
LEFT                         RIGHT
 ↓                             ↓
[ A ][ B ][ C ][ D ]
```

---

## LPUSH

Add to the left.

```redis
LPUSH tasks "task1"
LPUSH tasks "task2"
LPUSH tasks "task3"
```

Result:

```text
[task3, task2, task1]
```

---

## RPUSH

Add to the right.

```redis
RPUSH tasks "task4"
```

Result:

```text
[task3, task2, task1, task4]
```

---

## LRANGE

Retrieve a range of elements.

```redis
LRANGE tasks 0 -1
```

Meaning:

```text
0  → first element
-1 → last element
```

---

## LLEN

Get the number of elements.

```redis
LLEN tasks
```

---

## LINDEX

Get an element using its index.

```redis
LINDEX tasks 0
```

Example:

```text
[task3, task2, task1]

   0      1      2
```

---

## LPOP

Remove and return the leftmost element.

```redis
LPOP tasks
```

---

## RPOP

Remove and return the rightmost element.

```redis
RPOP tasks
```

---

# 12. Updating Lists

## LSET

Replace an element at a specific index.

```redis
LSET tasks 0 "new_task"
```

Example:

```text
Before:
[task3, task2, task1]

LSET tasks 0 "hello"

After:
[hello, task2, task1]
```

---

# 13. Inserting Into Lists

## LINSERT

Insert before or after another element.

Before:

```redis
LINSERT tasks BEFORE "task2" "new_task"
```

After:

```redis
LINSERT tasks AFTER "task2" "new_task"
```

Example:

```text
Before:

[task1, task2, task3]

After:

[task1, new_task, task2, task3]
```

---

# 14. LPUSHX

Push to the left **only if the list already exists**.

```redis
LPUSHX tasks "task0"
```

Difference:

```text
LPUSH
  ↓
Creates list if it doesn't exist

LPUSHX
  ↓
Doesn't create list
```

---

# 15. Blocking Lists

## BLPOP

`BLPOP` means **Blocking Left Pop**.

Normal:

```redis
LPOP tasks
```

If the list is empty, Redis immediately returns `nil`.

But:

```redis
BLPOP tasks 30
```

means:

> Wait for an element to become available, for up to 30 seconds.

This makes it useful for queues.

```text
Producer
   │
   │ LPUSH
   ▼
┌─────────────┐
│ Redis List  │
│             │
│ job3        │
│ job2        │
│ job1        │
└──────┬──────┘
       │
       │ BLPOP
       ▼
    Worker
```

---

# 16. SORT

Sort elements.

Example:

```redis
LPUSH numbers 5
LPUSH numbers 2
LPUSH numbers 9
LPUSH numbers 1
```

Then:

```redis
SORT numbers
```

Result:

```text
1
2
5
9
```

Descending:

```redis
SORT numbers DESC
```

---

# 17. Quick Command Reference

## Strings

| Command                  | Purpose             |
| ------------------------ | ------------------- |
| `SET key value`          | Store value         |
| `GET key`                | Retrieve value      |
| `DEL key`                | Delete key          |
| `MSET k1 v1 k2 v2`       | Set multiple values |
| `MGET k1 k2`             | Get multiple values |
| `STRLEN key`             | Get string length   |
| `GETRANGE key start end` | Get substring       |

## Numbers

| Command             | Purpose        |
| ------------------- | -------------- |
| `INCR key`          | Increase by 1  |
| `DECR key`          | Decrease by 1  |
| `INCRBY key n`      | Increase by n  |
| `DECRBY key n`      | Decrease by n  |
| `INCRBYFLOAT key n` | Increase float |

## Expiration

| Command                   | Purpose             |
| ------------------------- | ------------------- |
| `EXPIRE key seconds`      | Set expiration      |
| `TTL key`                 | Check remaining TTL |
| `SETEX key seconds value` | Set + expiration    |

## Keys

| Command        | Purpose                     |
| -------------- | --------------------------- |
| `KEYS pattern` | Find matching keys          |
| `DEL key`      | Delete key                  |
| `SCAN cursor`  | Safely iterate through keys |

## Lists

| Command                                | Purpose                  |
| -------------------------------------- | ------------------------ |
| `LPUSH key value`                      | Add to left              |
| `RPUSH key value`                      | Add to right             |
| `LPOP key`                             | Remove from left         |
| `RPOP key`                             | Remove from right        |
| `LRANGE key start stop`                | Get range                |
| `LLEN key`                             | Get list length          |
| `LINDEX key index`                     | Get element by index     |
| `LSET key index value`                 | Replace element          |
| `LINSERT key BEFORE/AFTER pivot value` | Insert element           |
| `LPUSHX key value`                     | Push only if list exists |
| `BLPOP key timeout`                    | Blocking left pop        |
| `SORT key`                             | Sort elements            |

---

# 18. Mental Model

Don't memorize Redis commands as one giant list.

Think in categories:

```text
                         REDIS
                           │
       ┌───────────────────┼───────────────────┐
       │                   │                   │
    STRINGS              LISTS              KEYS
       │                   │                   │
   SET / GET            LPUSH / RPUSH       KEYS
   MGET / MSET          LPOP / RPOP         DEL
   STRLEN               LRANGE              SCAN
   GETRANGE             LLEN
                        LINDEX
                        LSET
                        LINSERT
                        LPUSHX
                        BLPOP
                        SORT
       │
       ├──────────── NUMBERS
       │
       │   INCR
       │   DECR
       │   INCRBY
       │   DECRBY
       │   INCRBYFLOAT
       │
       └──────────── EXPIRATION
           
           EXPIRE
           TTL
           SETEX
           SET ... EX
```

---

# 19. What We Have Learned

So far, we understand:

```text
✅ What Redis is
✅ Why Redis is used
✅ Redis vs PostgreSQL
✅ Redis architecture
✅ Redis CLI
✅ Strings
✅ Numeric operations
✅ Expiration / TTL
✅ Key management
✅ Lists
✅ Blocking lists
✅ Basic sorting
```

Next:

```text
Redis Data Structures
        │
        ├── Strings       ✅
        ├── Lists         ✅
        ├── Hashes        ⬅ NEXT
        ├── Sets          ⬅ NEXT
        └── Sorted Sets   ⬅ NEXT
```

After that, we'll move from **Redis commands → actually using Redis in Python → Redis + FastAPI → caching → real backend architecture**.
