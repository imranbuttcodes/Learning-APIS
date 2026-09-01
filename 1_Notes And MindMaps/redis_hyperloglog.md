# Redis HyperLogLog — Notes

## 1. What is HyperLogLog?

**HyperLogLog (HLL)** is a **probabilistic data structure** used to estimate the number of **unique elements** in a large dataset.

The important word is:

> **Estimate**

It does **not store all the actual elements** like a Set. Instead, it maintains a compact statistical representation.

### Main purpose

```text
HyperLogLog
     ↓
Estimate cardinality
     ↓
"How many unique items are there?"
```

---

# 2. What is Cardinality?

**Cardinality = number of unique elements.**

Example:

```text
{A, B, A, C, B, D}
```

Unique elements:

```text
{A, B, C, D}
```

Therefore:

```text
Cardinality = 4
```

HyperLogLog is specifically designed to estimate this value.

---

# 3. Why Use HyperLogLog?

Suppose a website has millions of visitors.

You want to know:

> "How many unique users visited my website?"

Using a Redis Set:

```text
SET
 │
 ├── user1
 ├── user2
 ├── user3
 ├── ...
 └── user100000000
```

The Set stores the actual members, which can consume significant memory.

HyperLogLog instead stores a **very small probabilistic representation**.

```text
SET
 ↓
Exact unique count
 ↓
More memory


HYPERLOGLOG
 ↓
Approximate unique count
 ↓
Very little memory
```

Redis documents HLL with a standard error of approximately **0.81%**.

---

# 4. Set vs HyperLogLog

| Feature               | Redis Set           | HyperLogLog                    |
| --------------------- | ------------------- | ------------------------------ |
| Stores actual members | ✅                   | ❌                              |
| Unique values         | ✅                   | Conceptually tracks uniqueness |
| Exact count           | ✅                   | ❌                              |
| Approximate count     | Not necessary       | ✅                              |
| Memory usage          | Higher              | Very low                       |
| Retrieve members      | ✅                   | ❌                              |
| Main command          | `SCARD`             | `PFCOUNT`                      |
| Best for              | Actual unique items | Large-scale unique counting    |

### Remember:

> **Set = "Which users?"**

> **HyperLogLog = "Approximately how many unique users?"**

---

# 5. The Three Main HLL Commands

Redis HyperLogLog mainly uses:

```text
PFADD
   ↓
Add elements

PFCOUNT
   ↓
Estimate unique elements

PFMERGE
   ↓
Merge multiple HLLs
```

---

# 6. PFADD

Adds one or more elements to a HyperLogLog.

### Syntax

```redis
PFADD key element [element ...]
```

### Example

```redis
PFADD visitors "Imran"
PFADD visitors "Ali"
PFADD visitors "Ahmed"
```

Or multiple at once:

```redis
PFADD visitors "Imran" "Ali" "Ahmed"
```

Here:

```text
visitors
   ↓
HyperLogLog
```

---

# 7. Duplicate Values

Adding the same value repeatedly doesn't increase the estimated unique count in the way a normal collection of duplicates would.

```redis
PFADD visitors "Imran"
PFADD visitors "Imran"
PFADD visitors "Imran"
```

Conceptually:

```text
Imran
Imran
Imran
  ↓
1 unique element
```

Then:

```redis
PFCOUNT visitors
```

estimates the cardinality.

---

# 8. PFCOUNT

Returns the estimated number of unique elements.

### Syntax

```redis
PFCOUNT key
```

### Example

```redis
PFCOUNT visitors
```

If the HLL represents approximately 1 million unique visitors:

```text
PFCOUNT
   ↓
≈ 1,000,000
```

The result is an **estimate**, not a guaranteed exact count.

---

# 9. PFMERGE

Combines multiple HyperLogLogs into one.

### Syntax

```redis
PFMERGE destination source1 source2 ...
```

### Example

```redis
PFMERGE all_visitors visitors:day1 visitors:day2
```

Now:

```redis
PFCOUNT all_visitors
```

estimates the number of unique visitors across both HLLs.

---

# 10. Why PFMERGE Is Useful

Suppose:

```text
Day 1:
Imran
Ali
Ahmed

Day 2:
Imran
Usman
Ahmed
```

