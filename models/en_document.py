from pydantic import BaseModel

class EnDocuments(BaseModel):
    correct_sentence: str
    incorrect_sentence: str
    error_in_sentence: str