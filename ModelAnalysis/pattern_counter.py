"""
Classes that count patterns in SBML models
"""
from simple_sbml import SimpleSBML
import re
import sys
import os.path
import pandas as pd

################################################
# Classes that count pattern occurrences
################################################
class PatternCounter(object):
  """
  Abstract class for counting patterns.
  Defines the interface and establishes the instance variables.
  """

  def __init__(self, ssbml, pattern_cls):
    """
    :param SimpleSBML ssbml: for model to count pattern
    :param ModelPattern model_pattern:
    """
    self._ssbml = ssbml
    self._pattern_cls = pattern_cls

  def run(self):
    """
    Count the pattern for this model.
    :return int, int: 
        count of pattern occurrences, count of cases tested
    """
    raise RuntimeError("Not implemented. Must override.")


class ReactionPatternCounter(PatternCounter):
  """
  Abstract class for counting patterns in reactions.
  Handles the iteration.
  model_pattern must be a ReactionPattern
  """

  def run(self):
    """
    Count the pattern for this model.
    :return int, int: 
        count of pattern occurrences, count of cases tested
    """
    self._reactions = self._ssbml.getReactions()
    reaction_count = len(self._reactions)
    pattern_count = 0
    for reaction in self._reactions:
      model_pattern = self._pattern_cls(reaction)
      if model_pattern.isPattern():
        pattern_count += 1
    return pattern_count, reaction_count


################################################
# Classes that check for a pattern's presence
################################################
class ModelPattern(object):
  """
  Abstract class for a pattern
  """

  @staticmethod
  def _jointSubstring(substrings, string):
    """
    Calculates the number of non-overlapping substrings in string.
    The approach is heuristic and so will not always find the maximum
    number of substrings.
    :param list-of-str substrings:
    :param str string:
    :return int: Number of non-overlapping substrings present
    """
    ranges = []  # Positions for reactants in product
    for substring in substrings:
      pos = string.find(substring)
      if pos >= 0:
        ranges.append(range(pos, len(substring)))
    result = 0
    if len(ranges) > 0:
      result = 1
      last_range = set(ranges[0])
      for rng in ranges[1:]:
        combined_range = last_range.union(set(rng))
        if len(combined_range) == len(last_range) + len(rng):
          result += 1
          last_range = combined_range
    return result

  def isPattern(self):
    raise RuntimeError("Must override")


class ReactionPattern(ModelPattern):
  """
  Abstract class for patterns in reactions.
  Contains common code used for pattern analysis.
  """

  def __init__(self, reaction):
    """
    :param libsbml.Reaction reaction:
    """
    self._reaction = reaction

  def _getReactants(self):
    """
    :return list-of-str:
    """
    result = []
    for idx in range(raction.getNumReactants()):
      reactant = reaction.getProduct(idx)
      result.append(reactant.getSpecies())
    return result

  def _getProducts(self):
    """
    :return list-of-str:
    """
    result = []
    for idx in range(raction.getNumProducts()):
      reactant = reaction.getProduct(idx)
      result.append(reactant.getSpecies())
    return result


class ComplexFormationReactionPattern(ReactionPattern):
  """
  Tests if the reactants are combined in a way to be a substring
  of the product.
  """

  def isPattern(self):
    """
    Looks for a combination of the reactants in a product.
    :param libsbml.Reaction:
    :return bool: True if the pattern is present
    """
    cls = ComplexFormationReactionPattern
    reactants = self._getReactants()
    products = self._getProducts()
    result = False
    if len(reactants) > 1 and len(products) > 0:
      for product in products:
        if cls._jointSubstring(reactants, product) > 1:
          result = True
          break
    return result


class ComplexDisassociationReactionPattern(ReactionPattern):
  """
  Tests if one or more reactants are decomposed into products
  """

  def isPattern(self):
    """
    Looks for a combination of the product in a reactant.
    :param libsbml.Reaction:
    :return bool: True if the pattern is present
    """
    reactants = self._getReactants()
    products = self._getProducts()
    result = False
    if len(products) > 1 and len(reactants) > 0:
      for reactant in reactants:
        if self._jointSubstring(products, reactant) > 1:
          result = True
          break
    return result


if __name__ == '__main__':
  main(sys.argv)  
