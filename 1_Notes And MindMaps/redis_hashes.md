Absolutely bro. 🔥 **Redis Hashes** are one of the most important Redis data structures for backend development because they map naturally to **objects/records**.

# 🟠 Redis Hashes

Think of a Hash as a **key containing multiple field-value pairs**.

For example, instead of:

```text
user:1:name  → Imran
user:1:age   → 21
user:1:city  → Lahore
```

you can have:

```text
user:1
   │
   ├── name → Imran
   ├── age  → 21
   └── city → Lahore
```

That's a Redis Hash.

---

## 1. What is a Hash?

A Redis Hash is a collection of **field-value pairs** stored under one Redis key.

```text
Redis Key
    ↓
  user:1
    ↓
┌───────────────┐
│ name → Imran  │
│ age  → 21     │
│ city → Lahore │
└───────────────┘
```

The terminology is:

```text
user:1       → Hash key
name         → Field
Imran        → Value
age          → Field
21           → Value
```

### Mental model

> **Hash = an object/record containing fields.**

This makes Hashes extremely useful for things like:

```text
Users
Products
Profiles
Sessions
Configurations
Counters
```

---

# 2. Hash vs String

You might wonder:

> "Couldn't I just store the whole user as a String?"

You could.

For example:

```redis
SET user:1 "Imran,21,Lahore"
```

But now changing only the age becomes awkward.

With a Hash:

```redis
HSET user:1 name "Imran"
HSET user:1 age 21
HSET user:1 city "Lahore"
```

You can change only the age:

```redis
HSET user:1 age 22
```

So:

```text
STRING

user:1 → "Imran,21,Lahore"


HASH

user:1
 ├── name → Imran
 ├── age  → 21
 └── city → Lahore
```

---

# 3. `HSET`

The most important Hash command.

`HSET` adds or updates a field.

### Syntax

```redis
HSET key field value
```

Example:

```redis
HSET user:1 name "Imran"
HSET user:1 age 21
HSET user:1 city "Lahore"
```

Now:

```text
user:1
├── name → Imran
├── age  → 21
└── city → Lahore
```

You can also set multiple fields:

```redis
HSET user:1 name "Imran" age 21 city "Lahore"
```

---

# 4. `HGET`

Retrieve one field.

```redis
HGET user:1 name
```

Result:

```text
"Imran"
```

Or:

```redis
HGET user:1 age
```

Result:

```text
"21"
```

Mental model:

```text
HSET → Store/update one or more fields
HGET → Get one field
```

---

# 5. `HMGET`

Get multiple fields at once.

```redis
HMGET user:1 name age city
```

Result:

```text
1) "Imran"
2) "21"
3) "Lahore"
```

So:

```text
HGET
 ↓
One field

HMGET
 ↓
Multiple fields
```

---

# 6. `HGETALL`

Get **all fields and values**.

```redis
HGETALL user:1
```

Result:

```text
1) "name"
2) "Imran"
3) "age"
4) "21"
5) "city"
6) "Lahore"
```

Think:

```text
HGETALL
   ↓
Give me the entire Hash
```

This is one of the most commonly used Hash commands.

---

# 7. `HDEL`

Delete a field.

```redis
HDEL user:1 city
```

Now:

```text
user:1
├── name → Imran
└── age  → 21
```

Important:

`HDEL` removes a **field**, not necessarily the entire Redis key.

---

# 8. `HEXISTS`

Check whether a field exists.

```redis
HEXISTS user:1 age
```

Result:

```text
(integer) 1
```

Meaning:

```text
1 → exists
0 → doesn't exist
```

For example:

```redis
HEXISTS user:1 email
```

might return:

```text
(integer) 0
```

---

# 9. `HKEYS`

Get all field names.

```redis
HKEYS user:1
```

Result:

```text
1) "name"
2) "age"
3) "city"
```

So:

```text
HKEYS
  ↓
Give me only the fields.
```

---

# 10. `HVALS`

Get all values.

```redis
HVALS user:1
```

Result:

```text
1) "Imran"
2) "21"
3) "Lahore"
```

So:

```text
HKEYS
  ↓
Fields


HVALS
  ↓
Values
```

---

# 11. `HLEN`

Count how many fields exist in a Hash.

```redis
HLEN user:1
```

If we have:

```text
name
age
city
```

the result is:

```text
(integer) 3
```

Compare:

```text
LLEN → List length
SCARD → Set cardinality
ZCARD → Sorted Set cardinality
HLEN → Number of Hash fields
```

---

# 12. Updating a Field

`HSET` can update an existing field.

Suppose:

```redis
HSET user:1 age 21
```

Then:

```redis
HSET user:1 age 22
```

Now:

```redis
HGET user:1 age
```

returns:

```text
"22"
```

So:

```text
HSET
 ↓
If field doesn't exist → creates it
If field exists → updates it
```

---

# 13. `HSETNX`

`HSETNX` means:

> **Hash SET if Not eXists**

It only sets the field if it doesn't already exist.

```redis
HSETNX user:1 username "imran"
```

If `username` doesn't exist:

```text
username → imran
```

But if it already exists:

```text
username → imran
```

and:

```redis
HSETNX user:1 username "new_name"
```

