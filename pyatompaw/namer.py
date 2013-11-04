
import os
from os.path import basename, dirname, join, splitext

_default_export_name = 'pseudo.pawps'

class AtompawNamer(object):
    """A namer for AtomPAW"""
    # The Namer object can NOT have a 'fname' property.

    _rootname = 'Atom/root'
    _export_name = _default_export_name
    export_directory = '.'

    _to_master_functions = ['make_pseudo_name']

    def __init__(self, rootname='Atom/root', export_name='pseudo.pawps',
                 export_directory='.'):

        self.rootname = rootname

        self.export_directory = export_directory
        self.export_name = export_name

    @property
    def export_name(self):
        return join(self.export_directory, self._export_name)

    @export_name.setter
    def export_name(self, name):
        if basename(name) != name:
            self.export_directory = dirname(name)
        self._export_name = basename(name)

    def has_default_export_name(self):
        return basename(self.export_name) == _default_export_name

    @property
    def rootname(self):
        """The root to form all names."""
        return self._rootname

    @rootname.setter
    def rootname(self, name):
        """Set the root name."""

        # Take split extension
        if '.' in basename(name):
            name = splitext(name)[0]

        # The calculation must be in a directory.
        if name == basename(name):
            name = join(name, name)

        self._rootname = name

    @property
    def dirname(self):
        """The top-level directory."""
        return dirname(self.rootname)

    @property
    def basename(self):
        """The basename of the root name."""
        return basename(self.rootname)

    @property
    def inputname(self):
        """The top-level directory."""
        return self.rootname + '.in'

    @property
    def wfn_pdf(self):
        return join(self.dirname, 'wfn.pdf')

    @property
    def logderiv_pdf(self):
        return join(self.dirname, 'logderiv.pdf')

    def wfn(self, i):
        """
        Name of a wavefunction file
        containing radius, partial wave, pseudo-partial wave, and projector.
        """
        return join(self.dirname, 'wfn' + str(i))

    def logderiv(self, i):
        """Name of a log derivative file."""
        return join(self.dirname, 'logderiv.' + str(i))

    def tprod(self, i):
        """Name of a tprod file containing q, q**2 * p(q) * phitw(q)"""
        return join(self.dirname, 'tprod.' + str(i))

    def find_abinit_output(self):
        """
        Find the paw file output for abinit.

        Raises:
            LookupError
        """
        for fname in os.listdir(self.dirname):
            if fname.endswith('paw.abinit'):
                return join(self.dirname, fname)
        raise LookupError('No abinit output found.')

    def make_pseudo_name(self, Z, symbol, keywords='', extension='pawps',
                         directory=None):
        """
        Make a name for a pseudopotential file.
        """
        if not '__iter__' in dir(keywords):
            keywords = [keywords]
        keywords = [str(kw) for kw in keywords]

        fname = '-'.join([str(Z), symbol])
        if len(keywords) >= 1 and keywords[0]:
            fname = '_'.join([fname]+keywords)
        fname += '.' + extension.lstrip('.')
        if directory is None:
            directory = self.export_directory    
        fname = join(directory, fname)

        self.export_name = fname

        return fname

    
