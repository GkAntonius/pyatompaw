
class PseudoID:
    """
    A pseudo identifier.

    Keyword arguments:

        symbol: str
            Atom symbol.
        Z:  int
            Atomic number.
        Zion: int
            Ion charge.
        xc: str
            Exchange-correlation scheme.
        pseudo_type: str
            E.g., 'NC', 'PAW', 'USPP'
        ext: str
            The extension, e.g. 'pawps'.
        id_major: str
            An identifier.
        id_minor: str, int
            An identifier.
        keywords: list
            Keywords to put in the name.
    """

    def __init__(self, **kwargs):
        """
        """

        # Atomic symbol
        self.symbol = str()

        # Atomic number
        self.Z = 0

        # Zion
        self.Zion = 0

        # xc
        self.xc = str()

        # Type of pseudopotential
        self.pseudo_type = str()
        self.ext = str()

        # Ids for the file name
        self.id_major = '00'
        self.id_minor = '0'

        # keywords to put in the names, e.g. 'LDA', '4e'
        self.keywords = list()

        # Initialize values
        self.__dict__.update(kwargs)

        # Set some default values
        if not self.pseudo_type: self.pseudo_type = 'PAW'
        if self.pseudo_type.upper() == 'PAW': self.ext = 'pawps'
        if not self.ext: self.ext = 'pawps'

    def get_minorname(self):
        return self.symbol + str(self.id_minor)

    def get_fname(self):
        fname = '-'.join([str(self.Z), self.symbol])
        fname = '-'.join([fname, str(self.id_major), str(self.id_minor)])
        fname = '_'.join([fname]+ self.keywords)
        fname = '.'.join([fname, self.ext.lstrip('.')])
        return fname


