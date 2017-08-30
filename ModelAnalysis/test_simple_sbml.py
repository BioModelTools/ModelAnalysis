"""
Tests for simple_sbml
"""
import unittest
import numpy as np
from simple_sbml import SimpleSBML
import libsbml


IGNORE_TEST = True
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
    self.ssbml = SimpleSBML(filepath=TEST_FILE)

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

  def testcreateSBML(self):
    if IGNORE_TEST:
      return
    sbmlstr = SimpleSBML.createSBML("A + B -> C; 1")
    ssbml = SimpleSBML(sbmlstr=sbmlstr)
    reaction = ssbml.getReactions()[0]
    reactants = set([r.getSpecies() for r in
       ssbml.getReactants(reaction)])
    self.assertEqual(reactants, set(["A", "B"]))
    self.assertEqual(ssbml.getProducts(reaction)[0].getSpecies(), 
        "C")

  def testCreateReaction(self):
    if IGNORE_TEST:
      return
    reactants = ["A"]
    products = ["B", "C"]
    sbmlstr = SimpleSBML.createSBMLReaction(reactants, products)
    ssbml = SimpleSBML(sbmlstr=sbmlstr)
    self.assertTrue(len(ssbml.getReactants(0)), len(reactants))
    self.assertTrue(len(ssbml.getProducts(0)), len(products))

  def testGetReactionIndicies(self):
    antimonystr = '''
    A -> B; 1
    C -> D; 1
    A = 1
    B = 1
    C = 1
    D =1
    '''
    sbmlstr = SimpleSBML.createSBML(antimonystr)
    ssbml = SimpleSBML(sbmlstr=sbmlstr)
    reaction_indicies = ssbml.getReactionIndicies()
    self.assertEqual(len(reaction_indicies), 2)


if __name__ == '__main__':
  unittest.main()
