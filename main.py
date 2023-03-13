from typing import Union
from fastapi import FastAPI
from bs4 import BeautifulSoup
from nltk import word_tokenize
import re
import requests
# modules import end

app = FastAPI()


@app.get("/")
def health():
    return {
        "message": "Server is running"
    }


@app.get("/api/data-collect/{url_param}")
def read_item(url_param: str):
    html_data = requests.get("https://"+url_param)
    soup = BeautifulSoup(html_data.content, 'html.parser')
    data = soup.get_text()
    words = word_tokenize(data)
    words = [re.sub(r'[^A-Za-z0-9]+', '', token)
             for token in words if re.sub(r'[^A-Za-z0-9]+', '', token)]
    words = " ,".join(list(set(words)))
    return {
        "words": words
    }
