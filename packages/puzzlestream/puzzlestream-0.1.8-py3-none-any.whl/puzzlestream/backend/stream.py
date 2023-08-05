import diskcache as dc


class PSStream(dc.Cache):

    def __init__(self, path, *args):
        super().__init__(path, *args)

    def getItem(self, id, key):
        return super().__getitem__(str(id) + "-" + str(key))

    def setItem(self, id, key, data):
        super().__setitem__(str(id) + "-" + str(key), data)
