
A python interface to the software atompaw.


Installing pyatompaw
====================

Requirements
------------

1. python 2.7 (or later)

2. numpy 1.1 (or later)

3. matplotlib 

4. atompaw


Installing from source
----------------------

::
    python setup.py build
    python setup.py install


Example usage
=============

.. code-block:: python

    from pyatompaw import AtompawMaster
    
    # Atom definition
    atom = AtompawMaster('14-Si')
    atom.Atom_name = 'Si'
    atom.Z = 14
    
    # Keywords
    atom.XC_functional = 'LDA-PW'
    atom.projector_keyword = 'custom'
    atom.logderivrange = 'logderivrange', -6, 10, 2001
    atom.ps_scheme = 'rrjk'
    atom.ortho_scheme = 'gramschmidtortho'
    atom.Vloc_scheme = 'trouillermartins'
    atom.lloc = 2
    atom.Eloc = 0.5
    atom.output_format = 'abinit'
    
    # Atom configuration
    atom.nmax = [3, 3, 0, 0, 0, 0]  # Maximum occupied orbitals: 3s 3p
    atom.occ = [(3,1,2)]  # 3p has partiall occ: 2
    atom.lmax = 2
    atom.rpaw = 1.6
    
    # Projectors for valence states
    atom.add_valence(n=3, l=0, rc=atom.rpaw)
    atom.add_valence(n=3, l=1, rc=atom.rpaw)
    
    # Additional projectors
    atom.add_proj(l=0, Eref=12.0, rc=atom.rpaw)
    atom.add_proj(l=1, Eref=12.0, rc=atom.rpaw)
    atom.add_proj(l=2, Eref=5.0, rc=atom.rpaw)
    
    # Execution
    atom.make()  # Write the files
    atom.run()   # Run atompaw
    
    # Plot partial waves and logarithmic derivatives.
    atom.plot_wfn()
    atom.show_wfn()
    atom.plot_logderiv(show=True)
    
    # Export the atomic dataset
    atom.export('.')


License
=======

pyatompaw is released under the GNU GPL License.

