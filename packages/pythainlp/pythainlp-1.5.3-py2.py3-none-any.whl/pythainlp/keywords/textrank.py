'''
 An implmentation of TextRank in python 

Fork by https://gist.github.com/voidfiles/1646117
'''
import nltk
import itertools
from operator import itemgetter

from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.pagerank import pagerank
from pygraph.classes.exceptions import AdditionError
class textrank(object):
    def __init__(self, text):
        self.text = nltk.word_tokenize(text)
        self.tagged = nltk.pos_tag(self.text)
        self.tagged = self.filter_for_tags(self.tagged)
        self.tagged = self.normalize(self.tagged)
        self.unique_word_set = self.unique_everseen([x[0] for x in self.tagged])
        self.gr = digraph()
        self.gr.add_nodes(list(self.unique_word_set))
        self.window_start = 0
        self.window_end = 2
        while 1:
            self.window_words = self.tagged[self.window_start:self.window_end]
            if len(self.window_words) == 2:
                print(self.window_words)
                try:
                    self.gr.add_edge((self.window_words[0][0], self.window_words[1][0]))
                except AdditionError as e:
                    print('already added %s, %s' % ((self.window_words[0][0], self.window_words[1][0])))
            else:
                break
            self.window_start += 1
            self.window_end += 1
        self.calculated_page_rank = pagerank(self.gr)
        di = sorted(self.calculated_page_rank.items(), key=itemgetter(1))
        for k, g in itertools.groupby(di, key=itemgetter(1)):
            print(k, map(itemgetter(0), g))
        #return di#self.calculated_page_rank
    def filter_for_tags(self,tagged, tags=['NN', 'JJ', 'NNP']):
        return [item for item in tagged if item[1] in tags]
    def normalize(self,tagged):
        return [(item[0].replace('.', ''), item[1]) for item in tagged]
    def unique_everseen(self,iterable, key=None):
        "List unique elements, preserving order. Remember all elements ever seen."
        # unique_everseen('AAAABBBCCDAABBB') --> A B C D
        # # unique_everseen('ABBCcAD', str.lower) --> A B C D
        seen = set()
        seen_add = seen.add
        if key is None:
            for element in itertools.filterfalse(seen.__contains__, iterable):
                seen_add(element)
                yield element
        else:
            for element in iterable:
                k = key(element)
                if k not in seen:
                    seen_add(k)
                    yield element
a=textrank("""แมวกินปลาแมว""")
print(a)