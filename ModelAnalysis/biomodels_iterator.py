"""
Iterates through a collection of BioModels
"""
from sbml_shim import SBMLShim
import sys
import os.path

################################################
# Classes that count pattern occurrences
################################################
class BiomodelsIterator(object):

  def __init__(self, path):
    """
    :param str path: path to a file containing a list of BioModels to process
      The file should contain a list of BioModels identifiers,
      one per line.
    """
    self._path = path
    self._idx = 0
    self._cur_id = None
    with open(self._path, 'r') as fh:
      self._ids = fh.readlines()  # Biomodels Ids

  def __iter__(self):
    return self

  def next(self):
    """
    :return SBMLShim: next bio model
    :raises StopIteration:
    """
    if self._idx < len(self._ids):
      self._cur_id = (self._ids[self._idx]).replace('\n', '')
      sbmlstr = SBMLShim.getSBMLForBiomodel(self._cur_id)
      self._idx += 1
      return SBMLShim(sbmlstr=sbmlstr)
    else:
      raise StopIteration()

  def getId(self):
    return self._cur_id
     


if __name__ == '__main__':
  main(sys.argv)  
