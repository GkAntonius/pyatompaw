from pyatompaw import AtompawMaster

# Atom definition
atom = AtompawMaster('34-Se')
atom.Atom_name = 'Se'
atom.Z = 34

# Keywords
atom.XC_functional = 'LDA-PW'
atom.rel_keyword = 'scalarrelativistic'
atom.grid_keyword = 'loggrid', 2001, 80.0, 2.4
atom.logderivrange = 'logderivrange', -10, 35, 201
atom.projector_keyword = 'custom'
atom.ps_scheme = 'bloechlps'
atom.ortho_scheme = 'gramschmidtortho'
atom.shapefunction = 'besselshape'
atom.Vloc_scheme = 'bessel'
atom.output_format = 'abinit'
atom.comp_in_XC_keyword = ''

# Atom configuration
atom.nmax = [4, 4, 3, 0, 0, 0]
atom.occ = [(4,1,4)]
atom.lmax = 2
atom.rpaw = 2.1

# Projectors for valence states
atom.add_valence(n=3, l=0, rc=atom.rpaw)
atom.add_valence(n=4, l=0, rc=atom.rpaw)
atom.add_valence(n=4, l=1, rc=atom.rpaw)
atom.add_valence(n=3, l=2, rc=atom.rpaw)

# Additional projectors
atom.add_proj(l=0, Eref=5.0, rc=atom.rpaw)
atom.add_proj(l=1, Eref=7.0, rc=atom.rpaw)
atom.add_proj(l=2, Eref=3.0, rc=atom.rpaw)

# Write the files
atom.make()

# Run atompaw
atom.run()

# Export atom pseudo
atom.make_pseudo_name(keywords=(atom.XC_functional))
atom.export(directory='./')

# Plot projectors and log derivatives
atom.plot_wfn()
atom.show_wfn()
atom.plot_logderiv(show=True)

