
import os

import numpy as np
import matplotlib.pyplot as plt

from .namer import AtompawNamer

class AtompawPlotter:
    """A plotter for AtomPAW."""

    _to_parent_functions = ['show_wfn', 'show_logderiv']

    def __init__(self, rootname=None, namer=None):

        if rootname:
            self.namer = AtompawNamer(rootname)
        elif namer and isinstance(namer, AtompawNamer):
            self.namer = namer
        else:
            self.namer = AtompawNamer()

    def plot_wfn(self, Nproj, show=False):
        """
        Arguments:
            Nproj: list (lmax)
                Number of projector for each angular momentum quantum number.
            show: bool, optional
        """
        fig = plt.figure(figsize=(18,14))
        Nlines = len(Nproj)
        Ncols = max(Nproj)
        iwfn = 0
        for l, N in enumerate(Nproj):
            iline = l + 1
            for i in range(N):
                iwfn += 1
                icol = i + 1
                iplot = l * Ncols + icol
    
                ax = fig.add_subplot(Nlines, Ncols, iplot)
    
                plot_wfn(self.namer.wfn(iwfn), ax)
    
                xmin, xmax = ax.get_xlim()
                ax.set_xlim(0.,xmax)
                ax.hlines(0, *ax.get_xlim(), color='k', lw=.5, zorder=-1)
    
        fig.savefig(self.namer.wfn_pdf)

        if show:
            plt.show()
        else:
            plt.close()

    def plot_logderiv(self, Nl=1, show=False):
        """
        Arguments:
            Nl:
                Number of angular momentum.
            pdf: bool, optional
                Plot figure in a pdf file, then open it.
        """
        fig = plt.figure(figsize=(15,5))
        for i in range(Nl):
            ax = fig.add_subplot(1,Nl,i+1)
            plot_logderiv(self.namer.logderiv(i), ax, title='l = '+str(i))
    
            ax.set_ylim(-50,50)
    
        fig.savefig(self.namer.logderiv_pdf)

        if show:
            plt.show()
        else:
            plt.close()


    def show_wfn(self):
        os.system('open ' + self.namer.wfn_pdf)

    def show_logderiv(self):
        os.system('open ' + self.namer.logderiv_pdf)



class DataFile:
    """
    A data file formatted for gnuplot:
    It is a list of N data block each separated by two empty lines,
    refered to by 'index' (from 0 to N-1).
    Lines starting with "#" are ignored.
    """

    def __init__(self, fname=None):

        self.fname = fname

    def set_filename(self, fname):
        """Set the datafile to be treated."""
        self.fname = fname

    def get_data(self, index=0):
        """
        Returns a list of floats contained in a file.
        Lines starting with "#" are ignored
    
        Args:
            index:
                A counter, starting at 0, which  designate a block of data
                separated by two empty lines from the others.
        Returns:
            a list of numpy.ndarray for each column.
        """
        data = list()
        with open(self.fname, 'r') as f:
            nempty = 0
            cindex = 0
            for line in f.readlines():

                if line.lstrip().startswith('#'):
                    continue
                elif not line.split():
                    nempty += 1
                    continue
                elif nempty > 1:
                    cindex += 1
                    nempty = 0

                if cindex == index:
                    parts = line.split()
                    data.append([float(p) for p in parts])
                    continue
                elif cindex > index:
                    break

        newdata = zip(*data)
        newerdata = [np.array(col) for col in newdata]
        return newerdata


def show_wfn(fname):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plot_wfn(fname, ax)
    plt.show()

def plot_wfn(fname, ax, legend=False, legloc='lower right'):

    wfnfile = DataFile(fname)
    with open(fname, 'r') as f:
        line = f.readline()
        parts = line.split()
        l, E = int(parts[2]), float(parts[-1])
        title = "Wfn: l = {l}, E = {E:12.3e} Ry".format(l=l, E=E)
        ax.set_title(title, fontsize=12)

    r, pwave, pspwave, proj = wfnfile.get_data()

    style = dict(marker='', linewidth=2.0)
    ax.plot(r, pwave, label='partial wave', linestyle='-', **style)
    ax.plot(r, pspwave, label='pseudo wave', linestyle='-', **style)
    ax.plot(r, proj, label='projector', linestyle='--', **style)
    if legend:
        ax.legend(loc=legloc)

def plot_logderiv(fname, ax, legend=False, legloc='lower right', title=''):

    file = DataFile(fname)
    E, exact, paw = file.get_data()

    style = dict(marker='', linewidth=2.0)
    ax.plot(E, exact, label='exact', linestyle='-', **style)
    ax.plot(E, paw, label='PAW', linestyle='--', **style)

    if legend:
        ax.legend(loc=legloc)
    ax.set_title(title, fontsize=12)

