from trie import *

# RUN TEST- python test.py


class TrieTest(object):
    """
    Tests for Trie functionality.
    """

    def setup(self):
        self.data = [
            'pie', 'apple', 'anil', 'sam', 'syrup', 'zynga', 'test', 'comparison', 'dumpster', 'cup', 'cone',
            'anger', 'pierce', 'happy', 'sorrow'
        ]
        self.data = sorted(self.data)
        print 10, self.data
        self.word_rank_map = {word: i+1 for i, word in enumerate(self.data)}
        self.trie = Trie()

    def test(self):

        self.setup()

        # Test addition and word count
        assert self.trie.node.word_count == 0
        for word in self.data:
            self.trie.add(word)
        assert self.trie.node.word_count == len(self.data)

        print 20, self.trie.node.children.keys()
        print 21, [(k, self.trie.node.children[k].word_count)for k in sorted(self.trie.node.children.keys())]

        # Test search results (short first with rank).
        res = self.trie.find_matching('pie')
        print 13, res
        assert res == [('pie', self.word_rank_map['pie']), ('pierce', self.word_rank_map['pierce'])]
        print 12


TrieTest().test()
