Absolutely bro 🔥. **Sorted Sets (`ZSET`)** are one of Redis's most powerful data structures, especially for **leaderboards, rankings, priority systems, and time-based ordering**.

# 🟣 Redis Sorted Sets

## 1. What is a Sorted Set?

A Redis **Sorted Set** is like a normal Set, but every member has a **score**.

```text
Sorted Set

Member       Score
─────────    ─────
Imran         95
Ahmed         90
Ali           85
```

Redis automatically keeps the members **ordered by their scores**.

The two key properties are:

```text
Sorted Set
├── Members are UNIQUE
└── Members are ordered by SCORE
```

Compare:

```text
SET
{Imran, Ali, Ahmed}
     ↓
Unique, but unordered


SORTED SET
{Imran:95, Ali:85, Ahmed:90}
       ↓
Unique + ordered by score
```

---

# 2. Creating a Sorted Set — `ZADD`

The basic syntax is:

```redis
ZADD key score member
```

Example:

```redis
ZADD leaderboard 95 "Imran"
ZADD leaderboard 85 "Ali"
ZADD leaderboard 90 "Ahmed"
```

Now:

```redis
ZRANGE leaderboard 0 -1 WITHSCORES
```

You'll get:

```text
1) "Ali"
2) "85"
3) "Ahmed"
4) "90"
5) "Imran"
6) "95"
```

Notice something important:

**We inserted Imran first, but Redis returns Ali → Ahmed → Imran because the scores determine the ordering.**

---

# 3. The Mental Model

Think of a Sorted Set as:

```text
             leaderboard
                  │
       ┌──────────┼──────────┐
       │          │          │
     Ali        Ahmed      Imran
      85          90         95
       │           │          │
       └───────────┴──────────┘
              sorted by
                score
```

The **member** is the actual item.

The **score** determines its position.

---

# 4. `ZRANGE`

Get members ordered from **lowest score → highest score**.

```redis
ZRANGE leaderboard 0 -1
```

With scores:

```redis
ZRANGE leaderboard 0 -1 WITHSCORES
```

Example:

```text
Ali     85
Ahmed   90
Imran   95
```

### What does `0 -1` mean?

Exactly like `LRANGE`:

```text
0  → first
-1 → last
```

---

# 5. `ZREVRANGE`

Sometimes you want the highest score first.

Historically, you can use:

```redis
ZREVRANGE leaderboard 0 -1 WITHSCORES
```

Result:

```text
Imran   95
Ahmed   90
Ali     85
```

So:

```text
ZRANGE
↓
Low → High

ZREVRANGE
↓
High → Low
```

> In newer Redis versions, `ZRANGE` also supports reverse ordering with `REV`, but `ZREVRANGE` is still worth recognizing when reading existing Redis code.

---

# 6. `ZSCORE`

Want to find the score of one member?

```redis
ZSCORE leaderboard "Imran"
```

Result:

```text
"95"
```

Think:

```text
ZSCORE
   ↓
Give me this member's score.
```

---

# 7. `ZRANK`

`ZRANK` tells you a member's **position**, starting from `0`.

```redis
ZRANK leaderboard "Ali"
```

If:

```text
Ali     85
Ahmed   90
Imran   95
```

then:

```text
Ali   → 0
Ahmed → 1
Imran → 2
```

Remember:

> **Rank starts at 0.**

---

# 8. `ZREVRANK`

Want the ranking from highest score to lowest?

```redis
ZREVRANK leaderboard "Imran"
```

Given:

```text
Imran   95
Ahmed   90
Ali     85
```

you get:

```text
Imran → 0
Ahmed → 1
Ali   → 2
```

So:

```text
ZRANK
     ↓
Lowest → Highest

ZREVRANK
     ↓
Highest → Lowest
```

---

# 9. `ZCARD`

How many members are in the Sorted Set?

```redis
ZCARD leaderboard
```

If you have:

```text
Imran
Ahmed
Ali
```

you get:

```text
(integer) 3
```

Think:

```text
SCARD  → number of Set members
ZCARD  → number of Sorted Set members
```

---

# 10. Updating a Score

This is extremely useful.

Suppose Imran gets a new score:

```redis
ZADD leaderboard 100 "Imran"
```

