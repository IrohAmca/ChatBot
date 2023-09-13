import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('C:\\Users\\aliay\\PycharmProjects\\ChatBot\\words.pkl', 'rb'))
labels = pickle.load(open('C:\\Users\\aliay\\PycharmProjects\\ChatBot\\classes.pkl', 'rb'))
model = load_model('chatbot_model.keras')
#print(labels)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bagofwords(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bagofwords(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.1
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': labels[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json):

    tag = intents_list[0]['intent']
    #print(tag)
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        print(i['tag'])
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            #print(result)
            break
    return result

print("Hi,How can I help you?")

while True:

    message = input("")
    #print(message)
    ints = predict_class(message)
    res = get_response(ints, intents)
    try:

        encoded_text = res.encode('latin-1')
        decoded_text = encoded_text.decode('utf-8')
        print(decoded_text)
    except:
        print(res)
