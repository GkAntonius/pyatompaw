
class AtompawInput(object):
    """
    An input for atompaw-3.0.

    Keyword arguments
    -----------------

    Atom_name: str
        Atomic symbol.

    Z: int
        Atomic number

    XC_functional: str

    rel_keyword: str

    nucleus_keyword: list

    grid_keyword: list

    logderivrange: list

    nmax: list (5)
        The maximum quantum number 'n' for l=0,4.

    occ: 2d list (N, 3)
        (n, l, occ_nl) for each N empty or partially occupied state.

    lmax: int

    rpaw: float

    rshape: float

    rvloc: float

    rcore: float

    projector_keyword: str

    ps_scheme: str

    ortho_scheme: str

    shapefunction: str

    lloc: int

    Eloc: float

    Vloc_scheme: str

    configurations: 3d list (Ntests, N, 3)
        Configurations for tests.
        for each Ntests:
            for each empty or partially occupied nl state:
                (n, l, occ_nl)
 
    output_format: int or str
        Choices:
            2, 'abinit'
            3, 'pwscf'
            4, 'xml'

    coreWF_keyword: str

    proj_optim_keyword: str

    comp_in_XC_keyword: str

    reduced_grid_keyword: str

    upf_grid_keywords: str


    """

    _to_parent_properties = [
        'Atom_name',
        'Z',
        'XC_functional',
        'rel_keyword',
        'nucleus_keyword',
        'grid_keyword',
        'logderivrange',
        'nmax',
        'occ',
        'lmax',
        'rpaw',
        'rshape',
        'rvloc',
        'output_format',
        'rcore',
        'projector_keyword',
        'ps_scheme',
        'ortho_scheme',
        'shapefunction',
        'lloc',
        'Eloc',
        'Vloc_scheme',
        'configurations',
        'coreWF_keyword',
        'proj_optim_keyword',
        'comp_in_XC_keyword',
        'reduced_grid_keyword',
        'upf_grid_keywords',
        'nproj',
        'lmax',
        'partition',
        ]

    _to_parent_functions = [
        'add_valence',
        'add_projector',
        'add_proj',
        ]

    def __init__(self, fname='atompaw.in', **kwargs):

        # Big string containing the input
        self.content = str()

        # Name of the input file
        self.fname = str(fname)

        # ==== Input content == #

        # First line
        self.Atom_name = str()
        self.Z = int()

        # Second line
        self.XC_functional = str()
        self.rel_keyword = str()
        self.nucleus_keyword = list()
        self.grid_keyword = list()
        self.logderivrange = list()

        # Third line
        self._nmax = list()

        # Partial occupations
        self.occ = list()

        # Core-valence partitioning
        self._partition_1d = list()
        self._nval = list()
        self._val_n = list()

        # l max
        self._lmax = int()

        # various cut-off radii
        self.rpaw = float()
        self.rshape = float()
        self.rvloc = float()
        self.rcore = float()

        # Additional projectors energies
        self._Eref  = list()

        # ps scheme
        self.projector_keyword = str()
        self.ps_scheme = str()
        self.ortho_scheme = str()
        self.shapefunction = str()

        # Vloc_scheme
        self.lloc = int()
        self.Eloc = float()
        self.Vloc_scheme = str()

        # matching radii
        #self.rc = list()
        self._rc_val = list()
        self._rc_add = list()

        # test configurations
        self.configurations = list()

        # Output format
        self.output_format = 'abinit'

        # Abinit output keywords
        self.coreWF_keyword = str()
        self.proj_optim_keyword = str()
        self.comp_in_XC_keyword = str()
        self.reduced_grid_keyword = str()

        # PWscf keywords
        self.upf_grid_keywords = str()


        # Set attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def nmax(self):
        return self._nmax

    @nmax.setter
    def nmax(self, value):
        assert isinstance(value, list)
        self._nmax = value
        self._nval = list()
        self._val_n = list()
        for nl in value:
            if nl == 0:
                break
            self._nval.append(0)
            self._val_n.append(list())
            self._rc_val.append(list())

    @property
    def lmax(self):
        return self._lmax

    @lmax.setter
    def lmax(self, value):
        assert isinstance(value, int)
        self._lmax = value
        self._Eref = [ list() for i in range(value+1) ]
        self._rc_add = [ list() for i in range(value+1) ]

    @property
    def nval(self):
        """Number of valence state for each angular momentum."""
        return self._nval

    @nval.setter
    def nval(self, value):
        self._nval = value

    @property
    def Eref(self):
        return self._Eref

    @property
    def rc(self):
        rc = list()
        for l in range(self.lmax+1):
            rc.append(list())
            if len(self._rc_val) > l:
                rn = zip(self._rc_val[l], self._val_n[l])
                rn = sorted(rn, cmp=lambda x,y: cmp(x[1],y[1]))

                if rn != []:
                    # It is possible that the user will not define any valence state for a channel;
                    # only add a core value if there is a valence state. 
                    rc_val, ns = zip(*rn)
                    rc[l].extend(rc_val)
            rc[l].extend(self._rc_add[l])
        return rc

    @property
    def nproj(self):
        """
        The number of projector for each angular momentum.

        Returns:
            list (lmax+1)
                Ns, Np, Nd, Nf, ...
        """
        return [ len(rcl) for rcl in self.rc ]
        #nproj = self.lmax * [0]

        ## Count number of valence states
        #for l, nval in enumerate(self.nval):
        #    nproj[l] += nval

        ## Cound additional projectors
        #for l, Erefs in enumerate(self.Eref):
        #    nproj[l] += len(Erefs)

        #return nproj

    @property
    def partition(self):
        assert self.nmax, 'nmax is not set, can not return partition.'
        partition_2d = list()
        for l, (nmax, nval) in enumerate(zip(self.nmax, self.nval)):
            ncore = nmax - l - nval
            partition_2d.append(ncore * ['c'] + nval * ['v'])
        return partition_2d

    #@property
    #def partition(self):
    #    assert self.nmax, 'nmax is not set, can not return partition.'
    #    partition_2d = list()
    #    istart = 0
    #    iend = 0
    #    for l, nmax in enumerate(self.nmax):
    #        if nmax == 0:
    #            partition_2d.append(list())
    #            continue
    #        iend += nmax - l
    #        partition_2d.append(self._partition_1d[istart:iend])
    #        istart = iend
    #    return partition_2d

    #@partition.setter
    #def partition(self, value):
    #    assert value
    #    assert isinstance(value, list)
    #    if isinstance(value[0], list):
    #        self._partition_1d = sum(value, [])
    #    else:
    #        self._partition_1d = value

    #    assert all(pi in ('c', 'v') for pi in self._partition_1d)
        
    def add_valence(self, n, l, rc=0.0):
        assert self.nmax, "nmax not set."
        self.nval[l] += 1
        self._val_n[l].append(n)
        nmax = self.nmax[l]
        nval = self.nval[l]
        if not rc: rc = self.rpaw
        self._rc_val[l].append(rc)

    def add_projector(self, l, Eref, rc=0.0):
        """Add a projector."""
        missing = l+1 - len(self.Eref)
        if missing > 0:
            for i in range(missing):
                self.Eref.append(list())

        self.Eref[l].append(Eref)
        if not rc: rc = self.rpaw
        self._rc_add[l].append(rc)

    def add_proj(self, *args, **kwargs):
        """Alias for add_projector."""
        return self.add_projector(*args, **kwargs)

    def make_content(self):
        """Create a string with the content of the input file."""

        self.content = ""

        def add(line):
            self.content += line

        def add_keyword(line, keyword):
            if not keyword:
                pass
            elif (isinstance(keyword, str) or
                  isinstance(keyword, int) or
                  isinstance(keyword, float)):
                line = line.rstrip() + ' ' + str(keyword)
            elif isinstance(keyword, list) or isinstance(keyword, tuple):
                for kw in keyword:
                    line = line.rstrip() + ' ' + str(kw)
            return line.lstrip()

        # Atom identification
        line = ' '.join([self.Atom_name, str(self.Z)])
        add(line + '\n')

        # various keywords
        assert self.XC_functional, "XC_functional not set."
        line = ''
        for kw in (self.XC_functional, self.rel_keyword, self.nucleus_keyword,
                   self.grid_keyword, self.logderivrange):
            line = add_keyword(line, kw)
        add(line + '\n')

        # Ns
        line = ' '.join([str(n) for n in self.nmax])
        add(line + '\n')

        # occs
        for occnl in self.occ:
            line = ' '.join([str(i) for i in occnl])
            add(line + '\n')
        add('0 0 0\n')

        # core-valence partition
        for nl in self.partition:
            for partition in nl:
                add(str(partition) + '\n')

        # lmax
        add(str(self.lmax) + '\n')

        # radii
        line = str(self.rpaw)
        for r in (self.rshape, self.rvloc, self.rcore):
            if r: line += ' ' + str(r)
        add(line + '\n')

        # additional projectors
        assert len(self.Eref) == self.lmax+1, "Eref and lmax don't comply."
        for l in range(self.lmax+1):
            for Eref in self.Eref[l]:
                add('y\n{}\n'.format(Eref))
            add('n\n')

        # projector keywords
        assert self.projector_keyword, "projector_keyword not set."
        line = ''
        for kw in (self.projector_keyword, self.ps_scheme,
                   self.ortho_scheme, self.shapefunction):
            line = add_keyword(line, kw)
        add(line + '\n')

        # Vloc scheme
        if self.Vloc_scheme.lower() == 'bessel':
            line = ''
        else:
            line = str(self.lloc) + ' ' + str(self.Eloc) + ' '
        line += self.Vloc_scheme
        add(line + '\n')

        # rc
        assert len(self.rc) == self.lmax+1, "rc and lmax don't comply."
        if self.projector_keyword.lower() != 'bloechl':
            for l in range(self.lmax+1):
                for rc in self.rc[l]:
                    add(str(rc) + '\n')

        # Test configuration
        for test in self.configurations:
            add('1\n')
            for state in test:
                line = ' '.join([str(i) for i in state])
                add(line + '\n')
            add('0 0 0\n')

        # Output format
        if str(self.output_format).lower() in ('2', 'abinit'):
            add('2\n')
            line = ''

            for kw in (self.coreWF_keyword, self.proj_optim_keyword,
                       self.comp_in_XC_keyword, self.reduced_grid_keyword):
                line = add_keyword(line, kw)
            if line:
                add(line + '\n')
        elif str(self.output_format).lower() in ('3', 'pwscf'):
            add('3\n')
            line = ''
            for kw in (self.upf_grid_keywords,):
                line = add_keyword(line, kw)
            if line:
                add(line + '\n')
        elif str(self.output_format).lower() in ('4', 'xml'):
            add('4\n')
            line = ''
            for kw in (self.coreWF_keyword, self.proj_optim_keyword,
                       self.comp_in_XC_keyword, self.reduced_grid_keyword):
                line = add_keyword(line, kw)
            if line:
                add(line + '\n')

        else:
            raise ValueError("Output format not recognized")
                
        # End of the file
        add('0')

    def write(self):

        if not self.content:
            self.make_content()

        with open(self.fname, 'w') as f:
            f.write(self.content)

