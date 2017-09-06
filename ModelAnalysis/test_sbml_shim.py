"""
Tests for sbml_shim
"""
import unittest
import numpy as np
import os
from sbml_shim import SBMLShim
import libsbml


IGNORE_TEST = False
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TEST_FILE = os.path.join(DIRECTORY, "chemotaxis.xml")
NUM_REACTIONS = 111
NUM_PARAMETERS = 27
MAX_REACTANTS = 10
BIOMODEL = "BIOMD0000000200"


#############################
# Tests
#############################
class TestSBMLShim(unittest.TestCase):

  def setUp(self):
    self.shim = SBMLShim(filepath=TEST_FILE)

  def testConstructorWithFile(self):
    if IGNORE_TEST:
      return
    self.assertEqual(len(self.shim.getReactions()), NUM_REACTIONS)
    for reaction in self.shim.getReactions():
      self.assertTrue(isinstance(reaction, libsbml.Reaction))
      self.assertLessEqual(reaction.getNumReactants(), MAX_REACTANTS)
    self.assertEqual(len(self.shim.getParameters()), NUM_PARAMETERS)
    for parameter in self.shim.getParameters():
      self.assertTrue(isinstance(parameter, libsbml.Parameter))

  def testConstructorWithError(self):
    if IGNORE_TEST:
      return
    shim = SBMLShim(sbmlstr="", is_ignore_errors=True)
    self.assertIsNone(shim._exception)
    with self.assertRaises(Exception):
      SBMLShim(sbmlstr="")

  def testGetShimForBiomodel(self):
    if IGNORE_TEST:
      return
    shim = SBMLShim.getShimForBiomodel(BIOMODEL)
    self.assertTrue(len(shim.getReactions()) > 0)
    self.assertEqual(shim.getBiomodelId(), BIOMODEL)

  def testcreateSBML(self):
    if IGNORE_TEST:
      return
    sbmlstr = SBMLShim.createSBML("A + B -> C; 1")
    shim = SBMLShim(sbmlstr=sbmlstr)
    reaction = shim.getReactions()[0]
    reactants = set([r.getSpecies() for r in
       shim.getReactants(reaction)])
    self.assertEqual(reactants, set(["A", "B"]))
    self.assertEqual(shim.getProducts(reaction)[0].getSpecies(), 
        "C")

  def testCreateReaction(self):
    if IGNORE_TEST:
      return
    reactants = ["A"]
    products = ["B", "C"]
    sbmlstr = SBMLShim.createSBMLReaction(reactants, products)
    shim = SBMLShim(sbmlstr=sbmlstr)
    self.assertTrue(len(shim.getReactants(0)), len(reactants))
    self.assertTrue(len(shim.getProducts(0)), len(products))

  def testGetReactionIndicies(self):
    antimonystr = '''
    A -> B; 1
    C -> D; 1
    A = 1
    B = 1
    C = 1
    D =1
    '''
    sbmlstr = SBMLShim.createSBML(antimonystr)
    shim = SBMLShim(sbmlstr=sbmlstr)
    reaction_indicies = shim.getReactionIndicies()
    self.assertEqual(len(reaction_indicies), 2)

  def testExecFunction(self):
    num_errors = self.shim.execFunction("getNumErrors")
    self.assertEqual(num_errors, 0)
    num_params = self.shim.execFunction("getNumParameters",
        attribute="model")
    self.assertGreater(num_params, 0)


if __name__ == '__main__':
  unittest.main()
