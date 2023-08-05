from operator import itemgetter

from ngramgraphs.graph import Graph, make_ngram_graph

from ngramgraphs.similarity import value_similarity, containment_similarity,\
    normalized_value_similarity


# see "Representation Models for Text Classification"


class NgramgraphClassifier:
    def __init__(self, n, by_words=False):
        # dictionary mapping from class labels to their graphs
        self.document_graphs = {}
        self.n = n
        self.by_words = by_words

    @classmethod
    def train_from_documents(cls, training_docs, n, by_words=False):
        classifier = cls(n, by_words)
        class_graphs = make_classgraphs(
            training_docs, classifier.n, classifier.by_words)
        classifier.document_graphs = class_graphs
        return classifier

    def _make_feature_vectors(self, document):
        graph = make_ngram_graph(document, self.n, self.by_words)
        feature_vectors = {}
        for label, class_graph in self.document_graphs.items():
            feature_vectors[label] = make_feature_vector(graph, class_graph)
        return feature_vectors

    def classify(self, document):
        feature_vectors = self._make_feature_vectors(document)
        # return label and vector where feature vector has the highest value,
        # i.e. where the comparison vector represents the highest similarity
        return max(feature_vectors.items(), key=itemgetter(1))


def make_classgraphs(training_docs, n, by_words=False):
    """Make a dict which maps from class labels to their document class
    graphs.

    :param training_docs: Dict[str, Iterable[str]]
    :param n: int
    :param by_words: bool
    :return: Dict[str, Graph]
    """
    d = {}
    for label, documents in training_docs.items():
        graph = make_classgraph(documents, n, by_words)
        d[label] = graph
    return d


def make_classgraph(documents, n, by_words=False):
    """Determine the class graph for a given iterable of documents

    :param documents: Iterable[str]
    :param n: int
    :param by_words: bool
    :return: Graph
    """
    # 1. make a new empty graph g
    # 2. iterate over documents, use counter i
    #    3. transform document d_i into an ngram graph, call it g_i
    #    4. graph g_i is merged with g to form a new graph
    #       with the following properties:
    graph = Graph()
    for i, d in enumerate(documents, 1):
        g_i = make_ngram_graph(str(d), n, by_words)
        graph = merge_graphs(graph, g_i, i)
    return graph


def merge_graphs(g1, g2, i):
    """

    :param g1:
    :param g2:
    :param i: denotes the iteration step
    :return: a new merged graph
    """
    edges1 = set(g1.edges())
    edges2 = set(g2.edges())

    g = Graph()

    # iterate over those edges first that occur in both graphs
    for edge in edges1 & edges2:
        w1 = g1.get_weight(edge[0], edge[1])
        w2 = g2.get_weight(edge[0], edge[1])
        new_weight = w1 + (w2 - w1) / i
        g.add_edge(edge[0], edge[1], weight=new_weight)

    # now iterate over the remaining edges
    for edge in edges1 ^ edges2:
        g.add_edge(edge[0], edge[1], weight=edge.attr['weight'])
    return g


def make_feature_vector(graph1, graph2):
    vs = value_similarity(graph1, graph2)
    cs = containment_similarity(graph1, graph2)
    nvs = normalized_value_similarity(graph1, graph2)
    return (vs, cs, nvs)
