from typing import Union
from fastapi import FastAPI
from bs4 import BeautifulSoup
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize, sent_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, state_union, wordnet, movie_reviews
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk
import re
import requests
import random
# modules import end

app = FastAPI()


@app.get("/")
def health():
    return {
        "message": "Server is running"
    }


@app.get("/api/data-collect/{url_param}")
def collect_data(url_param: str):
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


@app.get('/api/tokenize')
def test_tokenize_nltk():
    cow_paragraph = "The cow is a very useful pet animal. It is a domestic animal kept by people at home for many purposes. The cow is a feminine gender of ‘ox’. The cow has four legs, two horns, a tail, two eyes, two ears and four udders. She eats a lot of grass and fodder. She produces milk."
    return {
        "sentence_tokenize": sent_tokenize(cow_paragraph),
        "word_tokenize": word_tokenize(cow_paragraph)
    }


@app.get('/api/stop-words')
def test_stopwords():
    cow_paragraph = "The cow is a very useful pet animal. It is a domestic animal kept by people at home for many purposes. The cow is a feminine gender of ‘ox’. The cow has four legs, two horns, a tail, two eyes, two ears and four udders. She eats a lot of grass and fodder. She produces milk."
    words = word_tokenize(cow_paragraph)
    stop_words = stopwords.words("english")
    filtered_sentence = []
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    return {
        "filtered_sentence": filtered_sentence
    }


@app.get('/api/stemming')
def test_stemming():
    exm_words = ["drive", "driver", "driving", "drivingly"]
    ps = PorterStemmer()
    words = []
    for w in exm_words:
        words.append(ps.stem(w))
    return {
        "words": words
    }


"""
CC coordinating conjunction
CD cardinal digit
DT determiner
EX existential there (like: “there is” … think of it like “there exists”)
FW foreign word
IN preposition/subordinating conjunction
JJ adjective ‘big’
JJR adjective, comparative ‘bigger’
JJS adjective, superlative ‘biggest’
LS list marker 1)
MD modal could, will
NN noun, singular ‘desk’
NNS noun plural ‘desks’
NNP proper noun, singular ‘Harrison’
NNPS proper noun, plural ‘Americans’
PDT predeterminer ‘all the kids’
POS possessive ending parent’s
PRP personal pronoun I, he, she
PRP$ possessive pronoun my, his, hers
RB adverb very, silently,
RBR adverb, comparative better
RBS adverb, superlative best
RP particle give up
TO, to go ‘to’ the store.
UH interjection, errrrrrrrm
VB verb, base form take
VBD verb, past tense took
VBG verb, gerund/present participle taking
VBN verb, past participle taken
VBP verb, sing. present, non-3d take
VBZ verb, 3rd person sing. present takes
WDT wh-determiner which
WP wh-pronoun who, what
WP$ possessive wh-pronoun whose
WRB wh-abverb where, when
"""


@app.get('/api/tagging')
def test_tagging():
    train_text = state_union.raw('2005-GWBush.txt')
    sample_text = state_union.raw('2006-GWBush.txt')
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)
    try:
        for i in tokenized:
            words = word_tokenize(i)
            tagged = pos_tag(words)
            return tagged
    except Exception as e:
        return str(e)


@app.get('/api/chunking')
def test_chunking():
    train_text = state_union.raw('2005-GWBush.txt')
    sample_text = state_union.raw('2006-GWBush.txt')
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)
    try:
        for i in tokenized:
            words = word_tokenize(i)
            tagged = pos_tag(words)
            chunkGram = r"""Chunk : {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            return chunked
    except Exception as e:
        return str(e)

# remove something from string


@app.get('/api/chinking')
def test_chunking():
    train_text = state_union.raw('2005-GWBush.txt')
    sample_text = state_union.raw('2006-GWBush.txt')
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)
    try:
        for i in tokenized:
            words = word_tokenize(i)
            tagged = pos_tag(words)
            chunkGram = r"""Chunk : {<.*>+}
            }<VB.?|In|DT>+{"""
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            return chunked
    except Exception as e:
        return str(e)


@app.get('/api/named-entity-recognition')
def test_chunking():
    train_text = state_union.raw('2005-GWBush.txt')
    sample_text = state_union.raw('2006-GWBush.txt')
    custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
    tokenized = custom_sent_tokenizer.tokenize(sample_text)
    try:
        for i in tokenized:
            words = word_tokenize(i)
            tagged = pos_tag(words)
            namedEnt = nltk.ne_chunk(tagged, binary=True)
            print(namedEnt)
            return namedEnt
    except Exception as e:
        return str(e)


@app.get('/api/lemmatizing')
def test_lemmatizing():
    lemmatizer = WordNetLemmatizer()
    return lemmatizer.lemmatize("better", pos="a")


@app.get('/api/word-net/{type}')
def test_wordnet(type: str):
    try:
        synonyms = []
        antonyms = []
        for syn in wordnet.synsets("good"):
            for l in syn.lemmas():
                synonyms.append(l.name())
                if l.antonyms():
                    antonyms.append(l.antonyms()[0].name())
            print(set(synonyms))
            print(set(antonyms))
        w1 = wordnet.synset('ship.n.01')
        w2 = wordnet.synset('boat.n.01')

        if type == 'sim':
            return w1.wup_similarity(w2)
        elif type == "sys":
            return synonyms
        else:
            return antonyms

    except Exception as e:
        return str(e)


@app.get('/api/text-classification')
def text_classification():
    documents = [(list(movie_reviews.words(fileid)), category)
                 for category in movie_reviews.categories()
                 for fileid in movie_reviews.fileids(category)]
    random.shuffle(documents)
    print(documents[1])

    all_words = []
    for w in movie_reviews.words():
        all_words.append(w.lower())

    all_words = nltk.FreqDist(all_words)
    print(all_words.most_common(15))
    print(all_words["stupid"])
    return all_words.most_common(15)
