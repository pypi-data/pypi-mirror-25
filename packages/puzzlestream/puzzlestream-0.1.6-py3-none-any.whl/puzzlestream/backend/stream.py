import diskcache as dc


class PSStream(dc.Cache):

    def __init__(self, path):
        super().__init__(path)

    def getItem(self, id, key):
        return super().__getitem__(str(id) + "-" + str(key))

    def setItem(self, id, key, data):
        super().__setitem__(str(id) + "-" + str(key), data)
