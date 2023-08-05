from puzzlestream.pslib.plot import Plot


class QuickPlot(Plot):

    def __init__(self, x, y, *args, e_x=None, e_y=None,
                 nrows=1, ncols=1, figsize=(7, 4), **kwargs):
        super().__init__(nrows=nrows, ncols=ncols, figsize=figsize)
        self.__x, self.__y, self.__e_x, self.__e_y = (x, y, e_x, e_y)
        self.plot(self.__x, self.__y, *args,
                  e_x=self.__e_x, e_y=self.__e_y, **kwargs)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_e_x(self):
        return self.__e_x

    def get_e_y(self):
        return self.__e_y
