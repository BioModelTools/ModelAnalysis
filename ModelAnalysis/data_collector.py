""" Analyzes patterns in BioModels, putting the statistics in a CSV."""

# Input is stdin with BioModels IDs. Outputs to to std out.
# May want something else as output since stdout may be for status
# Features
#   Checkpoints on each biomodel
#   Can be restarted and continues where left off based on
#     what has been written to the output file
#   Progress report
#   Writes CSV with variable descriptions

from biomodel_iterator import BiomodelIterator
from statistic import Statistic, ErrorStatistic

import os
import pandas as pd

REPORT_INTERVAL = 10  # Number of Biomodels between writing a status report
ROOT_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))
DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "Data")
IN_PATH = os.path.join(DATA_DIRECTORY, "all_models.dat")
OT_PATH_DATA = os.path.join(DATA_DIRECTORY, "all_statistics.csv")
OT_PATH_DOC = os.path.join(DATA_DIRECTORY, "variables.csv")
IS_MAIN = __name__ == '__main__'


class DataCollector(object):
  """
  Obtains the data from the BioModels database.
  """

  def __init__(self, in_path=IN_PATH, 
                     ot_path_data=OT_PATH_DATA, 
                     ot_path_doc=OT_PATH_DOC):
    """
    :param str in_path: Path to the file containing a list of model IDs
    :param str ot_path_data: Path to a output file for statistics
    :param str ot_path_doc: Path to a output file for variable descriptions
    """
    self._in_path = in_path
    self._ot_path_data = ot_path_data
    self._ot_path_doc = ot_path_doc

  def _getBiomodelIterator(self):
    """
    Finds the set of Biomodel IDs that have already been written
    :return BiomodelIterator:
    """
    excludes = None
    if os.path.isfile(self._ot_path_data):
      try:
        df = pd.read_csv(self._ot_data_path)
        self._excludes = [id for id in df['Biomodel_Id']]
      except:
        pass
    return BiomodelIterator(self._in_path, excludes=excludes)

  def run(self):
    """
    Compute the statistics
    """
    biter = self._getBiomodelIterator()
    report_count = REPORT_INTERVAL
    df = pd.DataFrame()
    for shim in biter:
      if shim.getException() is None:
        stat_dict = Statistic.getAllStatistics(shim)
      else:
        stat_dict = ErrorStatistic(shim).getStatistic()
      df = df.append(stat_dict, ignore_index=True)
      if IS_MAIN:
        report_count += -1
        if report_count < 1:
          df.to_csv(self._ot_path_data)
          print ("Completed Biomodel ID %s." % shim.getBiomodelId())
          report_count = REPORT_INTERVAL
    df.to_csv(self._ot_path_data, index=False)
    doc_dict = {
                "Column": Statistic.getDoc().keys(),
                "Description": Statistic.getDoc().values(),
               }
    pd.DataFrame(doc_dict).to_csv(self._ot_path_doc, index=False)
    if IS_MAIN:
      print ("Done!")


if IS_MAIN:
  collector = DataCollector()
  collector.run()