Redis doesn't create another Imran.

It **updates Imran's score**:

```text
Before:

Imran → 95

After:

Imran → 100
```

Because members in a Sorted Set are unique.

And Redis automatically adjusts the ordering.

---

# 11. `ZINCRBY` ⭐

This is one you'll definitely want to remember.

Instead of setting a new score, increase the existing score.

```redis
ZINCRBY leaderboard 10 "Imran"
```

If Imran had:

```text
Imran → 95
```

then:

```text
95 + 10 = 105
```

Now:

```redis
ZSCORE leaderboard "Imran"
```

returns:

```text
"105"
```

This is excellent for:

```text
Game points
XP
Leaderboard scores
Reputation
Ranking systems
```

---

# 12. `ZREM`

Remove a member.

```redis
ZREM leaderboard "Ali"
```

Ali is removed from the Sorted Set.

```text
Before:

Ali     85
Ahmed   90
Imran   95

After:

Ahmed   90
Imran   95
```

---

# 13. Finding Members by Score

Here's where Sorted Sets become really useful.

Suppose:

```text
leaderboard

Ali      85
Ahmed    90
Imran    95
Usman    70
Hassan   60
```

You can ask Redis:

> Give me everyone with a score between 80 and 100.

Using:

```redis
ZRANGEBYSCORE leaderboard 80 100
```

Result:

```text
Ali
Ahmed
Imran
```

So:

```text
ZRANGEBYSCORE
       ↓
Find members whose scores
fall inside a range.
```

---

# 14. `ZCOUNT`

Want to know **how many** members have scores in a range?

```redis
ZCOUNT leaderboard 80 100
```

Result:

```text
(integer) 3
```

So:

```text
ZRANGEBYSCORE
↓
Give me the members.

ZCOUNT
↓
Give me the number of members.
```

---

# 15. Score Ranges Can Be Exclusive

You can also exclude a boundary using `(`.

For example:

```redis
ZRANGEBYSCORE leaderboard (80 100
```

means:

```text
score > 80
AND
score <= 100
```

While:

```redis
ZRANGEBYSCORE leaderboard 80 100
```

means:

```text
score >= 80
AND
score <= 100
```

This becomes useful when doing precise range queries.

---

# 16. Removing by Rank

You can remove members based on their rank.

```redis
ZREMRANGEBYRANK leaderboard 0 2
```

This removes the members whose ranks are:

```text
0
1
2
```

⚠️ Be careful: rank `0` means the **lowest score** when using normal ascending rank.

---

# 17. Removing by Score

You can also remove everyone whose score falls within a range.

```redis
ZREMRANGEBYSCORE leaderboard 0 50
```

Meaning:

> Remove members whose score is between 0 and 50.

This can be useful for cleaning old/expired ranking data or maintaining bounded datasets.

---

# 18. What Happens When Two Members Have the Same Score?

Important question.

Suppose:

```redis
ZADD leaderboard 100 "Imran"
ZADD leaderboard 100 "Ali"
```

Both have:

```text
Score = 100
```

Redis still keeps both because **members are unique**.

When scores are equal, Redis uses the members' values to determine their ordering.

So don't think:

```text
Same score → one gets deleted ❌
```

Instead:

```text
Imran → 100
Ali   → 100
```

Both remain.

---

# 19. Real-World Example: Game Leaderboard 🎮

Imagine you're building a game.

Players earn XP:

```redis
ZADD game:leaderboard 1500 "Imran"
ZADD game:leaderboard 1200 "Ali"
ZADD game:leaderboard 1800 "Ahmed"
ZADD game:leaderboard 900 "Hassan"
```

Get leaderboard:

```redis
ZREVRANGE game:leaderboard 0 -1 WITHSCORES
```

Result:

```text
Ahmed    1800
Imran    1500
Ali      1200
Hassan    900
```

Now Imran earns 500 XP:

```redis
ZINCRBY game:leaderboard 500 "Imran"
```

Now:

```text
Ahmed    1800
Imran    2000
Ali      1200
Hassan    900
```

Redis automatically moves Imran to the top.

🔥 **That's why Sorted Sets are perfect for leaderboards.**

---

# 20. Real-World Example: Priority System

Imagine jobs have priorities:

