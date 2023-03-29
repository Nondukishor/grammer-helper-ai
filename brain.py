from nltk.tokenize import word_tokenize, TweetTokenizer
from nltk.corpus import wordnet, stopwords, words
from nltk.stem import WordNetLemmatizer
from nltk.metrics import edit_distance
import nltk
import contractions
import string
import itertools
import tensorflow as tf
import numpy as np

model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, input_shape=(10,), activation='relu'),  #relu stands for Rectified Linear Unit
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])

model.compile(loss="binary_crossentropy", optimizer='adam', metrics=['accuracy'])
X = np.random.rand(1000, 10)
y = np.random.randint(0, 2, size=(1000,))
model.fit(X, y, epochs=10)

tokenizer = TweetTokenizer()
def remove_punctuation(text):
   tokens = word_tokenize(text)
   table = str.maketrans('', '', string.punctuation)
   words_without_punctuations = [token.translate(table) for token in tokens]
   text_without_punctuations = ' '.join(words_without_punctuations)
   return text_without_punctuations

def suggest_words(text):
    tokens = tokenizer.tokenize(text)
    suggestions = []
    for token in tokens:
        if token.lower() not in words.words():
            suggestions.append(edit_distance(token))
    return suggestions

def replace_stopwords_with_full_form(text):
    return contractions.fix(text)

def check_spelling(tokens):
    suggestions = []
    for token in tokens:
       suggestions.append(suggest_words(token))
    return suggestions

async def pos_check(text):
    rpt = remove_punctuation(text)
    beautify_sentence =  replace_stopwords_with_full_form(rpt)
    tokens =  word_tokenize(beautify_sentence)
    spell = check_spelling(tokens)
    if len(list(itertools.chain.from_iterable(spell))) == 0:
     pos = nltk.pos_tag(tokens)
     return pos
    else:
      suggestions = []
      for index , token in enumerate(tokens):
        suggestions.append("Possible corrections for {}: {}".format(token, spell[index]))
    return {
       "sentence" : text,
       "suggestions": suggestions,
       "spell": spell
    }