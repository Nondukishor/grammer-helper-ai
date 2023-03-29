from fastapi import FastAPI
from controller import chat
from pydantic import BaseModel
from textblob import TextBlob
app = FastAPI()
class Message(BaseModel):
    text: str
@app.post("/")
async def chatRoute(message: Message):
    return await chat(message.text)
@app.post('/correct-sentence')
async def correct_sentence():

