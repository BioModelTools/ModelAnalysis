"""
Tests for PatternCounter
"""
import numpy as np
from pattern_counter import PatternCounter, ReactionPatternCounter,  \
    ComplexFormationReactionPattern, ComplexDisassociationReactionPattern
from sbml_shim import SBMLShim
#from util import createSBML, createReaction
import unittest


IGNORE_TEST = False
TEST_FILE = "chemotaxis.xml"


class DummyReactionPattern(ReactionPatternCounter):
  def isPattern(self, idx):
    return True


#############################
# Tests for Counter Classes
#############################
class TestCounterClasses(unittest.TestCase):

  def setUp(self):
    self.shim = SBMLShim(filepath=TEST_FILE)
    
  def testPatternCounter(self):
    if IGNORE_TEST:
      return
    counter = DummyReactionPattern(self.shim)
    self.assertIsNotNone(counter._shim)

  def testReactionPatternCounter(self):
    if IGNORE_TEST:
      return
    counter = DummyReactionPattern(self.shim)
    reaction_count, pattern_count = counter.run()
    self.assertEqual(reaction_count, pattern_count)

#############################
# Tests for Pattern Classes
#############################
class TestPatterns(unittest.TestCase):

  def setUp(self):
    self.shim = SBMLShim(filepath=TEST_FILE)

  def _testJointSubstring(self, substrings, string, expected):
    result = PatternCounter._jointSubstring(substrings, string)
    self.assertEqual(result, expected)
    substrings.reverse()
    result = PatternCounter._jointSubstring(substrings, string)
    self.assertEqual(result, expected)

  def testJointSubstring(self):
    if IGNORE_TEST:
      return
    self._testJointSubstring(["xx", "yy"], "xx_yy", 2)
    self._testJointSubstring(["xxy", "y"], "xx_yy", 1)
    self._testJointSubstring(["xx", "yy", "zz"], "zzz_xx_yy", 3)

  def _testFormationPattern(self, 
        reactants, products, expected_result):
    shimstr = SBMLShim.createSBMLReaction(reactants, products)
    shim = SBMLShim(sbmlstr=shimstr)
    complex = ComplexFormationReactionPattern(shim)
    self.assertEqual(complex.isPattern(0), expected_result)

  def testComplexFormationReactionPattern(self):
    if IGNORE_TEST:
      return
    self._testFormationPattern(["A", "B"], ["AB"], True)
    self._testFormationPattern(["B", "A"], ["AB"], True)
    self._testFormationPattern(["A", "C"], ["AB"], False)
    self._testFormationPattern(["A", "C", "B"], ["AB"], True)
    self._testFormationPattern(["A", "B"], ["A_B"], True)
    self._testFormationPattern(["B", "A"], ["A_B"], True)

  def _testDisassociatePattern(self, 
        reactants, products, expected_result):
    shimstr = SBMLShim.createSBMLReaction(reactants, products)
    shim = SBMLShim(sbmlstr=shimstr)
    complex = ComplexDisassociationReactionPattern(shim)
    self.assertEqual(complex.isPattern(0), expected_result)

  def testComplexDisassociationReactionPattern(self):
    if IGNORE_TEST:
      return
    self._testDisassociatePattern(["AB"], ["B", "A"], True)
    self._testDisassociatePattern(["AB"], ["A", "B"], True)
    self._testDisassociatePattern(["AB"], ["A", "C"], False)
    self._testDisassociatePattern(["AB"], ["A", "C", "B"], True)
    self._testDisassociatePattern(["A_B"], ["A", "B"], True)
    self._testDisassociatePattern(["A_B"], ["B", "A"], True)
   

if __name__ == '__main__':
  unittest.main()
