"""Utilities in support of Model Analysis."""

import tellurium as te


# Create an SBML file from an antimony string
def createSBML(antimony_str):
  """
  :param str antimony_str: antimony model
  :return str SBML:
  """
  rr = te.loada(antimony_str)
  return rr.getSBML()
