class PSEvent:

    def __init__(self):
        self.__methods = []

    def connect(self, method):
        self.__methods.append(method)

    def disconnect(self, method):
        i = self.__methods.index(method)
        del self.__methods[i]

    def emit(self, *args):
        for m in self.__methods:
            m(*args)
