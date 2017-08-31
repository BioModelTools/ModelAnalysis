"""
Tests for BiomodelsIterator
"""
from biomodels_iterator import BiomodelsIterator
from sbml_shim import SBMLShim
import unittest


IGNORE_TEST = False
TEST_FILE = "test_biomodels_iterator.dat"
NUM_IDS = 2


#############################
# Tests for Counter Classes
#############################
class TestBiomodelsIterator(unittest.TestCase):

  def testConstructor(self):
    if IGNORE_TEST:
      return
    biter = BiomodelsIterator(TEST_FILE)
    self.assertIsNotNone(biter._path)
    self.assertEqual(len(biter._ids), NUM_IDS)

  def testNext(self):
    if IGNORE_TEST:
      return
    biter = BiomodelsIterator(TEST_FILE)
    self.assertTrue(all([isinstance(s, SBMLShim) for s in biter]))

  def testGetId(self):
    if IGNORE_TEST:
      return
    biter = BiomodelsIterator(TEST_FILE)
    shim = biter.next()
    self.assertEqual(biter.getId(), 'BIOMD0000000001')
    shim = biter.next()
    self.assertEqual(biter.getId(), 'BIOMD0000000002')
    
    

   

if __name__ == '__main__':
  unittest.main()
