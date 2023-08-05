from copy import copy

from puzzlestream.backend.reference import PSCacheReference


class PSDict(dict):

    def __init__(self, sectionID, stream, changed=[], data={}):
        self.__changed = changed
        self.__id, self.__stream = sectionID, stream
        super().__init__(data)

    def __getitem__(self, key):
        """ Returns item from RAM if possible, if not the item is loaded from the
            stream and stored in RAM for faster access later on.
        """
        if super().__contains__(key):
            data = super().__getitem__(key)
        else:
            data = self.__stream.getItem(self.__id, key)
            while isinstance(data, PSCacheReference):
                data = self.__stream.getItem(int(data), key)
            super().__setitem__(key, data)
        return data

    def __setitem__(self, key, value):
        """ Stores item and logs changes. """

        if key not in self.changelog:
            self.changelog.append(key)
        super().__setitem__(key, value)

    def copy(self):
        """ Returns a copy of the dictionary. """
        return copy(self)

    @property
    def changelog(self):
        return self.__changed

    def resetChangelog(self):
        self.__changed = []
