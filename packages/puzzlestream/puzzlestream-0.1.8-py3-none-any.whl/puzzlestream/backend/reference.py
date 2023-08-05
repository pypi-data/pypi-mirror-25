class PSCacheReference:

    def __init__(self, sectionID):
        self.__sectionID = sectionID

    def __int__(self):
        return self.__sectionID

    def __str__(self):
        return str(self.__sectionID)

    def __repr__(self):
        return "reference to " + str(self.__sectionID)

    @property
    def sectionID(self):
        return self.__sectionID