Simply adding daily counts would give:

```text
3 + 3 = 6 ❌
```

because Imran and Ahmed appeared on both days.

After merging the HLLs:

```text
Day 1 HLL ──┐
            ├──→ Merged HLL
Day 2 HLL ──┘
                 ↓
          Unique visitors
```

The merged HLL estimates:

```text
Imran
Ali
Ahmed
Usman

≈ 4 unique visitors
```

---

# 11. Real-World Use Cases

## Website Analytics

```redis
PFADD visitors:2026-09-01 user123
PFADD visitors:2026-09-01 user456
```

Then:

```redis
PFCOUNT visitors:2026-09-01
```

→ Approximate unique visitors for the day.

---

## Unique Visitors Per Day

```text
visitors:2026-09-01
visitors:2026-09-02
visitors:2026-09-03
```

Each key can represent a separate HLL.

---

## Unique Visitors Per Month

Daily HLLs can be merged:

```redis
PFMERGE visitors:september \
    visitors:09-01 \
    visitors:09-02 \
    visitors:09-03
```

Then:

```redis
PFCOUNT visitors:september
```

→ Estimated unique visitors for the period.

---

## Analytics

HLL is useful for questions such as:

```text
How many unique users visited?

How many unique IP addresses appeared?

How many unique products were viewed?

How many unique search terms were used?

How many unique devices connected?
```

---

# 12. Important Limitation

HyperLogLog does **not** let you retrieve the actual members.

You cannot use it like:

```redis
SMEMBERS visitors
```

because HLL does not maintain an accessible list of users.

It answers:

```text
"How many unique elements?"
```

not:

```text
"Which elements?"
```

---

# 13. When Should You Use HLL?

### Use a Set when:

```text
I need the actual elements.
```

Example:

```text
Show me all users who visited.
```

Use:

```redis
SADD
SMEMBERS
SCARD
```

---

### Use HyperLogLog when:

```text
I only need an approximate unique count.
```

Example:

```text
How many unique users visited today?
```

Use:

```redis
PFADD
PFCOUNT
PFMERGE
```

---

# 14. Advantages

```text
✅ Extremely memory efficient
✅ Excellent for huge datasets
✅ Very fast
✅ Supports merging
✅ Great for analytics
✅ Useful for counting unique items
```

---

# 15. Disadvantages

```text
❌ Count is approximate
❌ Cannot retrieve actual members
❌ Cannot determine which specific users were seen
❌ Not suitable when exact results are required
```

---

# 16. Mental Model

```text
                 HYPERLOGLOG
                      │
                      ▼
             "How many unique?"
                      │
          ┌───────────┼───────────┐
          │           │           │
        PFADD       PFCOUNT     PFMERGE
          │           │           │
          ▼           ▼           ▼
        Add        Estimate      Merge
       values       count        HLLs
```

---

# 17. Set vs HLL Mental Model

```text
                 UNIQUE DATA
                      │
             ┌────────┴────────┐
             │                 │
            SET               HLL
             │                 │
       Stores members     Statistical
             │             representation
             │                 │
        Exact count       Approximate count
             │                 │
          SCARD            PFCOUNT
             │                 │
       More memory         Tiny memory
```

---

# 18. Command Cheat Sheet

| Command               | Meaning               |
| --------------------- | --------------------- |
| `PFADD key value`     | Add elements to HLL   |
| `PFCOUNT key`         | Estimate unique count |
| `PFMERGE dest src...` | Merge HLLs            |

### Example

```redis
PFADD visitors "Imran" "Ali" "Ahmed"

PFCOUNT visitors
```

Merge:

```redis
PFMERGE all_visitors morning evening
```

Count merged HLL:

```redis
PFCOUNT all_visitors
```

---

# 19. One-Line Revision

> **HyperLogLog is a memory-efficient probabilistic data structure used to estimate the number of unique elements in very large datasets.**

### Remember these 3 commands:

```text
PFADD    → Add
PFCOUNT  → Count
PFMERGE  → Merge
```

### And remember the trade-off:

```text
       MEMORY              ACCURACY

          ↓                   ↓
       VERY LOW          APPROXIMATE
          │                   │
          └────── HLL ────────┘
```
