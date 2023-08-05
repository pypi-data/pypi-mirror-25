import importlib as imp
import multiprocessing as mp
import os
import random
import sys
import string
import traceback
from multiprocessing.connection import Client, Listener
from threading import Thread
from time import sleep, time

import numpy as np
import psutil

from puzzlestream import pslib
from puzzlestream.backend.event import PSEvent


class PSWorker:

    def __init__(self):
        self.__process, self.__listener, self.__conn = None, None, None
        self.__finished = PSEvent()
        self.__newStdout = PSEvent()
        self.__progressUpdate = PSEvent()
        self.__name, self.__path, self.__libs = None, None, None

    def __getstate__(self):
        return (self.__name, self.__path, self.__libs)

    def __setstate__(self, state):
        # self.__init__()
        self.__name, self.__path, self.__libs = state

    @property
    def finished(self):
        return self.__finished

    @property
    def newStdout(self):
        return self.__newStdout

    @property
    def progressUpdate(self):
        return self.__progressUpdate

    def setName(self, name):
        self.__name = name

    def setPath(self, path):
        self.__path = path

    def setLibs(self, libs):
        self.__libs = libs

    def run(self, streamSection, currentID, lastID):
        thr = Thread(target=self._run,
                     args=(streamSection, currentID, lastID))
        thr.start()

    def pause(self):
        if self.__process is not None:
            p = psutil.Process(self.__process.pid)
            p.suspend()
        else:
            return False
        return True

    def resume(self):
        if self.__process is not None:
            p = psutil.Process(self.__process.pid)
            p.resume()
        else:
            return False
        return True

    def stop(self):
        if self.__process is not None:
            self.__process.terminate()
        else:
            return False
        return True

    def __importModule(self):
        for lib in self.__libs + [os.path.dirname(pslib.__file__)]:
            if lib not in sys.path:
                sys.path.append(lib)
        spec = imp.util.spec_from_file_location(self.__name, self.__path)
        mod = imp.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def __newPassword(self):
        return "".join(random.choice(string.ascii_letters) for i in range(20))

    def _run(self, streamSection, currentID, lastID):
        address = ("localhost", 10000 + currentID)
        authkey = bytes(self.__newPassword(), "utf-8")
        self.__listener = Listener(address, authkey=authkey)
        self.__process = mp.Process(
            target=self._calculate,
            args=(address, authkey, streamSection, currentID, lastID)
        )

        self.__process.start()
        sleep(0.01)
        self.__conn = self.__listener.accept()

        result = None
        while True:
            try:
                result = self.__conn.recv()

                if isinstance(result, str):
                    self.newStdout.emit(result)
                elif isinstance(result, float):
                    self.progressUpdate.emit(result)
                else:
                    self._finish(*result)
                    break
            except EOFError:
                self._finish(False, [], "Aborted by user.", [0, 0], {})
                break

    def _finish(self, success, log, out, times, testResults):
        self.__conn.close()
        self.__listener.close()
        self.__process.join()
        self.__process, self.__listener, self.__conn = None, None, None
        self.finished.emit(success, log, out, times, testResults)

    def _calculate(self, address, authkey, streamSec, currentID, lastID):
        conn = Client(address, authkey=authkey)

        def sendPrint(*args, sep=" ", end="\n"):
            s, sep = "", str(sep)
            for a in args:
                s += str(a) + sep
            conn.send(s + end)

        def progressUpdate(finished, total=None):
            if total is None and isinstance(finished, float):
                if finished < 0:
                    finished = 0
                elif finished > 1:
                    finished = 1
                conn.send(finished)
            else:
                finished = finished / total
                progressUpdate(finished)

        np.random.seed(int.from_bytes(os.urandom(4), "big"))

        runtime, savetime, testResults = 0, 0, {}

        try:
            mod = self.__importModule()

            mod.print = sendPrint
            mod.progressUpdate = progressUpdate

            inp = streamSec.sectionDict

            t0 = time()
            out = mod.main(inp)
            runtime = time() - t0
            log = out.changelog

            t0 = time()
            inp.update(out)
            streamSec.updateData(lastID, currentID, inp, log)
            savetime = time() - t0

            success, output = "successful", ""

            if "testFunctions" in dir(mod):
                if isinstance(mod.testFunctions, list):
                    for func in mod.testFunctions:
                        result = getattr(mod, func)(out)

                        if isinstance(result, bool):
                            testResults[func] = result

            del out

        except Exception as e:
            message = traceback.format_exc()
            success, log, output = "error", [], message

        times = [runtime, savetime]

        conn.send([success, streamSec.changelog, output, times, testResults])
        conn.close()
