import random
from collections import Counter
from bitstring import BitArray


def main():
    word_list = open("word-list.txt").readlines()
    word_list = [x.rstrip() for x in word_list]
    conversation = open("conversation.txt").readlines()
    conversation = [x.rstrip() for x in conversation]

    bits = BitArray()

    guesses_made = set()
    i = 0
    while i < len(conversation):
        if "_" not in conversation[i]:
            guesses_made = set()
            i = i + 1
            if i >= len(conversation):
                break

        word = conversation[i]
        guess = conversation[i + 1]
        i += 2

        probabilities = get_probabilities(word, word_list)
        probabilities = [x for x in probabilities if x[0] not in guesses_made]
        guesses_made.add(guess)

        probabilities.sort(key=count, reverse=True)

        if (
            len(probabilities) >= 3
            and probabilities[-2][1] < probabilities[0][1]
            and probabilities[-2][1] != probabilities[-1][1]
            and probabilities[0][1] != probabilities[1][1]
            and probabilities[-2][1] != probabilities[-3][1]
        ):
            if probabilities[0][0] != guess:
                if probabilities[-2][0] == guess:
                    bits.append(BitArray(uint=0, length=1))
                elif probabilities[-1][0] == guess:
                    bits.append(BitArray(uint=1, length=1))
                else:
                    print("error")
                    exit(1)

    print(bits.bytes.decode("ascii"))


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
