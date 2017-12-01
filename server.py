import csv
import os
import time

from flask import Flask, jsonify, request

from trie import *
app = Flask(__name__)

FILE = os.environ.get("FILE", "data.csv")


processed_vocab = {}


def preprocess_vocab():

    with open(FILE) as f:
        reader = csv.reader(f)
        terms = [row[0] for row in reader]
        trie = Trie()
        start = time.clock()
        count = 0
        for term in terms[1:]:
            trie.add(term if CASE_SENSITIVE_VOCAB else term.lower())
            count += 1
        info('Preprocessing complete in {} ms for {} words'.format((time.clock() - start) * 1000, count))
        processed_vocab['trie'] = trie


def find_matching(term):
    return [{'name': res[0], 'rank': res[1] + 1} for res in processed_vocab['trie'].find_matching(term)] if len(term) >= THRESHOLD_LEN_FOR_QUERY else []


preprocess_vocab()


@app.route('/auto')
def hello_world():
    query = request.args.get("q", '')
    start = time.clock()
    results = find_matching(query)
    info('Results found in {} ms'.format((time.clock() - start) * 1000))
    resp = jsonify(results=results[:RESULT_COUNT_PER_QUERY])  # top 10 results
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# ================================================================
# LOGIC
# ================================================================
# Fast response - Used TRIE for dictionary storage, gives O(n) insertion and lookup time for string of length n
# Short item first - Used BFS when finding matched.
# Rank - Maintained word count of children nodes with each node. For rank just looked up words before taken word at each level of trie.
# Fuzzy - Couldn't think of anything that does not violate the first requirement.
# ================================================================
