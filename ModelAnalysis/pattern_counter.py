"""
Classes that count patterns in SBML models
"""
from simple_sbml import SimpleSbml
import sys
import os.path
import pandas as pd


class PatternCounter(object)
  """
  Abstract class for counting patterns
  """

  def __init__(self, ssbml):
    """
    :param SimpleSbml ssbml: for model to count pattern
    """
    self._ssbml = ssbml

  def run(self):
    """
    Count the pattern for this model.
    :return int, int: 
        count of pattern occurrences, count of cases tested
    """
    raise RuntimeError("Not implemented. Must override.")


class ReactionPatternCounter(PatternCounter):
  """
  Abstract class for counting patterns in reactions
  """

  def run(self):
    """
    Count the pattern for this model.
    :return int, int: 
        count of pattern occurrences, count of cases tested
    """
    self._reactions = self._ssbml.getReactions()
    reaction_count = len(self._reactions)
    pattern_count = len(
        [r for r in self._reactions if self._isPattern(r)])
    return pattern_count, reaction_count

  def _isPattern(self, reaction):
    """
    :param libsbml.Reaction:
    :return bool: True if the pattern is present
    """
    raise RuntimeError("Must override.")


class ComplexFormationPatternCounter(ReactionPatternCounter):
  """
  Tests if the reactants are combined in a way to be a substring
  of the product.
  """

  def _isPattern(self, reaction):
    """
    :param libsbml.Reaction:
    :return bool: True if the pattern is present
    """


if __name__ == '__main__':
  main(sys.argv)  
