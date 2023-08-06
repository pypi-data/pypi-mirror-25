from ase import Atoms
from ase.dft.bee import BEEFEnsemble, readbee
from gpaw import GPAW, Mixer
from gpaw.test import equal, gen
from gpaw.mpi import world
import _gpaw

newlibxc = _gpaw.lxcXCFuncNum('MGGA_X_MBEEF') is not None

c = {'energy': 0.001, 'eigenstates': 1, 'density': 1}
d = 0.75

gen('H', xcname='PBEsol')

for xc, E0, dE0 in [('mBEEF', 4.90, 0.17),
                    ('BEEF-vdW', 5.17, 0.19),
                    ('mBEEF-vdW', 4.79, 0.36)]:
    print(xc)
    if not newlibxc and xc[0] == 'm':
        print('Skipped')
        continue

    # H2 molecule:
    h2 = Atoms('H2', [[0, 0, 0], [0, 0, d]])
    h2.center(vacuum=2)
    h2.calc = GPAW(txt='H2-' + xc + '.txt',
                   convergence=c,
                   eigensolver={'name': 'dav', 'niter': 3},
                   mixer=Mixer(0.02, 3))
    h2.get_potential_energy()
    h2.calc.set(xc=xc)
    h2.get_potential_energy()
    h2.get_forces()
    ens = BEEFEnsemble(h2.calc)
    e_h2 = ens.get_ensemble_energies()

    # H atom:
    h = Atoms('H', cell=h2.cell, magmoms=[1])
    h.center()
    h.positions += 0.12345
    h.calc = GPAW(txt='H-' + xc + '.txt',
                  convergence=c,
                  eigensolver={'name': 'dav', 'niter': 3},
                  mixer=Mixer(0.02, 3))
    h.get_potential_energy()
    h.calc.set(xc=xc)
    h.get_potential_energy()
    ens = BEEFEnsemble(h.calc)
    e_h = ens.get_ensemble_energies()

    # binding energy
    ae = 2 * e_h - e_h2
    print(ae.mean(), ae.std())
    print(E0, dE0)
    equal(ae.mean(), E0, 0.02)
    equal(ae.std(), dE0, 0.02)

ens.write('H')
world.barrier()
energies = readbee('H')
equal(abs(energies - e_h).max(), 0, 1e-12)
