from fastapi import APIRouter, Path, Query
from textblob import TextBlob
from sklearn.preprocessing import LabelEncoder
from models.en_document import EnDocuments
from config.db import conn
from Schemas.en_document import serializeDict, serializeList
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import joblib

en_document_routers = APIRouter()


@en_document_routers.get('/')
async def find_all():
    return serializeList(conn.grammerly.en_documents.find())


def error_detect(blob):
    for sentence in blob.sentences:
        subject = None
        for word, tag in sentence.tags:
            if tag.startswith('NN') or tag.startswith('PRP'):
                subject = word
            elif tag.startswith('VB'):
                if (subject == 'I' and tag.endswith('S')) or (subject != 'I' and not tag.endswith('S')):
                    print(
                        f"Error: '{sentence}' contains a subject-verb agreement error.")


@en_document_routers.post('/')
async def create_en_document(en_document: EnDocuments):
    inputText = TextBlob(en_document.incorrect_sentence)
    return {
        "correct_sentence": inputText.correct()
    }


@en_document_routers.post("/build-model")
async def buildModel():
    data = serializeList(conn.grammerly.en_documents.find())
    df = pd.DataFrame(data)
    correct_sentences = df['correct_sentence'].tolist()
    incorrect_sentences = df['incorrect_sentence'].tolist()
    error_types = df['error_in_sentence'].tolist()
    sentences = correct_sentences + incorrect_sentences + error_types
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(sentences)
    y = [2] * len(correct_sentences) + [1] * len(incorrect_sentences)+ [0] * len(error_types)
    classifier = SVC()
    classifier.fit(X, y)
    joblib.dump(classifier, "grammar-model.pkl")

@en_document_routers.post('/check-sentence/{sentence}')
async def checkSentence(sentence: str):
    loaded_model= joblib.load("grammar-model.pkl")
    new_sentences =[sentence]
    vectorizer = TfidfVectorizer()
    X_new = vectorizer.fit_transform(new_sentences)
    predictions = loaded_model.predict(X_new)
    response = []
    for sentence, prediction in zip(new_sentences, predictions):
        if prediction == 1:
            response.append({
                "sentence": sentence,
                "is_correct": True,
                "suggestion": None
            })
        else:
            response.append({
                "sentence": sentence,
                "is_correct": False,
                "suggestion": None
            })
    return response