```text
job1 → priority 10
job2 → priority 50
job3 → priority 20
```

Store:

```redis
ZADD jobs 10 "job1"
ZADD jobs 50 "job2"
ZADD jobs 20 "job3"
```

Then you can retrieve them according to priority.

```text
job1 → 10
job3 → 20
job2 → 50
```

Depending on your design, you can interpret a higher or lower score as higher priority.

---

# 21. Real-World Example: Time-Based Data

Sorted Sets can also use **timestamps as scores**.

For example:

```text
notification → timestamp
```

```redis
ZADD notifications 1788250000 "notification1"
ZADD notifications 1788250100 "notification2"
```

Now Redis can naturally order them by time.

This pattern is useful for things like:

```text
Scheduled jobs
Delayed tasks
Time-based events
Feeds
Expiration systems
```

---

# 22. Set vs Sorted Set

This is extremely important.

| Feature          | Set                | Sorted Set           |
| ---------------- | ------------------ | -------------------- |
| Unique members   | ✅                  | ✅                    |
| Ordered          | ❌                  | ✅                    |
| Score            | ❌                  | ✅                    |
| `SADD`           | ✅                  | ❌                    |
| `ZADD`           | ❌                  | ✅                    |
| Membership check | `SISMEMBER`        | `ZSCORE` / `ZMSCORE` |
| Count            | `SCARD`            | `ZCARD`              |
| Common use       | Unique collections | Rankings/order       |

Mental model:

```text
SET

{Python, Redis, Docker}
       ↓
"Is it there?"


SORTED SET

{Imran:95, Ali:85, Ahmed:90}
       ↓
"Who has what score/rank?"
```

---

# 🧠 Sorted Set Commands to Remember

```text
ZADD
   ↓
Add member + score

ZRANGE
   ↓
Get members low → high

ZREVRANGE
   ↓
Get members high → low

ZSCORE
   ↓
Get member's score

ZRANK
   ↓
Get rank low → high

ZREVRANK
   ↓
Get rank high → low

ZCARD
   ↓
Count members

ZINCRBY
   ↓
Increase score

ZREM
   ↓
Remove member

ZRANGEBYSCORE
   ↓
Get members by score range

ZCOUNT
   ↓
Count members in score range

ZREMRANGEBYRANK
   ↓
Remove by rank

ZREMRANGEBYSCORE
   ↓
Remove by score
```

---

# 🧪 Let's Practice

Run this:

```redis
ZADD leaderboard 95 "Imran"
ZADD leaderboard 85 "Ali"
ZADD leaderboard 90 "Ahmed"
ZADD leaderboard 70 "Hassan"
ZADD leaderboard 80 "Usman"
```

### See everyone:

```redis
ZRANGE leaderboard 0 -1 WITHSCORES
```

### Highest first:

```redis
ZREVRANGE leaderboard 0 -1 WITHSCORES
```

### Imran's score:

```redis
ZSCORE leaderboard "Imran"
```

### Imran's rank:

```redis
ZREVRANK leaderboard "Imran"
```

### Increase Imran's score:

```redis
ZINCRBY leaderboard 10 "Imran"
```

### Find people scoring 80–100:

```redis
ZRANGEBYSCORE leaderboard 80 100
```

### Count them:

```redis
ZCOUNT leaderboard 80 100
```

### Remove Hassan:

```redis
ZREM leaderboard "Hassan"
```

---

## 🔥 The Big Picture

You've now learned the three major Redis collection structures:

```text
             REDIS COLLECTIONS
                    │
       ┌────────────┼────────────┐
       │            │            │
      LIST         SET       SORTED SET
       │            │            │
    Ordered       Unique    Unique + Score
    Duplicates    Values        │
       │            │            │
    LPUSH         SADD         ZADD
    RPUSH         SREM         ZRANGE
    LPOP          SINTER       ZRANK
    LRANGE        SUNION       ZSCORE
                                ZINCRBY
                                ZREVRANGE
                                ZCOUNT
```

**The one sentence to remember:**

> 🟢 **Set = unique values.**
> 🟣 **Sorted Set = unique values + a score that determines their order.**

Next, I'd move to **Redis Hashes** because they are the natural next step for backend development—especially when you want to represent something like a `user`, `product`, or `session` as multiple fields.
