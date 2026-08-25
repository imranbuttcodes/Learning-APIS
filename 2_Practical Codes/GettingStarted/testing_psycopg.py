import psycopg2

try:
    connection = psycopg2.connect(
        host = 'localhost', 
        port = 5432,
        database = 'fastapi_db',
        user = 'postgres',
        password = 'postgres123'
    )
    print("Database connection successful")
    connection.close()  # Close the connection after testing
except Exception as e:
    print("Database connection failed")
    print(e)