from puzzlestream.backend.dict import PSDict
from puzzlestream.backend.reference import PSCacheReference


class PSStreamSection:

    def __init__(self, sectionID, stream):
        self.__stream = stream
        self.__id = sectionID
        self.changelog = {}

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return str(self.data)

    @property
    def id(self):
        return self.__id

    def updateData(self, lastStreamSectionID, moduleID, data, log):
        for key in data:
            if key in self.changelog and key not in log:
                ref = PSCacheReference(lastStreamSectionID)
                del data[key]
                data[key] = ref

        for key in data:
            self.__stream.setItem(self.__id, key, data[key])
        self.__logChanges(moduleID, log)

    def __logChanges(self, moduleID, log):
        for item in log:
            if item in self.changelog:
                self.changelog[item].append(moduleID)
            else:
                self.changelog[item] = [moduleID]
        self.sectionDict.resetChangelog()

    @property
    def sectionDict(self):
        return PSDict(self.__id, self.__stream)

    @property
    def data(self):
        data = {}

        for key in self.__stream:
            if key.startswith(str(self.__id)):
                originalKey = key.replace(str(self.__id) + "-", "")
                d = self.__stream.getItem(self.__id, originalKey)
                while isinstance(d, PSCacheReference):
                    d = self.__stream.getItem(int(d), originalKey)
                data[originalKey] = d

        return data

    def addSection(self, streamSection):
        for key in streamSection.changelog:
            ref = PSCacheReference(streamSection.id)
            self.__stream.setItem(self.__id, key, ref)
        self.changelog.update(streamSection.changelog)

    def copy(self, sectionID):
        new = PSStreamSection(sectionID, self.__stream)
        new.addSection(self)
        return new
