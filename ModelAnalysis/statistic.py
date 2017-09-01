"""
Classes that compute statistics for SBML models.
Statistic is an abstract class. Leaf classes that inherit from Statistic
override the method getStatistic, which returns a dictionary that has
name-value pairs.
Usage for a non-abstract XStatistic that inherits from Statistic:
  x_statistic = XStatistic(shim)  # Where shim is a SBMLShim object
  statistic_dict = x_statistic.getStatistic()
Note that all leaf classes are assumed to be non-abstract statistics classes
that are to be instantiated.
"""
from sbml_shim import SBMLShim

import numpy as np
import re
import os.path
import pandas as pd
import sys

################################################
# Classes that collect statistics
################################################
class Statistic(object):
  """
  Abstract class for computing statistics. Leaf classes must implement
  gtStatistic. This class provides methods used by inheriting classes.
  """

  def __init__(self, shim):
    """
    :param SBMLShim shim:
    """
    self._shim = shim

  def getStatistic(self):
    """
    Collect statistics for the model.
    Must be overridden by another "collector" class.
    :return dict: Dictionary of statistic name and its mean, std
    """
    raise RuntimeError("Not implemented. Must override.")

  @staticmethod
  def _findLeafSubclasses(klass):
    """
    Finds the descendents that have no inheritors
    :param type klass:
    :return list-of-type:
    """
    leaves = set()
    parents = set([klass])
    while len(parents) > 0:
      parent = parents.pop()
      children = parent.__subclasses__()
      if (len(children) == 0):
        leaves.add(parent)
      else:
        parents = parents.union(set(children))
    return leaves

  @classmethod
  def getAllStatistics(cls, shim):
    """
    Acquires all of the statistics available by instantiating all leaf
    classes.
    :param SBMLShim shim:
    :return dict: Dictionary of statistics
    """
    klasses = cls._findLeafSubclasses(cls)
    results = {}
    for klass in klasses:
      statistic = klass(shim)
      results.update(statistic.getStatistic())
    return results

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


################################################
# Model statistics
################################################
class ModelStatistic(Statistic):
  """
  Computes statistics that apply to the entire model
  """

  def getStatistic(self):
    """
    :return dict:
    """
    return   {
              "Num_Reactions": len(self._shim.getReactionIndicies()),
              "Num_Parameters": len(self._shim.getParameterNames()),
              "Num_Species": len(self._shim.getSpecies()),
             }


################################################
# Reaction statistics
################################################
class ReactionStatistic(Statistic):
  """
  Abstract class for collecting reaction statistics. Reaction statistics
  are obtained by iterating across all reactions and then computing
  aggregations of the results.
  Classes that inherit must provide the following methods:
    _getValue(idx) - provides a scalar number for a reaction, where
                   idx is the reaction index
    _getName() - provides the name for the resulting statistic
  """

  def getStatistic(self):
    """
    Count the pattern for this model.
    :return dict:
    """
    indicies = self._shim.getReactionIndicies()
    values = []
    for idx in indicies:
      values.append(self._getValue(idx))
    mean_value = np.mean(values)
    mean_key = "%s_mean" % self._getName()
    std_value = np.std(values)
    std_key = "%s_std" % self._getName()
    return {mean_key: mean_value, std_key: std_value}

  def _getValue(self):
    """
    :return int/float:
    """
    raise RuntimeError("Not implemented. Must override.")

  def _getName(self):
    """
    :return str:
    """
    raise RuntimeError("Not implemented. Must override.")


class ComplexFormationReactionStatistic(ReactionStatistic):
  """
  Determines if the reactants are combined in a way to be a substring
  of the product.
  """
  NAME = "Complex_Formation"

  def _getValue(self, reaction_idx):
    """
    Looks for a combination of the reactants in a product.
    :param int reaction_idx:
    :return bool: 1 if the pattern is present; else 0
    """
    reactants = [r.getSpecies() for
                 r in self._shim.getReactants(reaction_idx)]
    products = [p.getSpecies() for
                 p in self._shim.getProducts(reaction_idx)]
    result = 0
    if len(reactants) > 1 and len(products) > 0:
      for product in products:
        if self.__class__._jointSubstring(reactants, product) > 1:
          result = 1
          break
    return result

  def _getName(self):
    return self.__class__.NAME


class ComplexDisassociationReactionStatistic(ReactionStatistic):
  """
  Determines if one or more reactants are decomposed into products
  """
  NAME = "Complex_Disassociation"

  def _getValue(self, reaction_idx):
    """
    Looks for a combination of the product in a reactant.
    :param int reaction_idx:
    :return bool: 1 if the pattern is present; else 0
    """
    reactants = [r.getSpecies() for
                 r in self._shim.getReactants(reaction_idx)]
    products = [p.getSpecies() for
                 p in self._shim.getProducts(reaction_idx)]
    result = 0
    for reactant in reactants:
      if self._jointSubstring(products, reactant) > 1:
        result = 1
        break
    return result

  def _getName(self):
    return self.__class__.NAME


if __name__ == '__main__':
  main(sys.argv)  
