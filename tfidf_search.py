import os
import json
from collections import defaultdict
from pymystem3 import Mystem
import string
import pickle 


class TFIDF_SEARCH():
    '''
    Класс для поиска через датасет, векторизованный при помощи tf-idf.
    '''
    with open(f'{os.path.abspath(os.path.dirname(__file__))}/load_from/inverted_index.pkl', 'rb') as f:
        loaded_inverted_index = pickle.load(f)

    with open(f'{os.path.abspath(os.path.dirname(__file__))}/load_from/stopwords.json', 'r') as f:
        loaded_stopwords = f.read()

    with open(f'{os.path.abspath(os.path.dirname(__file__))}/load_from/jokess_short.txt', 'r') as f:
        loaded_jokes = f.read()

    def __init__(self) -> None:
        self.inverted_index = self.loaded_inverted_index
        self.m = Mystem()
        self.stopwords = json.loads(self.loaded_stopwords)
        self.jokes = json.loads(self.loaded_jokes)


    def preprocess_query(self, query: str) -> list:
        '''
        Функция для препроцессинга запроса в поиске \n
        Запрос лемматизируется, убираются знаки препинания и стоп-слова \n
        Запрос делится на список терминов
        '''
        query = query.translate(str.maketrans('', '', string.punctuation)) #удалили знаки препинания
        lemmas = self.m.lemmatize(query) #лемматизировали 
        lemmas =  "".join(lemmas).strip()
        lemmas = lemmas.split()
        for lemma in lemmas:
            if lemma in self.stopwords:
                lemmas.remove(lemma)
        return lemmas

    def search_jokes(self, query: str, n: int) -> list:
        '''
        Функция ищет n-самых релевантных анекдотов
        '''
        query_terms = self.preprocess_query(query)
        joke_scores = defaultdict(float)  
        
        for term in query_terms:
            if term in self.inverted_index:
                for joke_id, score in self.inverted_index[term]:
                    joke_scores[joke_id] += score 

        # Отсортируем шутки по релевантности
        sorted_jokes = sorted(joke_scores.items(), key=lambda item: item[1], reverse=True)
        output_list = []

        for joke in sorted_jokes[:n]:
            # output_list.append(self.jokes[joke[0]])
            output_list.append(self.jokes[joke[0]])
        return output_list
    
    def cli_search_jokes(self, query: str, n: int) -> list:
        '''
        Функция ищет n-самых релевантных анекдотов
        '''
        query_terms = self.preprocess_query(query)
        joke_scores = defaultdict(float)  
        
        for term in query_terms:
            if term in self.inverted_index:
                for joke_id, score in self.inverted_index[term]:
                    joke_scores[joke_id] += score 

        # Отсортируем шутки по релевантности
        sorted_jokes = sorted(joke_scores.items(), key=lambda item: item[1], reverse=True)
        output_list = []

        for joke in sorted_jokes[:n]:
            # output_list.append(self.jokes[joke[0]])
            output_list.append([self.jokes[joke[0]], round(joke[1], 2)])
        return output_list