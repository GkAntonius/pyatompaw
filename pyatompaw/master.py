
from .namer import AtompawNamer
from .launcher import AtompawLauncher
from .inputfile import AtompawInput
from .plotter import AtompawPlotter
from .util import set_child_functions, set_child_properties

__all__ = ['AtompawMaster']

class AtompawMaster(AtompawNamer):
    """The head."""

    def __init__(self, rootname, *args, **kwargs):

        AtompawNamer.__init__(self, rootname, *args, **kwargs)

        self.launcher = AtompawLauncher(namer=self)
        self.plotter = AtompawPlotter(namer=self)

    def plot_wfn(self, show=False):
        Nproj = self.launcher.inputfile.nproj
        self.plotter.plot_wfn(Nproj, show=show)

    def plot_logderiv(self, show=False):
        Nl = self.launcher.inputfile.lmax + 1
        self.plotter.plot_logderiv(Nl, show=show)

    def make_pseudo_name(self, *args, **kwargs):
        return super(AtompawMaster, self).make_pseudo_name(
            self.Z, self.Atom_name, *args, **kwargs)

    def export(self, directory=None, pseudo_name=None):
        if pseudo_name is None and self.has_default_export_name():
            self.make_pseudo_name()
        self.launcher.export(directory=directory, pseudo_name=pseudo_name)
        

# Link functions and properties
set_child_functions(AtompawMaster, 'plotter', AtompawPlotter)
set_child_functions(AtompawMaster, 'launcher', AtompawLauncher)
set_child_properties(AtompawMaster, 'launcher', AtompawLauncher)
