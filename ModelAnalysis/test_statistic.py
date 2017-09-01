"""
Tests for Statistic
"""
import numpy as np
import os
from statistic import Statistic,  \
    ReactionStatistic, \
    ComplexFormationReactionStatistic, \
    ComplexDisassociationReactionStatistic
from sbml_shim import SBMLShim
#from util import createSBML, createReaction
import unittest


IGNORE_TEST = False
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TEST_FILE = os.path.join(DIRECTORY, "chemotaxis.xml")


class DummyReactionStatistic(ReactionStatistic):

  def _getValue(self, idx):
    return 1
  
  def _getName(self):
    return "Dummy"


class TestClass(object):
  pass
class TestSubclassA(TestClass):
  pass
class TestSubclassB(TestClass):
  pass
class TestSubclassC(TestSubclassA):
  pass
LEAF_SUBCLASSES = set([TestSubclassB, TestSubclassC])


#############################
# Statistic
#############################
class TestStatistic(unittest.TestCase):

  def setUp(self):
    self.shim = SBMLShim(filepath=TEST_FILE)
    
  def testConstructor(self):
    if IGNORE_TEST:
      return
    statistic = Statistic(self.shim)
    self.assertIsNotNone(statistic._shim)

  def _testJointSubstring(self, substrings, string, expected):
    result = Statistic._jointSubstring(substrings, string)
    self.assertEqual(result, expected)
    substrings.reverse()
    result = Statistic._jointSubstring(substrings, string)
    self.assertEqual(result, expected)

  def testJointSubstring(self):
    if IGNORE_TEST:
      return
    self._testJointSubstring(["xx", "yy"], "xx_yy", 2)
    self._testJointSubstring(["xxy", "y"], "xx_yy", 1)
    self._testJointSubstring(["xx", "yy", "zz"], "zzz_xx_yy", 3)

  def testFindLeafSubclasses(self):
    leaves = Statistic._findLeafSubclasses(TestClass)
    self.assertEqual(leaves, LEAF_SUBCLASSES)

  def testGetAllStatistics(self):
    statistics = Statistic.getAllStatistics(self.shim)
    self.assertTrue(len(statistics.values()) > 0)


#############################
# Reaction Statistics
#############################
class TestReactionStatistic(unittest.TestCase):

  def setUp(self):
    self.shim = SBMLShim(filepath=TEST_FILE)

  def testgetStatistic(self):
    if IGNORE_TEST:
      return
    reaction_statistic = DummyReactionStatistic(self.shim)
    result = reaction_statistic.getStatistic()
    self.assertEqual(result.values(), [1.0, 0.0])

  def _testFormationStatistic(self, 
        reactants, products, expected_result):
    shimstr = SBMLShim.createSBMLReaction(reactants, products)
    shim = SBMLShim(sbmlstr=shimstr)
    complex = ComplexFormationReactionStatistic(shim)
    self.assertEqual(complex._getValue(0), expected_result)

  def testComplexFormationReactionStatistic(self):
    if IGNORE_TEST:
      return
    self._testFormationStatistic(["A", "B"], ["AB"], 1)
    self._testFormationStatistic(["B", "A"], ["AB"], 1)
    self._testFormationStatistic(["A", "C"], ["AB"], 0)
    self._testFormationStatistic(["A", "C", "B"], ["AB"], 1)
    self._testFormationStatistic(["A", "B"], ["A_B"], 1)
    self._testFormationStatistic(["B", "A"], ["A_B"], 1)

  def _testDisassociateStatistic(self, 
        reactants, products, expected_result):
    shimstr = SBMLShim.createSBMLReaction(reactants, products)
    shim = SBMLShim(sbmlstr=shimstr)
    complex = ComplexDisassociationReactionStatistic(shim)
    self.assertEqual(complex._getValue(0), expected_result)

  def testComplexDisassociationReactionStatistic(self):
    if IGNORE_TEST:
      return
    self._testDisassociateStatistic(["AB"], ["B", "A"], 1)
    self._testDisassociateStatistic(["AB"], ["A", "B"], 1)
    self._testDisassociateStatistic(["AB"], ["A", "C"], 0)
    self._testDisassociateStatistic(["AB"], ["A", "C", "B"], 1)
    self._testDisassociateStatistic(["A_B"], ["A", "B"], 1)
    self._testDisassociateStatistic(["A_B"], ["B", "A"], 1)
   

if __name__ == '__main__':
  unittest.main()
