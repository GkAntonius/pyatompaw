import subprocess as subp
import os
from os.path import abspath, basename, exists

from .inputfile import AtompawInput
from .namer import AtompawNamer
from .util import set_child_functions, set_child_properties

class AtompawLauncher(object):
    """
    A launcher to run atompaw and moves files.
    """

    _to_parent_functions = ['make', 'run', 'export',
                            ] + AtompawInput._to_parent_functions

    _to_parent_properties = AtompawInput._to_parent_properties

    def __init__(self, rootname=None, namer=None):

        # Initialize the namer with a rootname.
        if rootname:
            self.namer = AtompawNamer(rootname)
        elif namer and isinstance(namer, AtompawNamer):
            self.namer = namer
        else:
            self.namer = AtompawNamer()

        self.inputfile = AtompawInput(fname=self.namer.inputname)

    def set_input(self, string):
        self.inputfile.content = string.strip() + '\n'

    def make(self):
        """Make the files."""
        if not exists(self.namer.dirname):
            os.makedirs(self.namer.dirname)
        self.inputfile.write()

    def run(self):
        """Run atompaw."""
        exdir = abspath(os.curdir)
        os.chdir(self.namer.dirname)
        command = ' '.join(['atompaw', '<', basename(self.namer.inputname)])
        print command
        os.system(command)
        os.chdir(exdir)

    def export(self, directory=None, pseudo_name=None):
        """
        Copy the pseudopotential to an external directory.

        WARNING: will overwrite an existing file.
        """

        if pseudo_name is not None:
            self.namer.export_name = pseudo_name

        if directory is not None:
            self.namer.export_directory = directory

        source = self.namer.find_abinit_output()
        dest = self.namer.export_name

        subp.call(['cp', source, dest])


# Link functions and properties
set_child_functions(AtompawLauncher, 'inputfile', AtompawInput)
set_child_properties(AtompawLauncher, 'inputfile', AtompawInput)

