import re
from nltk.corpus import stopwords
from nltk.corpus import words as wrds
from nltk.stem.wordnet import WordNetLemmatizer


class Trainer:

    spam = {}
    ham = {}

    def __init__(self):
        pass

    def clear_string(self, string):
        res = re.compile('[^a-zA-Z]')
        return res.sub('', string)

    def get_words(self, string):
        replacements = ('.', ',', '-', '!', '?')
        for r in replacements:
            string = string.replace(r, ' ')
        return string.split()

    def filter_file(self):
        file_set = open('english_big.txt', 'r')
        lmt = WordNetLemmatizer()
        for line in file_set:
            words = self.get_words(line)
            for w in words:
                w = lmt.lemmatize(self.clear_string(w).lower())
                if (w not in stopwords.words('english')) and (w != ''):
                    if words[-1] == 'spam':
                        if w in self.spam:
                            self.spam[w] = self.spam.get(w) + 1
                        else:
                            if w in wrds.words():
                                self.spam[w] = 1
                    elif words[-1] == 'ham':
                        if w in self.ham:
                            self.ham[w] = self.ham.get(w) + 1
                        else:
                            if w in wrds.words():
                                self.ham[w] = 1
        file_set.close()


def main():
    tr = Trainer()
    tr.filter_file()
    print(tr.spam)
    return


if __name__ == "__main__":
    main()
