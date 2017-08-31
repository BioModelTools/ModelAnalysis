"""
Classes that count patterns in SBML models.
Usage:
   pattern = XPattern(shim)
   pattern_count, total_count = pattern.run()
"""
from sbml_shim import SBMLShim
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
  At the top of the class hierarchy are "Counter" classes that
  count occurrences of a pattern. "Recognizer" classes inherit
  from counter classes.
  """

  def __init__(self, shim):
    """
    :param SBMLShim shim: for model to count pattern
    :param ModelPattern model_pattern:
    """
    self._shim = shim

  def run(self):
    """
    Count the pattern for this model.
    Must be overridden by another "Counter" class.
    :return int, int: 
        count of pattern occurrences, count of cases tested
    """
    raise RuntimeError("Not implemented. Must override.")

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
    indicies = self._shim.getReactionIndicies()
    reaction_count = len(indicies)
    pattern_count = 0
    for idx in indicies:
      if self.isPattern(idx):
        pattern_count += 1
    return pattern_count, reaction_count


################################################
# Classes that recognize patterns
################################################
class ComplexFormationReactionPattern(ReactionPatternCounter):
  """
  Tests if the reactants are combined in a way to be a substring
  of the product.
  """

  def isPattern(self, reaction_idx):
    """
    Looks for a combination of the reactants in a product.
    :param int reaction_idx:
    :return bool: True if the pattern is present
    """
    cls = ComplexFormationReactionPattern
    reactants = [r.getSpecies() for
                 r in self._shim.getReactants(reaction_idx)]
    products = [p.getSpecies() for
                 p in self._shim.getProducts(reaction_idx)]
    result = False
    if len(reactants) > 1 and len(products) > 0:
      for product in products:
        if cls._jointSubstring(reactants, product) > 1:
          result = True
          break
    return result


class ComplexDisassociationReactionPattern(ReactionPatternCounter):
  """
  Tests if one or more reactants are decomposed into products
  """

  def isPattern(self, reaction_idx):
    """
    Looks for a combination of the product in a reactant.
    :param int reaction_idx:
    :return bool: True if the pattern is present
    """
    reactants = [r.getSpecies() for
                 r in self._shim.getReactants(reaction_idx)]
    products = [p.getSpecies() for
                 p in self._shim.getProducts(reaction_idx)]
    result = False
    for reactant in reactants:
      if self._jointSubstring(products, reactant) > 1:
        result = True
        break
    return result


if __name__ == '__main__':
  main(sys.argv)  
