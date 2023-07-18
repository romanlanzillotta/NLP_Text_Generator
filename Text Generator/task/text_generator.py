import operator
from collections import Counter
import random
import nltk
from nltk.tokenize import WhitespaceTokenizer

path_ = input()
# path_ = 'C:/Users/roman/PycharmProjects/Text Generator/Text Generator/task/test/corpus.txt'
with open(path_, "r", encoding="utf-8") as arch_:
    text = arch_.read()  # read Game of Thrones script corpus

# Stage 1/5
tokenizer = WhitespaceTokenizer()
tokenized = tokenizer.tokenize(text)
token_set = set(tokenized)
# print("Corpus statistics:")
# print("All tokens:", len(tokenized))
# print("Unique tokens:", len(token_set))

# Stage 2/5
bigrams = list(nltk.bigrams(tokenized))
# print("Number of bigrams:", len(bigrams))

# Stage 3/5
bigrams_dict = dict()
for index, bigram in enumerate(bigrams):
    bigrams_dict.setdefault(bigram[0], []).append(bigram[1])
bigrams_counters = dict()
for head, tails in bigrams_dict.items():
    bigrams_counters[head] = dict(sorted(Counter(tails).items(),
                                         key=operator.itemgetter(1), reverse=True))

# # Stages 1-3
# userin = input()
# while userin != "exit":
#     try:
#         # user_ind = int(userin)
#         # print(tokenized[user_ind])
#         # print("Head: ", bigrams[user_ind][0], "\tTail: ",bigrams[user_ind][1])
#         user_in = userin
#         print("Head:", userin)
#         counter_ = bigrams_counters[user_in]
#         for tail, counts in counter_.items():
#             print("Tail:", tail, "\tCount:", str(counts))
#     except TypeError:
#         print("Type Error. Please input an integer")
#     except ValueError:
#         print("Value Error. Please input an integer")
#     except IndexError:
#         print("Index Error. Please input an integer that is in the range of the corpus.")
#     except KeyError:
#         print("Key Error. The requested word is not in the model. Please input another word.")
#     except Exception as error:
#         print(error)
#     userin = input()


# Stage 4/5 and 5/5. Pseudo-sentence generator.
def validate_first_token(tkn):
    return bool(tkn[0].isupper() & (not validate_last_token(tkn)))


def validate_last_token(tkn):
    return bool(tkn[-1] in ["!", ".", "?"])


sentences = []
for _ in range(10):
    first_token = random.choice(list(bigrams_counters.keys()))
    sentence = list([first_token])
    ini = 0
    while (len(sentence) < 5) | (not validate_last_token(sentence[-1])):
        # Beginning
        while not validate_first_token(sentence[ini]):
            first_token = random.choice(list(bigrams_counters.keys()))
            sentence[ini] = first_token
        # middle tokens
        tails_dict = bigrams_counters[sentence[-1]]
        new_token = random.choices(list(tails_dict.keys()),
                                   weights=list(tails_dict.values()))[0]
        sentence.append(new_token)
        # validate again if there is a previous token with "."
        # and length has not been reached
        # we need to check a new sentence beginning with a valid token.
        if (validate_last_token(sentence[-1])) & (len(sentence) < 5):
            sentence.append(" ")
            ini = len(sentence) - 1
    sentences.append(' '.join(sentence))
    print(sentences[-1])

