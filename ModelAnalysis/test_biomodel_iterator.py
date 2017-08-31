"""
Tests for BiomodelIterator
"""
from biomodel_iterator import BiomodelIterator
from sbml_shim import SBMLShim
import unittest


IGNORE_TEST = False
TEST_FILE = "test_biomodel_iterator.dat"
NUM_IDS = 2


#############################
# Tests for Counter Classes
#############################
class TestBiomodelIterator(unittest.TestCase):

  def testConstructor(self):
    if IGNORE_TEST:
      return
    biter = BiomodelIterator(TEST_FILE)
    self.assertIsNotNone(biter._path)
    self.assertEqual(len(biter._ids), NUM_IDS)

  def testNext(self):
    if IGNORE_TEST:
      return
    biter = BiomodelIterator(TEST_FILE)
    self.assertTrue(all([isinstance(s, SBMLShim) for s in biter]))
    

   

if __name__ == '__main__':
  unittest.main()