won't overwrite it.

Mental model:

```text
HSET
 ↓
Create OR update


HSETNX
 ↓
Create ONLY if field doesn't exist
```

---

# 14. Numeric Operations — `HINCRBY`

Hashes can contain numbers, and Redis can increment them.

Suppose:

```redis
HSET user:1 login_count 10
```

Increase it:

```redis
HINCRBY user:1 login_count 1
```

Now:

```text
login_count → 11
```

Or:

```redis
HINCRBY user:1 login_count 5
```

Now:

```text
11 → 16
```

This is useful for:

```text
Login counts
View counts
Likes
XP
Scores
Counters
```

---

# 15. `HINCRBYFLOAT`

For floating-point numbers:

```redis
HSET product:1 price 99.5
```

Then:

```redis
HINCRBYFLOAT product:1 price 10.25
```

Result:

```text
109.75
```

So:

```text
HINCRBY
     ↓
Integer


HINCRBYFLOAT
     ↓
Floating-point number
```

---

# 16. `HSTRLEN`

Get the length of a field's string value.

```redis
HSET user:1 name "Imran"
```

Then:

```redis
HSTRLEN user:1 name
```

Result:

```text
(integer) 5
```

It's basically the Hash version of `STRLEN`.

```text
STRLEN
 ↓
String value


HSTRLEN
 ↓
String value inside a Hash field
```

---

# 17. Real Backend Example — User

This is where Hashes become really useful.

Create:

```redis
HSET user:1001 \
    name "Imran" \
    age 21 \
    city "Lahore" \
    role "student"
```

Now the structure is:

```text
user:1001
│
├── name → Imran
├── age → 21
├── city → Lahore
└── role → student
```

Get the whole user:

```redis
HGETALL user:1001
```

Get only the name:

```redis
HGET user:1001 name
```

Update city:

```redis
HSET user:1001 city "Karachi"
```

Delete role:

```redis
HDEL user:1001 role
```

---

# 18. Real Backend Example — Product

```redis
HSET product:5001 \
    name "Mechanical Keyboard" \
    price 7500 \
    stock 25 \
    category "keyboard"
```

Now:

```text
product:5001
│
├── name → Mechanical Keyboard
├── price → 7500
├── stock → 25
└── category → keyboard
```

When someone purchases one:

```redis
HINCRBY product:5001 stock -1
```

Now:

```text
stock:
25 → 24
```

🔥 This is one reason Redis is powerful for backend systems.

---

# 19. Hashes and Objects

Think of a Python object:

```python
user = {
    "name": "Imran",
    "age": 21,
    "city": "Lahore"
}
```

Redis Hash:

```redis
HSET user:1 name "Imran" age 21 city "Lahore"
```

Conceptually:

```text
Python Dictionary
        ↓
Redis Hash
```

This is why you'll frequently see patterns like:

```text
user:<id>
product:<id>
order:<id>
session:<id>
```

with fields stored inside the Hash.

---

# 20. Hash vs Set

Don't confuse them.

### Set

```text
skills
 ↓
{Python, Redis, Docker}
```

It's a collection of **unique values**.

### Hash

```text
user:1
 ↓
{
    name: Imran,
    age: 21,
    city: Lahore
}
```

It's a collection of **field → value pairs**.

```text
SET
 ↓
"value1"
"value2"
"value3"


HASH
 ↓
field → value
field → value
field → value
```

---

# 21. Important Command Family

You'll notice Redis commands follow patterns.

### Basic Hash operations

```text
HSET       → Set field
HGET       → Get field
HMGET      → Get multiple fields
HGETALL    → Get everything
HDEL       → Delete field
```

### Checking / inspecting

```text
HEXISTS    → Does field exist?
HKEYS      → Get field names
HVALS      → Get values
HLEN       → Number of fields
HSTRLEN    → Length of a field's value
```

### Conditional

```text
HSETNX     → Set only if field doesn't exist
```

### Numeric

```text
HINCRBY       → Increment integer
HINCRBYFLOAT  → Increment float
```

---

# 🧠 Hash Mental Map

```text
                    REDIS HASH
                        │
          ┌─────────────┼─────────────┐
          │             │             │
        WRITE          READ        DELETE
          │             │             │
        HSET           HGET          HDEL
        HSETNX         HMGET
                       HGETALL
          │
          │
       INSPECT
          │
    ┌─────┼──────┬────────┐
    │     │      │        │
 HEXISTS HKEYS HVALS    HLEN
                         │
                      # fields

          │
       NUMBERS
          │
     ┌────┴─────┐
     │          │
 HINCRBY   HINCRBYFLOAT
```

## 🔥 The one sentence to remember

> **A Redis Hash stores multiple field-value pairs under one Redis key, making it ideal for representing objects such as users, products, and sessions.**

And the commands I'd memorize first are:

```text
HSET      → Create/update field
HGET      → Get field
HMGET     → Get multiple fields
HGETALL   → Get entire Hash
HDEL      → Delete field
HEXISTS   → Check field
HKEYS     → Get fields
HVALS     → Get values
HLEN      → Count fields
HSETNX    → Set if doesn't exist
HINCRBY   → Increment integer
HINCRBYFLOAT → Increment float
```
