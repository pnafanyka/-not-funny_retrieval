from transformers import AutoTokenizer, BertModel
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import json

class BERT_SEARCH():
    '''
    Класс для поиска через эмюеддинги БЕРТа
    '''
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    #модель выбрана с HuggingFace по встроенным фильтрам
    with open(f'{os.path.abspath(os.path.dirname(__file__))}/load_from/jokess_short.txt', 'r') as f:
        loaded_jokes = f.read()

    def __init__(self) -> None:
        self.joke_embeds = np.load(f'{os.path.abspath(os.path.dirname(__file__))}/load_from/joke_embeddings.npy')
        self.jokes = json.loads(self.loaded_jokes)

    def search_jokes(self, query: str, n: int) -> list:
        '''
        Функция находит n-самых близких шуток к запросу
        '''
        query_embed = query_embed = self.model.encode(query)
        similarities = cosine_similarity(query_embed.reshape(1, -1), self.joke_embeds)
        top_k_indices = np.argsort(similarities[0])[-n:][::-1]

        output_list = []
        for id in top_k_indices:
            output_list.append(self.jokes[id])

        return output_list