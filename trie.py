import os
from Queue import Queue

FILE = os.environ.get("FILE", "data.csv")


LOG_INFO = True


def log(msg):
    print msg


def info(msg):
    if LOG_INFO:
        log('[INFO] '+msg)


def error(msg):
    log('[ERROR] '+msg)


RESULT_COUNT_PER_QUERY = 10
THRESHOLD_LEN_FOR_QUERY = 3
CASE_SENSITIVE_VOCAB = False
ALPHABETS = '.0123456789abcdefghijklmnopqrstuvwxyz{}'.format('ABCDEFGHIJKLMNOPQRSTUVWXYZ' if CASE_SENSITIVE_VOCAB else '')


class TrieNode(object):

    def __init__(self, is_word=False, children=None):
        self.is_word = is_word  # Represents whether path from root till current node is a word in the dictionary or not.
        self.children = children or {}
        self.word_count = 1 if is_word else 0  # Stores count of words under this node including current node.

    def __str__(self):
        return 'word: {} ({})'.format(self.is_word, str(self.children))


class Trie(object):

    node = TrieNode()

    def __init__(self, alphabets=ALPHABETS):
        self.alphabets = alphabets

    def add(self, term):
        """
        Adds given term to Trie in O(n) time, n being length of term.
        :param term:str: Word to add.
        """

        # Validate term
        if any([c not in self.alphabets for c in term]):
            error('Unable to add word [{}]: characters out of supported alphabets present in the word.'.format(term))
            return
        node = self.node
        index = 0
        n = len(term)

        # Add term to trie till last char.
        while index < n:
            # Anytime a word going through a node is added, word count of that node is increased.
            node.word_count += 1
            c = term[index]
            if c not in node.children:
                node.children[c] = TrieNode(is_word=(index == n-1))  # If last char node, mark it as word.
            node = node.children[c]
            index += 1

    @classmethod
    def populate_children_words(cls, node, children_words, pre='', max_count=-1, parent_level_smaller_words_count=0):
        """
        Populates given list of 'children_words' with all words starting with given 'pre' text.
        Also adds rank to each word based on 'parent_level_smaller_words_count' and word-count of other nodes.
        IMP- This method populates results in DFS manner, i.e. results will come in sorted manner.
        :param node:TrieNode: Node of last character whose children words are to be found.
        :param children_words:list: List which is to be populated with children words.
        :param pre:str: Text which is prefix of children words.
        :param max_count:int: Max number of result items to populate, if -1 no limit is put.
        :param parent_level_smaller_words_count:int: Number of words smaller than parent prefix in the trie.
        """
        for key in sorted(node.children.keys()):
            word = '{}{}'.format(pre, key)
            # Check if max-count is reached, reaches only if max-count given.
            max_count_reached = max_count < 0 or len(children_words) >= max_count
            if max_count_reached:
                return
            if node.children[key].is_word and not max_count_reached:
                # On match, add word and it's rank to the result list.
                children_words.append((word, parent_level_smaller_words_count))
            # Add word-count of current node for further nodes.
            parent_level_smaller_words_count += node.children[key].word_count
            cls.populate_children_words(node.children[key], children_words, pre=word, max_count=max_count, parent_level_smaller_words_count=parent_level_smaller_words_count)

    @classmethod
    def populate_children_words_bfs(cls, node, children_words, pre='', max_count=-1, parent_level_smaller_words_count=0):
        """
        Populates given list of 'children_words' with all words starting with given 'pre' text.
        Also adds rank to each word based on 'parent_level_smaller_words_count' and word-count of other nodes.
        IMP- This method populates results in BFS manner, i.e. shorter results will come first.
        :param node:TrieNode: Node of last character whose children words are to be found.
        :param children_words:list: List which is to be populated with children words.
        :param pre:str: Text which is prefix of children words.
        :param max_count:int: Max number of result items to populate, if -1 no limit is put.
        :param parent_level_smaller_words_count:int: Number of words smaller than parent prefix in the trie.
        """

        queue = Queue()
        queue.put((node, pre, parent_level_smaller_words_count))
        while not queue.empty():
            next_node, next_pre, next_parent_level = queue.get()
            for key in sorted(next_node.children.keys()):
                word = '{}{}'.format(next_pre, key)
                # Check if max-count is reached, reaches only if max-count given.
                max_count_reached = max_count < 0 or len(children_words) >= max_count
                if max_count_reached:
                    return
                if next_node.children[key].is_word and not max_count_reached:
                    # On match, add word and it's rank to the result list.
                    children_words.append((word, next_parent_level+1))
                    # Add word-count of current node for further nodes.
                    next_parent_level += next_node.children[key].word_count
                queue.put((next_node.children[key], word, next_parent_level))

    def find_matching(self, term, count=RESULT_COUNT_PER_QUERY):
        """
        Finds the matching words in dictionary for given term.
        :param term:str: Query string.
        :param count:int: Maximum number of results to be returned.
        :return list: List of results where each element is a tuple of 2 elements; first being matched word and second being it's rank.
        """
        results = []
        node = self.node
        index = 0
        n = len(term)
        parent_level = 0
        while node and index < n:
            c = term[index]
            if c in node.children:
                parent, node = node, node.children[c]
                for i in parent.children.keys():
                    # For those siblings of current node, which were smaller than current node, add their word_count for calculating rank later.
                    if i < c:
                        parent_level += parent.children[i].word_count
                index += 1
            else:
                break
        # If all characters matched, show words starting from the word. Else, show words starting from matched part as they may be relevant too.
        if node:
            if index == n and node.is_word:
                parent_level += 1
                results.append((term, parent_level))
            Trie.populate_children_words_bfs(
                node, results, pre=term[:index], max_count=count, parent_level_smaller_words_count=parent_level
            )

        return results


# t = Trie()
# t.add('sau')
# t.add('saura')
# t.add('saaamki')
# t.add('sam')
# t.add('sin')
# t.add('sinio')
# t.add('sanr')
# # node = t.node.children['s'].children['i'].children['n']
# # print node
# # print node.word_count
# print t.find_matching('san')
