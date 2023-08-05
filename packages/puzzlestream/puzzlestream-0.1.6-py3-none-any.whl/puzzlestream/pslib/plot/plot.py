from matplotlib.figure import Figure
from collections import Iterable


class Plot(Figure):

    def __init__(self, nrows=1, ncols=1, figsize=(7, 4), dpi=150,
                 sharex=False, sharey=False, gridspec_kw=None):
        super().__init__(figsize=figsize, dpi=dpi)
        for i in range(1, nrows * ncols + 1):
            self.add_subplot(nrows, ncols, i)

    def get_xlabel(self, i=0):
        return self.ax(i).xaxis.get_label_text()

    def set_xlabel(self, label, i=0):
        self.ax(i).set_xlabel(label)

    def get_ylabel(self, i=0):
        return self.ax(i).yaxis.get_label_text()

    def set_ylabel(self, label, i=0):
        self.ax(i).set_ylabel(label)

    def get_title(self, i=0):
        return self.ax(i).get_title()

    def set_title(self, title, i=0):
        self.ax(i).set_title(title)

    def get_xlim(self, i=0):
        return self.ax(i).get_xlim()

    def set_xlim(self, *limits, i=0):
        self.ax(i).set_xlim(limits)

    def get_xlim(self, i=0):
        return self.ax(i).get_ylim()

    def set_ylim(self, *limits, i=0):
        self.ax(i).set_ylim(limits)

    def grid(self, i=0, *args, **kwargs):
        self.ax(i).grid(*args, **kwargs)

    def set_properties(self, prop, i=0):
        for key in prop:
            if key == "title":
                self.setTitle(prop[key], i=i)
            elif key == "x-label":
                self.setXLabel(prop[key], i=i)
            elif key == "y-label":
                self.setYLabel(prop[key], i=i)
            elif key == "x-limits":
                self.setXLim(prop[key], i=i)
            elif key == "y-limits":
                self.setYLim(prop[key], i=i)

    def savefig(self, filename, bbox_inches="tight", dpi=300):
        super().savefig(filename, bbox_inches=bbox_inches, dpi=dpi)

    def plot(self, x, y, *args, e_x=None, e_y=None, visible=True,
             i=0, markersize=4, ls="none", fmt=".", **kwargs):
        if e_x is not None or e_y is not None:
            bar = self.ax(i).errorbar(x, y, xerr=e_x, yerr=e_y,
                                      ls=ls, fmt=fmt,
                                      markersize=markersize, **kwargs)
            bar[0].set_visible(visible)
        else:
            plot, = self.ax(i).plot(x, y, markersize=markersize,
                                    *args, **kwargs)
            plot.set_visible(visible)

    def imshow(self, x, *args, i=0, **kwargs):
        return self.ax(i).imshow(x, *args, **kwargs)

    def bar(self, x, y, *args, e_x=None, e_y=None, i=0):
        self.ax(i).bar(x, y, xerr=e_x, yerr=e_y, *args)

    def text(self, x, y, text, *args, i=0, **kwargs):
        self.ax(i).text(x, y, text, *args, **kwargs)

    def legend(self, *args, i=0, **kwargs):
        self.ax(i).legend(*args, **kwargs)

    def hspan(self, start, end, *args, i=0, **kwargs):
        self.ax(i).axhspan(start, end, *args, **kwargs)

    def vspan(self, start, end, *args, i=0, **kwargs):
        self.ax(i).axvspan(start, end, *args, **kwargs)

    def ax(self, i=0):
        return self.get_axes()[i]
