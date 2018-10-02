import re
import os.path
import operator
import matplotlib.pyplot as plt
import pandas as pd
import pickle as pic
from collections import Counter
from nltk.corpus import stopwords
from nltk.corpus import words as woc
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
        string = string.split()
        for i in range(0, len(string)):
            if re.search('\d+', string[i]):
                string[i] = ''
        return string

    def filter_file(self):
        file_set = open('english_big.txt', 'r')
        lmt = WordNetLemmatizer()
        for line in file_set:
            words = self.get_words(line)
            for w in words[:-1]:
                w = lmt.lemmatize(lmt.lemmatize(self.clear_string(w).lower()), 'v')
                if (w not in stopwords.words('english')) and (w != ''):
                    if words[-1] == 'spam':
                        if w in self.spam:
                            self.spam[w] = self.spam.get(w) + 1
                        else:
                            if w in woc.words():
                                self.spam[w] = 1
                    elif words[-1] == 'ham':
                        if w in self.ham:
                            self.ham[w] = self.ham.get(w) + 1
                        else:
                            if w in woc.words():
                                self.ham[w] = 1
        file_set.close()

    def write_to_files(self):
        if os.path.exists('spam_words.pkl') and os.path.exists('ham_words.pkl'):
            sw = open('spam_words.pkl', 'rb')
            self.spam = pic.load(sw)
            sw.close()
            hw = open('ham_words.pkl', 'rb')
            self.ham = pic.load(hw)
            hw.close()
            return
        self.filter_file()
        sw = open('spam_words.pkl', 'wb')
        pic.dump(self.spam, sw, 2)
        sw.close()
        hw = open('ham_words.pkl', 'wb')
        pic.dump(self.ham, hw, 2)
        hw.close()
        return

    def draw_plot(self):
        word_s = (sorted(self.spam.items(), key=operator.itemgetter(1)))[-11:-1]
        df_s = pd.DataFrame(word_s, columns=['word', 'frequency'])
        df_s.plot(kind='bar', x='word')
        word_h = (sorted(self.ham.items(), key=operator.itemgetter(1)))[-11:-1]
        df_h = pd.DataFrame(word_h, columns=['word', 'frequency'])
        df_h.plot(kind='bar', x='word')
        plt.show()

    def calc_pos(self, string):
        words = self.get_words(string)
        lmt = WordNetLemmatizer()
        spam_all = sum(self.spam.values())
        ham_all = sum(self.ham.values())
        spam_p = 1
        ham_p = 1
        added_s = 0
        added_h = 0
        l = 0
        for i in range(0, len(words)):
            words[i] = lmt.lemmatize(lmt.lemmatize(self.clear_string(words[i]).lower()), 'v')
            if (words[i] in stopwords.words('english')) or (words[i] == '') or (words[i] not in woc.words()):
                words[i] = ''
            if words[i] != '':
                l = l + 1
        count = Counter(words)
        for key in count.keys():
            if (key not in self.spam) and key != '':
                added_s = added_s + count[key]
            if (key not in self.ham) and key != '':
                added_h = added_h + count[key]
        for key in count.keys():
            if key != '':
                if key in self.spam:
                    spam_p = (spam_p * count[key]) / self.spam[key]
                else:
                    spam_p = (spam_p * count[key]) / added_s
                if key in self.ham:
                    ham_p = (ham_p * count[key]) / self.ham[key]
                else:
                    ham_p = (ham_p * count[key]) / added_h
        #d = spam_p * (l / spam_all) + ham_p * (l / ham_all)
        #print(spam_p * (spam_all / (spam_all + ham_all)))
        #print(ham_p * (ham_all / (spam_all + ham_all)))
        return spam_p * (spam_all / (spam_all + ham_all)), ham_p * (ham_all / (spam_all + ham_all))

#def main():
    #tr = Trainer()
    #tr.write_to_files()
    #print(tr.calc_pos('Hi are you dating today?'))
    #lmt = WordNetLemmatizer()
    #print(lmt.lemmatize(lmt.lemmatize(tr.clear_string('n').lower()), 'v') in stopwords.words('english'))
    #tr.draw_plot()
    #return

# TRY TO CHANGE DICT, DO PLOTS
#if __name__ == "__main__":
    #main()
