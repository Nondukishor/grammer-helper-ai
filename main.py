from fastapi import FastAPI
from dotenv import load_dotenv
import uvicorn
from routes.en_document import en_document_routers
load_dotenv()
app = FastAPI()
app.include_router(en_document_routers)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

