"""
Tests for PatternCounter
"""
import unittest
import numpy as np
from pattern_counter import PatternCounter, ReactionPatternCounter,  \
    ModelPattern, ReactionPattern, ComplexFormationReactionPattern,  \
    ComplexDisassociationReactionPattern


IGNORE_TEST = False


#############################
# Tests
#############################
class TestPatternCounter(unittest.TestCase):

  def setUp(self):
    pass

  def testConstructor(self):
    if IGNORE_TEST:
      return


if __name__ == '__main__':
  unittest.main()
