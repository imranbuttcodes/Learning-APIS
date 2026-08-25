from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

#postgres URL = postgres://<username>:<password>@<ip-address/hostname>/<database_name>   


load_dotenv()  # Load environment variables from .env file

postgres_user = os.getenv('DB_USER')
postgres_password = os.getenv('DB_PASSWORD')
postgres_host = os.getenv('DB_HOST')
postgres_port = os.getenv('DB_PORT')
postgres_db = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # this is responsible for making the connection to the database

#print(engine)  # Print the engine object to verify the connection

with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM posts"))  # Execute a simple query to test the connection
    print(result.fetchall())  # Print the results of the query
    # print(result)
    # print()
    # print(result.scalar())  # Print the scalar result of the query and the scalar method returns the first column of the first row in the result set. If the result set is empty, it returns None.
