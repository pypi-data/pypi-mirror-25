from puzzlestream.pslib.plot.plot import Plot
from puzzlestream.pslib.table import Table


class Export:

    def __init__(self, path=""):
        if path != "":
            self.__path = path
        else:
            self.__path = "."
        self.__plots = {}
        self.__data = {}
        self.__tables = {}

    def update(self, export):
        if isinstance(export, Export):
            self.__plots.update(export.plots)
            self.__data.update(export.data)
            self.__tables.update(export.tables)
        else:
            raise Exception

    def addPlot(self, name, plot):
        if isinstance(plot, Plot):
            self.__plots[name] = plot

    def addData(self, name, data, math=True):
        if math:
            self.__data[name] = "$" + str(data) + "$"
        else:
            self.__data[name] = str(data)

    def addTable(self, name, table, replace=[]):
        if isinstance(table, Table):
            self.__tables[name] = (table, replace)

    def saveData(self, filename):
        if len(self.__data) > 0:
            text = ""
            data = list(self.__data.items())
            data = sorted(data, key=lambda x: x[0])

            for d in data:
                text += r"\newcommand{\%s" % str(d[0])
                text += r"}{" + d[1] + r"}"
                text += "\n"

            with open(self.__path + "/Data/" + filename, "w") as file:
                file.write(text)

    def savePlots(self, type="pdf"):
        for key in self.__plots:
            self.__plots[key].savefig(
                self.__path + "/Plots/" + key + "." + type)

    def __replace(self, text, replace):
        for r in replace:
            text = text.replace(r[0], r[1])
        return text

    def saveTables(self, filename):
        if len(self.__tables) > 0:
            completeText = ""
            for key in self.__tables:
                text = ""
                table = self.__tables[key][0]
                if table.plot is None:
                    exportType = "table"
                else:
                    exportType = "figure"

                text += "\n"
                text += r"\newcommand{\%s" % str(key)
                text += "}{\n" + r"\begin{" + exportType + "}[h!]" + "\n"
                if table.plot is None:
                    if table.caption != "":
                        text += r"\caption{" + table.caption + "}\n"
                else:
                    text += r"\includegraphics[width=\textwidth]{"
                    text += "Plots/" + table.plot + "}\n"
                text += "\centering" + "\n"
                text += table.getLatex() + "\n"
                if table.plot is not None:
                    if table.caption != "":
                        text += r"\caption{" + table.caption + "}\n"
                text += r"\label{"
                if exportType == "table":
                    text += "tab"
                else:
                    text += "fig"
                text += ":" + str(key) + "}\n"
                text += r"\end{" + exportType + "}}"
                text += "\n"
                completeText += self.__replace(text, self.__tables[key][1])

            with open(self.__path + "/Data/" + filename, "w") as f:
                f.write(completeText)

    @property
    def data(self):
        return self.__data

    @property
    def plots(self):
        return self.__plots

    @property
    def tables(self):
        return self.__tables
