Bro 🔥 here's the **SQLAlchemy ORM CRUD mind map** covering the methods, what they do, and why/when we use them.

![Image](https://images.openai.com/static-rsc-4/W71uVfPHYDTIqdapOKDp9leNgvoLXXwGUHv0Ulc8Nq2x-Y1E1JTUTEaDncw4dOwVIeYJfH8_FLq2ewq6L4C9JkwBX3WdyZi2GJ6iHyKWVXt5GmTdrFk0a3lUrM0oR81K972DVh9uUohhwPPlAAavdgvk0xgab7pJKMkgw26QkyCIQ2frVGjYBc_GrX0h0NIQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/YHsHmSlcTFmmK1gAg3t4xMvVHDWI7EIFWm44brxnXu45drSqOD8COPQ03Kh-pE6Kph9RJK0RXxkqodulUQCoz7Cg-66yPpqlPlrkBz_bxBfenl_vnjMO26voRZeon9MdZ-HEvtoup_jfanKJ_UYpHuZq1GLULpOjoxK4OtfuZYkEgji1U72L5eCv2HfTji7j?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/gcgcxzxrXCkpXLLp8TioUjHokqHTno3q31a2hhdghOh_KW7QxfJenl1SQ811-v8R5F01RJsCo8r4HehnSZZB6H2EPQMQ29iGNsk9nR4XCrmy-aFoKumQo4yfgWaHvbefGTSfxeMTfqWltIgpinZ9vcQujt2vvSzMROrpKmyIVLLMjY26pv6VSgIPRNUJxKGt?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/n03bHRwOM6n4iO-goaB4XHAWwUzncR8Iev4orfXb1Bi3ubnqfMc7c0YE6qcBzag6dbtVpDCZoaPM2ztfHGxrAb4st1odlmyf1AHG6bpT3vBQDjHsyGX2LINcUU4bFyjnuEzwtukrbok67NDxn4MxwpItPos7fOfc4_MzYLV4_zG-3UU1SgIPGcS1LR13G651?purpose=fullsize)

# 🧠 SQLAlchemy ORM — Complete Mind Map

```text
                         ┌──────────────────────────┐
                         │   SQLAlchemy ORM CRUD     │
                         └────────────┬─────────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
              ▼                       ▼                       ▼
        DATABASE SETUP             SESSION                  CRUD
              │                       │                       │
              │                       │          ┌────────────┼────────────┐
              │                       │          │            │            │
              ▼                       ▼          ▼            ▼            ▼
          Engine                 SessionLocal  CREATE        READ        UPDATE
              │                       │          │            │            │
              ▼                       ▼          ▼            ▼            ▼
       create_engine()          sessionmaker() db.add()    select()    modify object
              │                       │          │            │            │
              ▼                       ▼          ▼            ▼            ▼
          Engine                 Factory      commit()    execute()    commit()
              │                       │
              │                       ▼
              │                  Session (db)
              │                       │
              │                       ├── add()
              │                       ├── execute()
              │                       ├── delete()
              │                       ├── commit()
              │                       ├── rollback()
              │                       ├── refresh()
              │                       ├── flush()
              │                       └── close()
              │
              ▼
          PostgreSQL
```

---

# 🟢 1. ENGINE

```python
engine = create_engine(DATABASE_URL)
```

### What is it?

The **Engine** is SQLAlchemy's database communication hub.

```text
SQLAlchemy
    ↓
  Engine
    ↓
Psycopg2
    ↓
PostgreSQL
```

### Important:

`engine` ≠ Session.

The Engine handles the connection/communication infrastructure.

---

# 🟡 2. `Session`

```python
from sqlalchemy.orm import Session
```

### What is it?

`Session` is SQLAlchemy's ORM **workspace**.

You use it to perform database operations.

```python
db.add(...)
db.execute(...)
db.delete(...)
db.commit()
```

Think:

```text
Session
  ↓
Database workspace
```

---

# 🟠 3. `sessionmaker`

```python
from sqlalchemy.orm import sessionmaker
```

`sessionmaker` is a **factory** that creates Sessions.

```python
SessionLocal = sessionmaker(bind=engine)
```

Think:

```text
sessionmaker
      ↓
   Factory
      ↓
Sessions
```

---

# 🔵 4. `SessionLocal`

```python
SessionLocal = sessionmaker(bind=engine)
```

`SessionLocal` is **our variable name**, not some special SQLAlchemy object.

It represents our configured Session factory.

Then:

```python
db = SessionLocal()
```

creates an actual Session.

```text
SessionLocal
     │
     │ ()
     ▼
   db
     │
     ▼
Session object
```

---

# 🟣 5. `get_db()`

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Purpose:

```text
Create Session
      ↓
Give Session to FastAPI
      ↓
Route uses Session
      ↓
Close Session
```

---

# 🔴 6. `Depends(get_db)`

```python
db: Session = Depends(get_db)
```

This is FastAPI.

It means:

> "FastAPI, give this route a database Session using `get_db`."

```text
Request
   ↓
FastAPI
   ↓
Depends(get_db)
   ↓
SessionLocal()
   ↓
db
   ↓
Route
```

---

# 🟢 CREATE

## `db.add()`

```python
post = Post(
    title="Hello",
    content="World"
)

db.add(post)
```

### Meaning:

> Add this ORM object to the Session's work.

It doesn't mean "permanently save it" yet.

```text
Post object
     ↓
db.add()
     ↓
Session tracks object
```

---

## `db.commit()`

```python
db.commit()
```

### Meaning:

> Commit the current transaction.

For CREATE:

```text
db.add()
   ↓
db.commit()
   ↓
INSERT
```

---

## `db.refresh()`

```python
db.refresh(post)
```

### Meaning:

> Reload the object's current values from the database.

Useful for database-generated values:

```text
Before:
post.id = None

commit()

PostgreSQL:
id = 5

refresh()

post.id = 5
```

---

# 🔵 READ

Modern SQLAlchemy 2.x:

```python
from sqlalchemy import select
```

## `select()`

```python
statement = select(Post)
```

Builds a SELECT statement.

Conceptually:

```sql
SELECT *
FROM posts;
```

---

## `db.execute()`

```python
result = db.execute(statement)
```

Executes the SQLAlchemy statement using the Session.

```text
select(Post)
     ↓
statement
     ↓
db.execute()
     ↓
PostgreSQL
```

---

## `scalars()`

```python
result.scalars()
```

Extracts the ORM objects from the result.

```text
Result
  ↓
scalars()
  ↓
Post objects
```

---

## `all()`

```python
posts = result.scalars().all()
```

Gets all results as a list.

```text
Database
   ↓
Result
   ↓
scalars()
   ↓
all()
   ↓
[Post, Post, Post]
```

---

# 🟠 READ ONE

```python
statement = select(Post).where(Post.id == post_id)

result = db.execute(statement)

post = result.scalar_one_or_none()
```

## `where()`

```python
.where(Post.id == post_id)
```

Adds a filtering condition.

Conceptually:

```sql
WHERE id = 5
```

---

## `scalar_one_or_none()`

Returns:

```text
One result → Post object

No result → None

Multiple results → Error
```

Perfect when searching by primary key.

---

# 🟡 UPDATE

Here's the ORM magic.

First retrieve:

```python
post = db.execute(
    select(Post).where(Post.id == post_id)
).scalar_one_or_none()
```

Then modify the Python object:

```python
post.title = "New title"
post.content = "New content"
```

Then:

```python
db.commit()
```

SQLAlchemy detects the changes.

```text
Database
   ↓
Post object
   ↓
Modify attributes
   ↓
db.commit()
   ↓
SQLAlchemy detects changes
   ↓
UPDATE
```

You don't manually write:

```sql
UPDATE posts ...
```

---

# 🔴 DELETE

First retrieve the object:

```python
post = db.execute(
    select(Post).where(Post.id == post_id)
).scalar_one_or_none()
```

Then:

```python
db.delete(post)
```

This marks it for deletion.

Then:

```python
db.commit()
```

makes it permanent.

```text
Post object
     ↓
db.delete()
     ↓
Session tracks deletion
     ↓
db.commit()
     ↓
DELETE
```

---

# ⚫ TRANSACTION METHODS

These are also important.

## `commit()`

```python
db.commit()
```

Save/commit the transaction.

---

## `rollback()`

```python
db.rollback()
```

Undo uncommitted changes in the current transaction.

Typical pattern:

```python
try:
    db.add(post)
    db.commit()
except:
    db.rollback()
    raise
```

Think:

```text
Something went wrong
       ↓
rollback()
       ↓
Undo transaction
```

---

## `flush()`

```python
db.flush()
```

Send pending changes to the database **without committing the transaction**.

```text
add()
 ↓
flush()
 ↓
Database receives changes
 ↓
Transaction still open
 ↓
commit()
```

You'll use this less often as a beginner.

---

# ⚪ `close()`

```python
db.close()
```

Closes the Session.

In FastAPI:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

So:

```text
Request starts
     ↓
Session created
     ↓
Route uses db
     ↓
Request finishes
     ↓
db.close()
```

---

# 🧠 FINAL CRUD MAP

```text
                         SQLAlchemy Session (db)
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
           CREATE                READ               MODIFY
              │                   │                   │
              │                   │             ┌─────┴─────┐
              │                   │             │           │
              ▼                   ▼             ▼           ▼
          Post(...)           select()       UPDATE       DELETE
              │                   │             │           │
              ▼                   ▼             │           │
          db.add()           db.execute()      │       db.delete()
              │                   │             │           │
              │                   ▼             │           │
              │               scalars()        │           │
              │                   │             │           │
              │                   ▼             │           │
              │              all() / one()      │           │
              │                   │             │           │
              └───────────────────┼─────────────┴───────────┘
                                  │
                                  ▼
                              db.commit()
                                  │
                                  ▼
                              PostgreSQL
```

---

# 🔥 The 10 methods/functions I want you to know first

Don't try to memorize everything yet. These are your **core SQLAlchemy ORM tools**:

```text
┌─────────────────────────────┬─────────────────────────────┐
│ Tool                        │ Purpose                     │
├─────────────────────────────┼─────────────────────────────┤
│ create_engine()             │ Create Engine               │
│ sessionmaker()              │ Create Session factory      │
│ SessionLocal()              │ Create actual Session       │
│ db.add()                    │ Add ORM object              │
│ db.execute()                │ Execute statement           │
│ select()                    │ Build SELECT statement      │
│ db.commit()                 │ Commit transaction           │
│ db.refresh()                │ Refresh ORM object          │
│ db.delete()                 │ Mark object for deletion    │
│ db.close()                  │ Close Session               │
└─────────────────────────────┴─────────────────────────────┘
```

And the **mental model** to keep in your head:

```text
              ENGINE
                │
                ▼
         SESSION FACTORY
          sessionmaker()
                │
                ▼
             SESSION
                │
                │ db
       ┌────────┼────────┐
       ▼        ▼        ▼
     CREATE    READ    MODIFY
       │        │        │
    add()    execute()   │
       │      select()   │
       │        │        ├── change object
       │        │        └── delete()
       │        │
       └────────┼────────┘
                ▼
             commit()
                │
                ▼
           PostgreSQL
```

That's the **core SQLAlchemy ORM map** you've built so far. 🔥
