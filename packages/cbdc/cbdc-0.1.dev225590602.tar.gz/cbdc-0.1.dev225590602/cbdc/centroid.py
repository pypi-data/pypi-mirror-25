import math

from cbdc import dirs2corpus, corpus2matrices, tokenize

from cbdc.vectors import Vector, dotproduct
from cbdc.tokendict import TokenDict


class CbdcClassifier:
    def __init__(self, document_frequencies=None):
        # `centroids` is a dict mapping from document classes (strings)
        # to their centroid vectors
        self.centroids = {}
        # inverse document frequencies of all terms in the training corpus
        self.document_frequencies = dict(document_frequencies or {})
        # dictionary mapping from token to IDs AND BACK
        self.tokendict = TokenDict()

    @classmethod
    def train_from_dirs(cls, directories):
        corpus, idfs = dirs2corpus(directories)
        classifier = cls(idfs)
        matrices, tokendict = corpus2matrices(corpus, idfs)
        for label, matrix in matrices.items():
            centroid = make_centroid_vector(matrix)
            classifier.centroids[label] = centroid
        classifier.tokendict = tokendict
        return classifier

    def classify(self, document):
        # make sure that # `centroids` attribute is not empty
        assert self.centroids
        # make sure that `train` has initialized `document_frequencies`
        # attribute
        assert self.document_frequencies is not None
        # 1) calculate vector for `document`:
        # "First we use the **document-frequencies of the various terms
        # computed from the training set** to compute the tf-idf weighted
        # vector-space representation of x,
        # and scale it so x is of unit length"
        # tokenized = tokenize_document(document)
        text = tokenize(document)
        vector_args = [0 for _ in self.tokendict.id2token]
        for token in text:
            tf = document.count(token)
            try:
                idf = self.document_frequencies[token]
            except KeyError:
                idf = 0
            tf_idf = tf * idf

            index = self.tokendict.token2id.get(token)
            if index is not None:
                vector_args[index] = tf_idf
        vector = Vector(*vector_args).normalize()
        # 2) compare similarity of calculated vector with all centroid vectors
        max_similarity = float('-inf')
        best_label = None
        for label, centroid in self.centroids.items():
            similarity = similarity_between_documents(centroid, vector)
            if similarity > max_similarity:
                max_similarity = similarity
                best_label = label
        # 3) return key whose centroid vector has the highest similarity
        return best_label, max_similarity


def make_centroid_vector(document_vectors):
    size = len(document_vectors)
    if size == 0:
        return Vector()
    vector_sum = Vector(*([0] * len(document_vectors[0])))
    for vector in document_vectors:
        vector_sum += vector
    return (1/size) * vector_sum


similarity_between_documents = dotproduct
similarity_between_documents.__doc__ = (
    'It is assumed that both vectors have unit length')


def similarity_to_centroid(document, centroid):
    dividend = dotproduct(document, centroid)
    divisor = math.sqrt(dotproduct(centroid, centroid))
    return (1/divisor) * dividend
