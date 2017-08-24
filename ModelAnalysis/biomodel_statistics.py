"""
Creates statistics for one or more Biomodels
"""
from simple_sbml import SimpleSbml
import sys
import os.path
import pandas as pd


class BiomodelStatistics(object):
  """
  Creates statistics for one or more biomodels
  """

  def __init__(self, biomodel_ids):
    """
    :param list-of-str biomodel_ids: Biomodel IDs
    """
    self._biomodel_ids = biomodel_ids

  def run(self):
    """
    Create the statistics
    :return pandas.DataFrame:
    """
    df = pd.DataFrame()
    for biomodel_id in self._biomodel_ids:
      df = df.append(self._process(biomodel_id))
    return df

  df _process(biomodel_id):
    """
    Compute statistics for a single Biomodel
    :param str biomodel_id:
    """


if __name__ == '__main__':
  main(sys.argv)  
