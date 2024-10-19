import argparse
from tfidf_search import TFIDF_SEARCH
from bert_search import BERT_SEARCH

tf_search = TFIDF_SEARCH()
bert = BERT_SEARCH()


def main():
    parser = argparse.ArgumentParser(description="Search jokes using TF-IDF or BERT models.")
    
    #Добавляем необходимые нам аргументы
    parser.add_argument("--query", type=str, required=True, help="Поисковый запрос")
    parser.add_argument("--model", type=str, default='tfidf', help="Модель векторизации: 'tfidf' или 'bert'")
    parser.add_argument("--top_n", type=int, default=3, help="Количество анекдотов на выход")

    # Парсим из командной строки
    args = parser.parse_args()

    # Выбор модели векторизации из аргумента
    if args.model == "tfidf":
        results = tf_search.search_jokes(args.query, args.top_n)
        print(f"{args.top_n}-анекдотов:\n", results)
    elif args.model == "bert":
        results = bert.search_jokes(args.query, args.top_n)
        print(f"{args.top_n}-анекдотов:\n", results)
    else:
        print("Вы не выбрали один из доступных методов векторизации. Пожалуйста, выберите \
для аргумента model значение 'tfidf' или 'bert'")

# Entry point for the script
if __name__ == "__main__":
    main()

