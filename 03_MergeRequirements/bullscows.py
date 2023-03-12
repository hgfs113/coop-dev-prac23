import collections
import os
import random
import sys
from argparse import ArgumentParser
from urllib.request import urlopen


def parse_args():
    parser = ArgumentParser()

    parser.add_argument("dictionary", help="Имя файла или URL", type=str)
    parser.add_argument("length", default=5, nargs="?",
         help="Длина используемых слов", type=int)

    args = parser.parse_args()
    return args


def bullscows(guess: str, secret: str) -> (int, int):
    assert len(guess) == len(secret), f"Длина guess: {len(guess)} не совпадает "\
         f"с длиной secret:  {len(secret)}"

    guess_dict = collections.defaultdict(int)
    secret_dict = collections.defaultdict(int)

    b, c = 0, 0

    for letter_g, letter_s in zip(guess, secret):
        b += letter_g == letter_s
        guess_dict[letter_g] += 1
        secret_dict[letter_s] += 1

    for letter, secret_cnt in secret_dict.items():
        guess_cnt = guess_dict[letter]
        c += min(guess_cnt, secret_cnt)

    return b, c - b


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret_word = random.choice(words)
    guess_word = None
    n = 0
    while guess_word != secret_word:
        guess_word = ask("Введите слово: ", words)
        b, c = bullscows(guess_word, secret_word)
        inform("Быки: {}, Коровы: {}", b, c)
        n += 1
    return n


def ask(prompt: str, valid: list[str] = None) -> str:
    word = input(prompt)
    while valid and word not in valid:
        word = input(prompt)
    return word


def inform(format_string: str, bulls: int, cows: int) -> None:
    print(format_string.format(bulls, cows), file=sys.stdout)


if __name__ == "__main__":
    args = parse_args()

    if not os.path.exists(args.dictionary):
        print(f"Файла {args.dictionary} не существует, пробую скачать", file=sys.stderr)
        try:
            fname, _ = urlopen(args.dictionary)
        except Exception as e:
            print(f"Произошла ошибка во время загрузки: {e}", file=sys.stderr)
            exit(0)
    else:
        fname = args.dictionary

    with open(fname, "r") as f:
        data = f.read()
    words = list(filter(lambda x: len(x) == args.length, data.split()))
    assert len(words) > 0, "Пустой словарь"

    print(f"Число попыток: {gameplay(ask, inform, words)}", file=sys.stdout)
