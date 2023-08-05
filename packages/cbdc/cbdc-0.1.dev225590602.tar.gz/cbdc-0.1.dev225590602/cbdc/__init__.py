from itertools import chain
from collections import defaultdict
import os

from cbdc.tokendict import TokenDict
from cbdc.vectors import Vector
from cbdc.tfidf import secure_inverse_document_frequencies_smooth,\
    count_overall_frequency
from cbdc.util import readfile

from amazonreviewanalyzer_preprocess import tokenize


__all__ = ['documents2matrix']

"""
0. input: corpus as list of strings (each string representing one
   document)
1. remove stop chars (such as punctuation) and stop words
2. remove words that appear only once in the whole corpus
   (corpus = collection of all documents)
3. return a matrix by converting each document (list of strings now) to a
   vector (tuple of tf-idf frequencies)
"""


def dirs2corpus(dirs):
    """Convert an iterable of directories to a dictionary of documents.
    Note that the documents have been tokenized and that terms with lower
    frequency than 2 will have been eliminated.

    This function returns the described dict and a frequency distribution
    of all words that occur at least 2 times.

    :param dirs: List[str]
    :return: Tuple[Dict[str, List[str]], Dict[str, int]]
    """
    corpus = {}
    documents = defaultdict(list)
    for dir in dirs:
        label = os.path.basename(dir)
        for filename in sorted(os.listdir(dir)):
            with open(os.path.join(dir, filename)) as f:
                document = '\n'.join(readfile(f))
            tokenized_document = tokenize(document)
            documents[label].append(list(tokenized_document))

    tokenized_all = list(chain.from_iterable(
        documents.values()))
    overall_frequency = count_overall_frequency(tokenized_all)

    idfs = secure_inverse_document_frequencies_smooth(tokenized_all)

    for label, documents in documents.items():
        cleaned_docs = remove_lowfreq_words(documents, overall_frequency)
        corpus[label] = cleaned_docs

    return corpus, idfs


def corpus2matrices(corpus, idfs):
    """

    :param corpus: Dict[str, List[str]]
        dictionary mapping from labels to lists of documents
    :param idfs: Dict[str, float]
        dictionary mapping from tokens to their inverse document
        frequencies
    :return: Tuple[Dict[str, List[Vector]], TokenDict]
        dictionary mapping from labels to their matrices
    """
    # all_docs = corpus.values()
    matrices = {}
    all_docs = chain.from_iterable(corpus.values())
    #  make a dict mapping from words to their unique IDs
    tokendict = tokenized_documents2ids(all_docs)
    for label, documents in corpus.items():
        matrix = []
        for document in documents:
            # skip empty documents (i.e. if all tokens exist only once)
            # if not document:
            #     continue
            row = []
            # make sure that we iterate from lowest ID to highest ID
            for _, token in sorted(tokendict.id2token.items()):
                idf = idfs[token]
                # use raw count for term frequency
                tf = document.count(token)
                # append the tf-idf
                row.append(tf * idf)
            vector = Vector(*row).normalize()
            matrix.append(vector)
        matrices[label] = matrix
    return matrices, tokendict


def remove_lowfreq_words(tokenized_documents, docfreq, min_freq=2):
    """Remove all words that have a lower frequency than `min_freq`."""
    return [
        [token for token in text if docfreq[token] >= min_freq]
        for text in tokenized_documents]


def tokenized_documents2ids(tokenized_documents):
    tokendict = TokenDict()
    for i, word in enumerate(set(chain.from_iterable(tokenized_documents))):
        tokendict.set(word, i)
    return tokendict


def tokenize_documents(documents):  # pragma: no cover
    return [tokenize(document) for document in documents]
