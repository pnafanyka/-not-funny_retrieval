Здесь представлена инструкция выполнения скрипта по поиску шуток в базе данных

    Для поиска через TF-IDF датасет был лемматизирован, почищен от стоп-слов и знаков препинания.

    Для поиска через BERT никакого препроцессинга датасета не было

ИНСТРУКЦИЯ ПО ЗАПУСКУ:
1. Скачать репозиторий командой 
    git clone 
2. Прописать для установки всех необходимых зависимостей
    pip install requirements.txt
3. Прописать следующую команду, выбрав векторизацию
    python3 main_search.py --query "Кошка и собака" --model 'tfidf|bert' --top_n 2 

    NB! Обязательно прописать только query (запрос), в таком случае, по умолчанию будет использован поиск по tfidf, а на выходе будет 3 шутки.


P.S.
В папке dump лежат промежуточные файлы, которые могут быть полезны для просмотра блокнта ниже
Блокнот с обработкой сырых данных лежит по ссылке:
https://colab.research.google.com/drive/1Dq4XGQ143uS4KWWEzVztL_p-TRd2mBXA?authuser=1#scrollTo=6LjpT0GCvs_3&uniqifier=4