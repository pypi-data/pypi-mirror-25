import math


def document_frequency(token, documents):
    """Count the number of documents that contain `token`."""
    return sum(int(token in doc) for doc in documents)


def secure_inverse_document_frequencies_smooth(documents):
    """Make a dict mapping from all tokens to their smoothed IDFs."""
    def generate_token_idfs():
        for doc in documents:
            for token in doc:
                yield (
                    token,
                    secure_inverse_document_frequency_smooth(token, documents))
    return dict(generate_token_idfs())


def secure_inverse_document_frequency_smooth(token, documents):
    n = len(documents)
    df = document_frequency(token, documents)
    return math.log(1 + n / (1 + df))


def count_overall_frequency(tokenized_documents):
    """Count the overall occurence of all (tokenised) words through the
    whole corpus.

    """
    document_frequency = {}
    for document in tokenized_documents:
        for word in document:
            if word in document_frequency:
                document_frequency[word] += 1
            else:
                document_frequency[word] = 1
    return document_frequency
