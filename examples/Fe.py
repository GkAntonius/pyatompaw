from pyatompaw import AtompawMaster

# Atom definition
atom = AtompawMaster('26-Fe')

atom.launcher.set_executable(executable)

atom.Atom_name = 'Fe'
atom.Z = 26

rpaw   = 2.12 # a.u.
rshape = 1.81

rs = 2.01
rp = 1.81
rd = 2.01


rmax   = 10.0 # a.u.
rmatch = rpaw 

# Keywords
atom.XC_functional      = 'GGA-PBE'

atom.rel_keyword        = 'scalarrelativistic'
atom.grid_keyword       = 'loggrid', 2001, rmax, rmatch
atom.logderivrange      = 'logderivrange', -10., 10., 2001

atom.projector_keyword  = 'custom'

atom.ps_scheme          = 'RRKJ'
#atom.ps_scheme          = 'bloechlps'

atom.ortho_scheme       = 'GramSchmidtOrtho'

# Local part of pseudopotential

atom.Vloc_scheme        = 'ultrasoft'
#atom.Vloc_scheme        = 'bessel'

#atom.Vloc_scheme        = 'trouillermartins'
#atom.lloc               = 2
#atom.Eloc               =-0.5

atom.coreWF_keyword     = 'prtcorewf'
atom.proj_optim_keyword = 'nooptim'
atom.comp_in_XC_keyword = 'usexcnhat'

#atom.output_format = 'abinit'
atom.output_format = 'xml'

# Atom configuration
atom.nmax = [4, 3, 3, 0, 0, 0]  # Maximum occupied orbitals: 4s 3p 3d
#atom.occ = [(3,2,6)]  # 3d has partiall occ: 6

atom.occ = [ (3,2,7),  # 3d has partiall occ: 7
             (4,0,1)]  # 4s has partiall occ: 1


atom.lmax   = 2
atom.rpaw   = rpaw 
atom.rshape = rshape
atom.rvloc  = rshape
atom.rcore  = rshape



# Projectors for valence states
atom.add_valence(n=3, l=0, rc=rs)
atom.add_valence(n=4, l=0, rc=rs)
atom.add_valence(n=3, l=1, rc=rp)
atom.add_valence(n=3, l=2, rc=rd)

# Additional projectors
atom.add_proj(l=1, Eref=3.5, rc=rp)
atom.add_proj(l=2, Eref=2.0, rc=rd)


# Test configurations

atom.configurations = [ [ (3,0,2),
                          (3,1,6),
                          (3,2,6),
                          (4,0,2)],
                         [(3,0,2),
                          (3,1,6),
                          (3,2,8),
                          (4,0,0)]]


# Execution
atom.make()  # Write the files
atom.run()   # Run atompaw

# Plot partial waves and logarithmic derivatives.

atom.plot_wfn()
atom.show_wfn()
atom.plot_logderiv(show=True)

# Export the atomic dataset
atom.export('.')

