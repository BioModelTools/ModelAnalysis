"""
Tests for DataCollector
"""
from data_collector import DataCollector
import os
import pandas as pd
import unittest


IGNORE_TEST = False
DIRECTORY = os.path.dirname(os.path.realpath(__file__))
IN_FILE = os.path.join(DIRECTORY, "test_biomodel_iterator.dat")
IN_FILE_BAD = os.path.join(DIRECTORY, "test_data_collector.dat")
OT_FILE_DATA = os.path.join(DIRECTORY, "test_data_collector_data.csv")
OT_FILE_DOC = os.path.join(DIRECTORY, "test_data_collector_doc.csv")


#############################
# Tests for Counter Classes
#############################
class TestDataCollector(unittest.TestCase):

  def setUp(self):
    self.collector = DataCollector(in_path=IN_FILE,
        ot_path_data=OT_FILE_DATA, ot_path_doc=OT_FILE_DOC)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertEqual(self.collector._ot_path_data, OT_FILE_DATA)

  def testRun(self):
    self.collector.run()
    df = pd.read_csv(OT_FILE_DATA)
    self.assertEqual(len(df["Biomodel_Id"]), 2)

  def testRunWithError(self):
    collector = DataCollector(in_path=IN_FILE_BAD,
        ot_path_data=OT_FILE_DATA, ot_path_doc=OT_FILE_DOC)
    collector.run()
    df = pd.read_csv(OT_FILE_DATA)
    self.assertEqual(len(df["Biomodel_Id"]), 3)



if __name__ == '__main__':
  unittest.main()
