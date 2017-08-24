"""
Tests for simple_sbml
"""
import unittest
import numpy as np
from simple_sbml import SimpleSBML
import libsbml


IGNORE_TEST = False
TEST_FILE = "chemotaxis.xml"
NUM_REACTIONS = 111
NUM_PARAMETERS = 27
MAX_REACTANTS = 10
BIOMODEL = "BIOMD0000000200"


#############################
# Tests
#############################
class TestSimpleSBML(unittest.TestCase):

  def setUp(self):
    self.ssbml = SimpleSBML(filename=TEST_FILE)

  def testConstructorWithFile(self):
    if IGNORE_TEST:
      return
    self.assertEqual(len(self.ssbml.getReactions()), NUM_REACTIONS)
    for reaction in self.ssbml.getReactions():
      self.assertTrue(isinstance(reaction, libsbml.Reaction))
      self.assertLessEqual(reaction.getNumReactants(), MAX_REACTANTS)
    self.assertEqual(len(self.ssbml.getParameters()), NUM_PARAMETERS)
    for parameter in self.ssbml.getParameters():
      self.assertTrue(isinstance(parameter, libsbml.Parameter))

  def testGetSBMLForBiomodel(self):
    if IGNORE_TEST:
      return
    sbmlstr = SimpleSBML.getSBMLForBiomodel(BIOMODEL)
    ssbml = SimpleSBML(sbmlstr=sbmlstr)
    self.assertTrue(len(ssbml.getReactions()) > 0)
    


if __name__ == '__main__':
  unittest.main()
