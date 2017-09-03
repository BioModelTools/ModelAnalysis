""" Analyzes patterns in BioModels, putting the statistics in a CSV."""

# Input is stdin with BioModels IDs. Outputs to to std out.
# May want something else as output since stdout may be for status
# Features
#   Checkpoints on each biomodel
#   Can be restarted and continues where left off based on
#     what has been written to the output file
#   Progress report
#   Writes CSV with variable descriptions

import statistic
import os

REPORT_INTERVAL = 1  # Number of Biomodels between writing a status report
ROOT_DIRECTORY = os.path.dirname(
    os.path.dirname(os.path.realpath(__file__)))
DATA_DIRECTORY = os.path.join(ROOT_DIRECTORY, "Data")
IN_PATH = os.path.join(DATA_DIRECTORY, "all_models.dat")
OT_PATH_DATA = os.path.join(DATA_DIRECTORY, "all_statistics.csv")
OT_PATH_DOC = os.path.join(DATA_DIRECTORY, "variables.csv")


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
    if os.path.isfile(self._ot_path_data):
      with open(self
   

if __name__ == '__main__':
  collector = DataCollector()
  collector.run()
