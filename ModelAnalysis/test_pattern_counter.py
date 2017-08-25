"""
Tests for PatternCounter
"""
import unittest
import numpy as np
from pattern_counter import PatternCounter, ReactionPatternCounter,  \
    ModelPattern, ReactionPattern, ComplexFormationReactionPattern,  \
    ComplexDisassociationReactionPattern
from simple_sbml import SimpleSBML


IGNORE_TEST = False
TEST_FILE = "chemotaxis.xml"


class DummyReactionPattern(ReactionPattern):
  def isPattern(self):
    return True


#############################
# Tests for Counter Classes
#############################
class TestCounterClasses(unittest.TestCase):

  def setUp(self):
    self.ssbml = SimpleSBML(filepath=TEST_FILE)
    
  def testPatternCounter(self):
    if IGNORE_TEST:
      return
    counter = PatternCounter(self.ssbml, ModelPattern)
    self.assertEqual(counter._pattern_cls,ModelPattern)

  def testReactionPatternCounter(self):
    if IGNORE_TEST:
      return
    counter = ReactionPatternCounter(self.ssbml, DummyReactionPattern)
    reaction_count, pattern_count = counter.run()
    self.assertEqual(reaction_count, pattern_count)

#############################
# Tests for Pattern Classes
#############################
class TestPatterns(unittest.TestCase):

  def setUp(self):
    self.ssbml = SimpleSBML(filepath=TEST_FILE)

  def _testJointSubstring(self, substrings, string, expected):
    result = ModelPattern._jointSubstring(substrings, string)
    self.assertEqual(result, expected)
    substrings.reverse()
    result = ModelPattern._jointSubstring(substrings, string)
    self.assertEqual(result, expected)

  def testJointSubstring(self):
    self._testJointSubstring(["xx", "yy"], "xx_yy", 2)
    self._testJointSubstring(["xxy", "y"], "xx_yy", 1)
    self._testJointSubstring(["xx", "yy", "zz"], "zzz_xx_yy", 3)
   


if __name__ == '__main__':
  unittest.main()
