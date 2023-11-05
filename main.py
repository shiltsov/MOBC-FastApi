import os, json, psycopg2
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import HTTPException
from dotenv import load_dotenv
from enum import Enum
from pydantic import BaseModel, constr
from typing import Optional, List

load_dotenv()

pg_host = os.getenv('PG_HOST')
pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_db = os.getenv('PG_DB')

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class DogKind(BaseModel):
    kind: DogType

class Dog(BaseModel):
    name: constr(min_length=1) # добавил констрейнт - нулевое имя - плохо
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


@app.get("/", response_class=JSONResponse, summary='Root')
def root():
    """
    Информация о том куда он попал 
    """
    return {"message": "Hello, this is vet clinic!"}

@app.post("/post",  response_class=JSONResponse, summary='Post Ts')
def post_ts(ts: Timestamp) -> Timestamp:
    """
    записываем данные в таблицу timestamps тупо и без проверок на констрейнты
    и возвращаем ему сам этот таймстемп
    
    никаких проверок на уникальность НЕ делаем. Что кидают - то и пишем
    """
    
    conn = psycopg2.connect(
        dbname=pg_db,
        user=pg_user,
        password=pg_password,
        host=pg_host,
    )

    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO timestamps(id, timestamp) VALUES ({ts.id}, {ts.timestamp})')
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return ts


@app.get("/dog",  response_class=JSONResponse, summary='Get Dog List')
def get_dog_list(kind: Optional[str] = None) -> List[Dog]:
    """
    Возвращает список собак данной породы если порода указана
    или весь список собак если не указана
    
    Args:
        kind str: порода собаки

    Raises:
        HTTPException: ValueError если данная порода отсутствует в списке пород

    Returns:
        list[Dog]: список собак
    """
    
    sql = "SELECT * FROM dogs"
    if kind:
        sql += f" WHERE kind = '{kind}'"
        
    print(sql)

    conn = psycopg2.connect(
        dbname=pg_db,
        user=pg_user,
        password=pg_password,
        host=pg_host,
    )

    cursor = conn.cursor()
    cursor.execute(sql)
    records = cursor.fetchall() 
    cursor.close()
    conn.close()

    result = []
    for pk, name, kind in records:
        result.append({"pk":pk, "name": name, "kind": kind})

    return result


@app.post("/dog", response_class=JSONResponse, response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog) -> Dog:
    """
    добавление новой собаки. Выкидываем исключение если предлагает
    собаку с pk который уже есть. По хорошему у него вообще не должно быть 
    возможности задавать pk - мы собаке его сами выдаем. Но раз передается Dog 
    целиком то пусть так и будет
    
    Args:
        dog (Dog): данные по новой собаке

    Returns:
        Dog: если ок - возвращаем то что было на входе
    """
    
    conn = psycopg2.connect(
        dbname=pg_db,
        user=pg_user,
        password=pg_password,
        host=pg_host,
    )

    cursor = conn.cursor()
    
    # проверка что собаки с таким pk нет
    sql = f"SELECT * FROM dogs WHERE pk = {dog.pk}"
    cursor.execute(sql)    
    if cursor.rowcount > 0:
        conn.close()
        raise HTTPException(status_code=409, detail=f"Value pk={dog.pk} already in use")
    
    sql = f"INSERT INTO dogs (pk, name, kind) VALUES ('{dog.pk}','{dog.name}','{dog.kind}')"
    cursor.execute(sql)
    conn.commit()
    conn.close()
            
    return dog


@app.get("/dog/{pk}", response_class=JSONResponse, response_model=Dog, summary='Get Dog By Pk')
def get_dog(pk: int) -> Dog:
    """
    Получить информацию о собаке по значению pk
    Args:
        pk (int): номер собаки

    Returns:
        Dog: объект 'Собака'
    """
    
    conn = psycopg2.connect(
        dbname=pg_db,
        user=pg_user,
        password=pg_password,
        host=pg_host,
    )

    cursor = conn.cursor()
    
    sql = f"SELECT pk, name, kind FROM dogs WHERE pk = {pk} LIMIT 1"
    cursor.execute(sql)    
    if cursor.rowcount == 0:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"message": f"Dog with pk={pk} wasn't found"},
        )        
    pk, name, kind = cursor.fetchone()
    conn.close()     
    return {"pk": pk, "name": name, "kind":kind }    
    
    
@app.patch("/dog/{pk}", response_class=JSONResponse, response_model=Dog, summary='Get Dog By Pk')
def patch_dog(pk: int, dog: Dog) -> Dog:
    
    # проверим что pk собаки равен pk из url (тест на подозрительную активность)
    # (!!!) по идее правильнее бы было делать патч просто на /dog без параметра в url
    # потому что мы уже требуем полные данные по собаке в запросе
    if pk != dog.pk:
        raise HTTPException(status_code=409, detail=f"Value pk={dog.pk} diffes from pk={pk} from url")
    
    # проверим что такая есть
    conn = psycopg2.connect(
        dbname=pg_db,
        user=pg_user,
        password=pg_password,
        host=pg_host,
    )

    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM dogs WHERE pk={pk}')
    if cursor.rowcount == 0:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"message": f"Dog with pk={pk} wasn't found"},
        )  
    
    sql = f"UPDATE dogs SET name = '{dog.name}', kind = '{dog.kind}'  where pk = {dog.pk}"
    cursor.execute(sql)
    conn.commit()
    conn.close()
            
    return dog

