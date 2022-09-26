"""Demonstrates molecular dynamics with constant energy."""

from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase import units
from asap3 import Trajectory

def calcenergy(a):  #calculates the epot, ekin, etot and T per atom.
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    T = ekin / (1.5 * units.kB)
    return [epot, ekin, T, epot]

def run_md():
        
    # Use Asap for a huge performance increase if it is installed
    use_asap = True

    if use_asap:
        from asap3 import LennardJones
        size = 6
        epsilon = 0.010323 #eV
        sigma = 3.40 #Å
        cutoff = -1 #Å
        atomic_number = 18
    else:
        from ase.calculators.emt import EMT
        size = 3

    # Set up a crystal
    atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                            symbol="Ar",
                            size=(size, size, size),
                            pbc=True)

    # Describe the interatomic interactions with the Effective Medium Theory
    atoms.calc = LennardJones(
                    [atomic_number], [epsilon], [sigma], 
                    rCut=cutoff, modified=True)

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(atoms, temperature_K=40)

    # We want to run MD with constant energy using the VelocityVerlet algorithm.
    dyn = VelocityVerlet(atoms, 1 * units.fs)  # 1 fs time step.
    traj = Trajectory("argon.traj", "w", atoms)
    dyn.attach(traj.write, interval=100)

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        """Function to print the potential, kinetic and total energy."""
        calc = calcenergy(a)
        print('Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
            'Etot = %.3feV' % (calc[0], calc[1], calc[2] , calc[3]))


    # Now run the dynamics
    dyn.attach(printenergy, interval=100)
    printenergy()
    dyn.run(2000)

if __name__ == "__main__":
    run_md()