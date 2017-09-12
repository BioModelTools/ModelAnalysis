"""
Tests for Statistic
"""
import numpy as np
import os
from statistic import Statistic, ModelStatistic, \
    ReactionStatistic, \
    ComplexTransformationReactionStatistic
from sbml_shim import SBMLShim
#from util import createSBML, createReaction
import unittest


IGNORE_TEST = False
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
TEST_FILE = os.path.join(DIRECTORY, "chemotaxis.xml")


class DummyReactionStatistic(ReactionStatistic):

  def _addValues(self, value_dict, idx):
    if "Dummy" not in value_dict:
      value_dict["Dummy"] = [1]
    else:
      value_dict["Dummy"].append(1)
    return value_dict


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
    self.assertTrue("Complex_Disassociation_mean" in statistics)

  def testStatisticError(self):
    shim = SBMLShim.getShimForBiomodel("BIOMD0000000020")
    statistics = Statistic.getAllStatistics(self.shim)
    self.assertTrue(len(statistics.keys()) > 10)


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
    self.assertEqual(result["Dummy_mean"], 1.0)
    self.assertEqual(result["Dummy_std"], 0.0)

  def _testTransformStatistic(self, 
        reactants, products, key, value):
    """
    :param list-of-str reactants:
    :param list-of-str products:
    :param str key: key in the result
    :param float value: value in the result
    """
    sbmlstr = SBMLShim.createSBMLReaction(reactants, products)
    shim = SBMLShim(sbmlstr=sbmlstr)
    complex = ComplexTransformationReactionStatistic(shim)
    self.assertEqual(complex._addValues({}, 0)[key], [value])

  def testComplexDisassociationReactionStatistic(self):
    if IGNORE_TEST:
      return
    key = "Complex_Disassociation"
    self._testTransformStatistic(["AB"], ["B", "A"], key, 1)
    self._testTransformStatistic(["AB"], ["A", "B"], key, 1)
    self._testTransformStatistic(["AB"], ["A", "C"], key, 0)
    self._testTransformStatistic(["AB"], ["A", "C", "B"], key, 1)
    self._testTransformStatistic(["A_B"], ["A", "B"], key, 1)
    self._testTransformStatistic(["A_B"], ["B", "A"], key, 1)
    key = "Complex_Formation"
    self._testTransformStatistic(["A", "B"], ["AB"], key, 1)
    self._testTransformStatistic(["B", "A"], ["AB"], key, 1)
    self._testTransformStatistic(["A", "C"], ["AB"], key, 0)
    self._testTransformStatistic(["A", "C", "B"], ["AB"], key, 1)
    self._testTransformStatistic(["A", "B"], ["A_B"], key, 1)
    self._testTransformStatistic(["B", "A"], ["A_B"], key, 1)

  def testGetDoc(self):
    doc_dict = Statistic.getDoc()
    self.assertTrue("Num_Parameters" in doc_dict)
   

if __name__ == '__main__':
  unittest.main()
