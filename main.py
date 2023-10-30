from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello, AI Student!"}

@app.get("/add")
def add(x: int, y: int) -> int:
    return x + y

@app.get("/double/{number}")
def double(number: int) -> int:
    content = "<h1>" + str(number * 2) + "</h1>"
    return HTMLResponse(content=content)