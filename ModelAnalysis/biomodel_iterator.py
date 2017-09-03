"""
Iterates through a collection of BioModels
"""
from sbml_shim import SBMLShim
import sys
import os.path

################################################
# Classes that count pattern occurrences
################################################
class BiomodelIterator(object):

  def __init__(self, path, excludes=None):
    """
    :param str path: path to a file containing a list of Biomodel IDs to process
      The file should contain a list of BioModels identifiers,
      one per line.
    :param list-of-str excludes: Biomodel IDs to exclude
    """
    self._path = path
    self._idx = 0
    with open(self._path, 'r') as fh:
      ids = fh.readlines()  # Biomodels Ids
    if excludes is None:
      excludes = []
    pruned_ids = [id.replace('\n', '') for id in ids]
    self._ids = [id.replace('\n', '') for id in pruned_ids
                 if not id in excludes]

  def __iter__(self):
    return self

  def next(self):
    """
    :return SBMLShim: next bio model
    :raises StopIteration:
    """
    if self._idx < len(self._ids):
      shim = SBMLShim.getShimForBiomodel(self._ids[self._idx])
      self._idx += 1
      return shim
    else:
      raise StopIteration()
     


if __name__ == '__main__':
  main(sys.argv)  
