from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database import DB_Session
from tfidf_search import TFIDF_SEARCH
from embed_search import EMBED_SEARCH
import os
import json
import time
from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

# Создаем объекты для моделей и БД
tf_search = TFIDF_SEARCH()
embed = EMBED_SEARCH()
db_session = DB_Session()

# Cоздаем объект класса фастапи
app = FastAPI()

# объявляем статические файлы
static_dir = "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# задаем модель для поиска
class SearchRequest(BaseModel):
    query: str
    model: str = "tfidf"  # Дефолтно 'tfidf'
    top_n: int = 3        # Дефолтно 3 шутки

def perform_search(model_type: str, query: str, top_n: int):
    """
    Основная функция поиска для АПИ, отсюда ищем либо с тфдиф, либо бертом на фронте (нет близости)
    """
    if model_type == "tfidf":
        return tf_search.search_jokes(query, top_n)
    elif model_type == "embed":
        return embed.search_jokes(query, top_n)
    else:
        raise ValueError("Такой модели нет. Выберите 'tfidf' или 'embed'.")

def perform_cli_search(model_type: str, query: str, top_n: int):
    """
    Функция поиска для cli, отсюда ищем либо с тфдиф, либо бертом, есть близость
    """
    if model_type == "tfidf":
        return tf_search.cli_search_jokes(query, top_n)
    elif model_type == "embed":
        return embed.cli_search_jokes(query, top_n)
    else:
        raise ValueError("Такой модели нет. Выберите 'tfidf' или 'embed'.")
    
# Поисковый эндпоинт
@app.post("/search")
async def search(request: SearchRequest):
    try:
        start_time = time.time()
        results = perform_search(request.model, request.query, request.top_n)
        end_time = time.time()
        search_time = round(end_time - start_time, 2)
        return {"query": request.query, 
                "model": request.model, 
                "results": results, 
                "time_taken": search_time}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/cli_search/{mt}/{q}/{n}")
async def search(mt: str, q: str, n: int):
    try:
        start_time = time.time()
        results = perform_cli_search(model_type=mt, query=q, top_n=n)
        end_time = time.time()
        search_time = round(end_time - start_time, 2)
        return {"results": results, 
                "time_taken": search_time}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Обновим фронтэнд
@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/api/corpus-info")
async def get_corpus_info():
    with open('/Users/andrejpihtin/учеба/информационный_поиск/ht_1/dump/cleaned_jokes.json', 'r') as f:
        jokess = f.read()
    jokes = json.loads(jokess)
    tok_counter = 0
    for el in jokes:
        tok_counter += len(el.split())
    return {
        "Кол-во записей": f"{len(jokes)}",
        "Кол-во токенов": f"{tok_counter}",
        "corpus_name": "архив несмешного башорга"
    }


@app.get("/add_user/{login}/{password}")
async def add_user(login: str, password: str):
    try:
        message = db_session.add_user(login, password)
        if "Error" in message:
            raise HTTPException(status_code=400, detail=message)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/del_user/{login}")
async def add_user(login: str):
    try:
        message = db_session.add_user(login)
        if "Error" in message:
            raise HTTPException(status_code=400, detail=message)
        return {"message": message}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/lookup/{table}")
async def lookup_table(table: str):
    try:
        result = db_session.table_lookup(table)
        if isinstance(result, str) and result.startswith("Error"):
            raise HTTPException(status_code=400, detail=result)
        return {"table": table, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/cli_search&save/{mt}/{q}/{n}/{login}/{password}")
async def lookup_table(table: str):
    try:
        result = db_session.table_lookup(table)
        if isinstance(result, str) and result.startswith("Error"):
            raise HTTPException(status_code=400, detail=result)
        return {"table": table, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def get_user(self, login: str, password: str):
    """Fetch user by login and password."""
    result = self.session.execute(
        text("SELECT id FROM users WHERE login = :login AND password = :password"),
        {"login": login, "password": password}
    ).fetchone()
    return result


def add_response(self, joke_text: str):
    """Add a response (joke) if it doesn't exist already."""
    result = self.session.execute(
        text("SELECT id FROM responses WHERE text = :text"),
        {"text": joke_text}
    ).fetchone()
    if result:
        return result[0]
    else:
        self.session.execute(
            text("INSERT INTO responses (text) VALUES (:text)"),
            {"text": joke_text}
        )
        self.session.commit()
        return self.session.execute(
            text("SELECT id FROM responses WHERE text = :text"),
            {"text": joke_text}
        ).fetchone()[0]
    

def add_like(self, user_id: int, response_id: int):
    """Add a like entry for the user and the response."""
    self.session.execute(
        text("INSERT INTO likes (user_id, response_id) VALUES (:user_id, :response_id)"),
        {"user_id": user_id, "response_id": response_id}
    )
    self.session.commit()


def close(self):
    self.session.close()

@app.get("/cli_search&save/{mt}/{q}/{n}/{login}/{password}")
async def cli_search_and_save(mt: str, q: str, n: int, login: str, password: str):
    try:
        start_time = time.time()
        jokes = perform_search(model=mt, query=q, top_n=n)
        end_time = time.time()
        search_time = round(end_time - start_time, 2)
        user = db_session.get_user(login, password)

        if not user:
            db_session.close()
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        user_id = user[0]
        for joke in jokes:
            joke_text = joke["text"]
            response_id = db_session.add_response(joke_text)
            db_session.add_like(user_id, response_id)
        db_session.close()

        return {
            "message": f"{n} шуток добавлено к понравившемуся.",
            "search_time": search_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))