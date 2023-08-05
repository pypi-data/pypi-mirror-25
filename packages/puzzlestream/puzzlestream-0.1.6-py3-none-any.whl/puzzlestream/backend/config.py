import json
import os
from threading import Thread

from appdirs import user_config_dir

from puzzlestream.backend.event import PSEvent


class PSConfig(dict):

    def __init__(self, *args):
        super().__init__(*args)
        self.__configDir = user_config_dir("PuzzleStream")
        self.__edited = PSEvent()
        self.load()

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.edited.emit(key)
        self.save()

    def __setDefaultItem(self, key, value):
        if key not in self:
            super().__setitem__(key, value)
            self.edited.emit(key)

    @property
    def edited(self):
        return self.__edited

    def save(self):
        thr = Thread(target=self.__save)
        thr.start()

    def __save(self):
        if not os.path.isdir(self.__configDir):
            os.mkdir(self.__configDir)

        with open(self.__configDir + "/config.json", "w") as f:
            json.dump(self, f)

    def load(self):
        if os.path.isfile(self.__configDir + "/config.json"):
            try:
                with open(self.__configDir + "/config.json", "r") as f:
                    self.clear()
                    self.update(json.load(f))
            except Exception as e:
                print(e)
        self.__setDefaults()

    def __setDefaults(self):
        self.__setDefaultItem("last projects", [])
        self.__setDefaultItem("Test", True)
        self.__setDefaultItem("Test 2", "bla")
        self.__setDefaultItem("Test 3", [0, ["0", "1", "2"]])

    def addRecentProject(self, path):
        if path in self["last projects"]:
            i = self["last projects"].index(path)
            del self["last projects"][i]
        self["last projects"].append(path)

        if len(self["last projects"]) > 10:
            del self["last projects"][0]

        self.edited.emit("last projects")
        self.save()
