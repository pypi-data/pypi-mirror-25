from functools import partial, reduce
from operator import concat
from collections import defaultdict, Counter

from nltk.util import ngrams
from pygraphviz import AGraph

from ngramgraphs import util
from ngramgraphs.datastructures import MultiDict

from amazonreviewanalyzer_preprocess import tokenize


# TODO: consider using a simple custom graph class, independent of AGraph
class Graph(AGraph):
    def contains_edge(self, other_edge):
        """Returns true if the given edge occurs in the graph, False
        otherwise. Attributes and directions are ignored.

        """
        for edge in self.edges():
            if edges_equal(edge, other_edge):
                return True
        return False

    def add_edge(self, u, v, **kwargs):
        # make sure that direction goes from lower to higher value
        a, b = min(u, v), max(u, v)
        super().add_edge(a, b, **kwargs)

    def add_edges(self, edges):
        for (u, v, weight) in edges:
            self.add_edge(u, v, weight=weight)

    def get_weight(self, u, v):
        edge1 = self.get_edge(u, v)
        w = get_edge_weight(edge1)
        if w is None:
            edge2 = self.get_edge(v, u)
            # u->v is unavailable, try v->u instead'
            return get_edge_weight(edge2)
        return w

    def __len__(self):
        """Cardinality of a graph is defined as the no. of edges, see the
        paper "Representation Models for Text Classification for a
        reference.

        """
        return len(self.edges())


def preprocess(document):
    """Remove stop chars (punctuation), stop words (using the definition
    of NLTK) and stem every remaining word.

    """
    return ' '.join(tokenize(document))


def make_ngram_graph(document, n, by_words=False):
    document = preprocess(document)
    nodes = []
    if not by_words:
        ngram = ngrams(document, n)
        nodes = map(partial(reduce, concat), ngram)
    graph = Graph()
    graph.add_nodes_from(nodes)
    if by_words:
        edges = make_word_edges(document, n)
        for adjacent_nodes, weight in edges.items():
            for node, adjacent_node in zip(adjacent_nodes, adjacent_nodes[1:]):
                graph.add_edge(
                    node, adjacent_node, weight=weight, label=weight)
    else:
        edges = make_char_edges(document, n)
        for node, adjacent_nodes in edges.items():
            for adjacent_node, weight in Counter(adjacent_nodes).items():
                # weights denote how often ngram occur together
                graph.add_edge(
                    node, adjacent_node, weight=weight, label=weight)
    return graph


def make_word_edges(document, n):
    # take the maximum for each found co-occurence
    # by conjugating the counter objects via the | operator
    edges = reduce(
        Counter.__or__,
        (Counter(
            {tuple(sorted(nodes)): weight}) for nodes, weight in
            Counter(ngrams(document.split(), n)).items()),
        Counter())
    return edges


def make_char_edges(document, n):
    edges = defaultdict(list)
    for i in range(len(document) - 2):  # FIXME: always minus two?!
        key = document[i:i+n]
        for j in range(-n, n+1):
            seq = util.slice_with_default(document, i+j, i+j+n)
            seq_as_str = util.seq_to_string(seq)
            if len(seq_as_str) == len(key) and seq_as_str != key:
                edges[key].append(seq_as_str)
    return edges


def graphs_equal(graph1, graph2):
    """Note that edge attributes are ignored.

    """
    d1 = MultiDict.from_list(map(sorted, graph1.edges()))
    d2 = MultiDict.from_list(map(sorted, graph2.edges()))
    return d1 == d2


def get_edge_weight(edge):
    weight = edge.attr['weight']
    if weight is None:
        return None
    return float(weight)


def edges_equal(edge1, edge2):
    "compares two edges, ignoring their attributes and directions"
    return sorted([edge1[0], edge1[1]]) == sorted([edge2[0], edge2[1]])


def common_edges(graph1, graph2):
    """Return a list of all edges that occur both in graph1 and
    graph2.

    """
    edges = []
    for edge in graph2.edges():
        if graph1.contains_edge(edge):
            edges.append((edge, graph1.get_edge(*edge)))
    return edges
