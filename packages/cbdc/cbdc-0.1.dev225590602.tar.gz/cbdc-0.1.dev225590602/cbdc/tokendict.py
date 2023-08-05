class TokenDict:
    def __init__(self):
        self._token2id = {}
        self._id2token = {}

    @property
    def token2id(self):
        return self._token2id

    @property
    def id2token(self):
        return self._id2token

    def set(self, token, id):
        self._token2id[token] = id
        self._id2token[id] = token

    def update(self, tokendict):
        for token, id in tokendict.token2id.items():
            self.set(token, id)

    def __len__(self):
        l = len(self.token2id)
        assert l == len(self.id2token)
        return l

    def __repr__(self):
        return repr(self.id2token)
