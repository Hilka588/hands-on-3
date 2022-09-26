import sys, unittest
from ase.lattice.cubic import FaceCenteredCubic
from asap3 import LennardJones
from md import calcenergy

class MdTests(unittest.TestCase):

    def test_calcenergy(self):

        atoms = FaceCenteredCubic(directions=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                            symbol="Ar",
                            size=(6, 6, 6),
                            pbc=True)

        atoms.calc = LennardJones(
                    [18], [0.010323], [3.40], 
                    rCut=-1, modified=True)
        
        boolean = False
        if calcenergy(atoms) == [-0.08194238731586774, 0.0, 0.0, -0.08194238731586774]:
            boolean = True

        self.assertTrue(boolean)

if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(MdTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
