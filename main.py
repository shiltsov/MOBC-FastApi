import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import psycopg2

load_dotenv()

pg_host = os.getenv('PG_HOST')
pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_db = os.getenv('PG_DB')

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


@app.get("/config",response_class=HTMLResponse)
def get_config():
    return config['postgres']['host']
    

@app.get("/list", response_class=HTMLResponse)
def list_dogs():
    conn = psycopg2.connect(
        dbname=pg_db,
        user=pg_user,
        password=pg_password,
        host=pg_host,
    )

    cursor = conn.cursor()
    cursor.execute('SELECT * FROM dogs')
    records = cursor.fetchall()

    context = "<table>"
    for row in records:
        context += f"<tr><td>{str(row[0])}</td><td>{str(row[1])}</td><td>{str(row[1])}</td></tr>"
    context += "</table>"  
    
    cursor.close()
    conn.close()
              
    return context

    
    
    