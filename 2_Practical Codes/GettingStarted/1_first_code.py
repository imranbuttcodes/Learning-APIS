from fastapi import FastAPI, Request
from fastapi.params import Body
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "This is Imran Butt Learning FastAPI"}

@app.get("/")
def about():
    return {"message": "This is the About endpoint"}

@app.post("/users")
async def create_user(request: Request):
    print("Creating a user...")
    print("Headers: ",request.headers)

    data = await request.json()
    print("Data: ",data)
    # print(payload.get("title"))
    # print(payload.get("content"))
    # return {"new_user": f"User with title '{payload.get('title')}' and content '{payload.get('content')}' created successfully."}
    return {"new_user": f"User created successfully."}

# @app.post("/users")
# def create_user(payload: dict = Body(...)):
#     print("Creating a user...")
#     print(payload)
#     print(payload.get("title"))
#     print(payload.get("content"))
#     return {"new_user": f"User with title '{payload.get('title')}' and content '{payload.get('content')}' created successfully."}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q} 

