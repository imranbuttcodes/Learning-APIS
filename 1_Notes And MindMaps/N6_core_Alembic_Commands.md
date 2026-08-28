*Core command set for managing your Alembic database migrations.*

| Command | Purpose |
| --- | --- |
| `alembic init alembic` | Initializes the migration environment, creating the `alembic/` folder and the `alembic.ini` config file in your project root. |
| `alembic revision --autogenerate -m "message"` | Scans your `models.py`, compares it to the live PostgreSQL database, and writes a new Python script detailing the exact changes needed. |
| `alembic upgrade head` | Executes all pending blueprint scripts against your database, updating the live tables to match your latest code. |
| `alembic downgrade -1` | Reverts the database schema exactly one step backward. You can also specify a specific revision hash (e.g., `alembic downgrade a1b2c3d4`) to roll back further. |
| `alembic history` | Prints a chronological timeline of all your migration scripts in the terminal, showing the unique hash for each version. |
| `alembic current` | Displays the exact migration version your live PostgreSQL database is currently running. |