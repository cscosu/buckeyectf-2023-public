import random
from collections import Counter
from bitstring import BitArray


def main():
    word_list = open("/etc/dictionaries-common/words").readlines()
    word_list = [
        x.rstrip().lower()
        for x in word_list
        if x.rstrip().isalpha() and x.rstrip().isascii()
    ]
    encode("bctf{ju57_w47ch_7h053_6u35535}", word_list)


def make_guess(guess, current_word, answer):
    assert len(current_word) == len(answer)
    new_word = list(current_word)
    for i in range(len(current_word)):
        if guess == answer[i]:
            new_word[i] = guess
    return "".join(new_word)


def encode(message, word_list):
    bits = BitArray(bytes(message, "ascii"))

    while len(bits) > 0:
        answer = random.choice(word_list)
        displayed_word = "_" * len(answer)
        print(displayed_word)
        guesses_made = set()
        while "_" in displayed_word:
            probs = get_probabilities(displayed_word, word_list)
            guesses = [x for x in probs if x[0] not in guesses_made]
            guesses.sort(key=count, reverse=True)
            if (
                len(bits) > 0
                and random.random() < 0.5
                and len(guesses) >= 3
                and guesses[-2][1] < guesses[0][1]
                and guesses[-2][1] != guesses[-1][1]
                and guesses[0][1] != guesses[1][1]
                and guesses[-2][1] != guesses[-3][1]
            ):
                if bits[0]:
                    guess = guesses[-1][0]
                else:
                    guess = guesses[-2][0]
                del bits[0]
            else:
                guess = guesses[0][0]
            print(guess)
            guesses_made.add(guess)

            displayed_word = make_guess(guess, displayed_word, answer)
            print(displayed_word)


def count(x):
    return x[1]


def get_probabilities(word, word_list):
    filtered_word_list = [x for x in word_list if len(x) == len(word)]
    filtered_word_list = [x for x in filtered_word_list if match(word, x)]
    counter = Counter()
    for x in filtered_word_list:
        counter.update(set(x) - set(word))
    return counter.most_common(26)


def match(a, b):
    for i in range(0, len(a)):
        if a[i] != b[i] and a[i] != "_":
            return False
    return True


if __name__ == "__main__":
    main()
