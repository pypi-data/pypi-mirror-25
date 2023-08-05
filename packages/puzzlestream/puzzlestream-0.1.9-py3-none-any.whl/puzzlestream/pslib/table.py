import tabulate as tab


class Table:

    def __init__(self, replace=[]):
        self.__tab = []
        self.__head = []
        self.__vhead = False
        self.__caption = ""
        self.__rep = replace

    def getLatex(self):
        tab.LATEX_ESCAPE_RULES = {}
        t = self.__replace(tab.tabulate(self.__tab, headers=self.__head,
                                        tablefmt="latex"))
        return t

    def getText(self):
        t = self.__replace(tab.tabulate(self.__tab, headers=self.__head))
        return t

    def __replace(self, t):
        for r in self.__rep:
            t = t.replace(r[0], r[1])
        return t

    def getTable(self):
        return self.__tab

    def __str__(self):
        return self.getText()

    def addRow(self, content, index=None):
        if isinstance(content, list):
            if index is None:
                self.__tab.append(content)
            else:
                self.__tab.insert(index, content)
            self.__expand()
        else:
            raise NotImplementedError

    def addColumn(self, content, index=None):
        if isinstance(content, list):
            run = max(len(content), len(self.__tab))
            for i in range(run):
                if i < len(self.__tab):
                    if i >= len(content):
                        content.append("")
                    if index is None:
                        self.__tab[i].append(content[i])
                    else:
                        self.__tab[i].insert(index, content[i])
                else:
                    if len(self.__tab) > 0:
                        length = self.__maxRowLength()
                    else:
                        length = 0

                    if index is None:
                        ind = length
                    else:
                        ind = index

                    if ind < 0:
                        inde = length + ind

                    row = ["" for j in range(ind)]
                    row.append(content[i])
                    row.extend(["" for j in range(length - ind - 1)])
                    self.__tab.append(row)
        else:
            raise NotImplementedError

    def __expand(self):
        maxLength = self.__maxRowLength()
        for row in self.__tab:
            if len(row) < maxLength:
                diff = maxLength - len(row)
                row.extend(["" for i in range(diff)])

    def __maxRowLength(self):
        length = 0
        for row in self.__tab:
            if len(row) > length:
                length = len(row)
        return length

    def removeRow(self, index=None):
        if index is None:
            self.__tab.pop()
        else:
            self.__tab.pop(index)

    def removeColumn(self, index=None):
        for row in self.__tab:
            if index is None:
                row.pop()
            else:
                row.pop(index)

    def setHHeaders(self, headers):
        self.__head = headers

    def setVHeaders(self, headers):
        if self.__vhead:
            self.removeColumn(0)
        self.addColumn(headers, 0)
        self.__vhead = True

    @property
    def caption(self):
        return self.__caption

    @caption.setter
    def caption(self, text):
        self.__caption = text
