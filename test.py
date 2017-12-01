from trie import *

# RUN TEST- python test.py


class TrieTest(object):
    """
    Tests for Trie functionality.
    """

    def setup(self):
        self.data = [
            'pie', 'apple', 'anil', 'sam', 'syrup', 'zynga', 'test', 'comparison', 'dumpster', 'cup', 'cone',
            'anger', 'pierce', 'happy', 'sorrow', 'application'
        ]
        self.data = sorted(self.data)
        self.word_rank_map = {word: i+1 for i, word in enumerate(self.data)}
        self.trie = Trie()

    def test(self):

        self.setup()

        # Test addition and word count
        assert self.trie.node.word_count == 0
        for word in self.data:
            self.trie.add(word)
        assert self.trie.node.word_count == len(self.data)

        # Test search results (short first with rank).
        res = self.trie.find_matching('pie')
        assert res == [('pie', self.word_rank_map['pie']), ('pierce', self.word_rank_map['pierce'])]

        res = self.trie.find_matching('app')
        assert res == [('apple', self.word_rank_map['apple']), ('application', self.word_rank_map['application'])]


TrieTest().test()
