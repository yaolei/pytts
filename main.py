from typing import Union
import edge_tts
from fastapi import FastAPI
from pydantic import BaseModel

from connectDb import session, get_db
from db.testDb import MP3File
import datetime
import os
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import select, delete

from until.tools import judge_language
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# VOICE = "en-US-AvaNeural"
# VOICE = "zh-CN-XiaoxiaoNeural"

class Items(BaseModel):
    message_id: str
    send_by_name: str
    message_connent: str
    send_by_id: str

class TestItems(BaseModel):
    id:str
    content:str

@app.get("/")
async def read_root():
    v  = judge_language("So what do you think")
    return {"Hello": v}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/testApi")
async def handle_test_api(items:TestItems):
    # return {"success get data": {items.content}}
    print("Received data@@@@:", items.dict())
    return {"data": {"id": items.id, "content": items.content}}

@app.post("/tts")
async def tts(itmes:Items):
    v  = judge_language(itmes.message_connent)
    if v == "EN":
         VOICE = "en-US-AvaNeural"
    else:
         VOICE = "zh-CN-XiaoxiaoNeural"
    communicate = edge_tts.Communicate(itmes.message_connent, VOICE)
    OUTPUT_FILE = itmes.send_by_name + itmes.message_id + ".mp3"
    
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    with open(OUTPUT_FILE, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    print("translated audio successfully.")
                    # print(f"WordBoundary: {chunk}")
                data = await StoreAudio(OUTPUT_FILE, itmes.message_id, itmes.send_by_name)
    if data is not None:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)                   
    return data

async def validateVoideExite (userId:str):
    # query = session.query(MP3File).filter(MP3File.send_user_id == userId).one()
    result = session.execute(select(MP3File.id).where(MP3File.send_user_id == userId))
    data = result.fetchone()
    if data is not None:
        delete_query = session.execute(delete(MP3File).where(MP3File.send_user_id == userId))
        session.commit()
        print(f"Deleted {delete_query.rowcount} rows")
    return ''

async def StoreAudio (fileName:str, 
                      send_user_id:str, 
                      send_user_name:str):
            file_path = fileName
            await validateVoideExite(send_user_id)
            try:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    mp3_file = MP3File(message_id=os.path.basename(file_path), 
                                message_data = file_data,
                                send_user_id = send_user_id, 
                                send_user_name = send_user_name, 
                                created_date = datetime.datetime.now())
                    session.add(mp3_file)
                    session.commit()
                    print(f"File insert success: {mp3_file}")
            except Exception as e:
                session.rollback()
                print(f"An error occurred !!!!!!!!: {e}")
            finally:
                session.close()
            return {'state': 'ok'}