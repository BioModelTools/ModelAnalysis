"""
Tests for BiomodelIterator
"""
from biomodel_iterator import BiomodelIterator
from sbml_shim import SBMLShim
import os
import unittest


IGNORE_TEST = True
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TEST_FILE = os.path.join(DIRECTORY, "test_biomodel_iterator.dat")
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

  def testNextWithExcludes(self):
    #if IGNORE_TEST:
    #  return
    with open(TEST_FILE) as f:
      first_id = f.readline().replace('\n', '')
    biter = BiomodelIterator(TEST_FILE, excludes=[first_id])
    self.assertEqual(len(biter._ids), NUM_IDS-1)
    

   

if __name__ == '__main__':
  unittest.main()
