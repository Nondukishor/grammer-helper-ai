from brain import pos_check
from pydantic import BaseModel
class Message(BaseModel):
    text: str

async def chat(text: Message):
    result = await pos_check(text)
    return {
        "message": result
    }