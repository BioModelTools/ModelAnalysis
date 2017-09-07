"""
Tests for DCString
"""
from dcstring import DCString
import unittest


IGNORE_TEST = False


#############################
# Tests for Counter Classes
#############################
class TestDCString(unittest.TestCase):

  def setUp(self):
    self.dcstring = DCString("doing", "dog")

  def testIsPresent(self):
    if IGNORE_TEST:
      return
    dcstring = DCString("doing", "dog")
    self.assertTrue(dcstring.isPresent())
    dcstring = DCString("oing", "dog")
    self.assertFalse(dcstring.isPresent())
    dcstring = DCString("cats and dogs", "asd")
    self.assertFalse(dcstring.isPresent())
    self.assertTrue(dcstring.isPresent(num_discontinuities=2))

  def testFind(self):
    if IGNORE_TEST:
      return
    dcstring = DCString("doing", "dog")
    self.assertEqual(dcstring._find(), [0, 1, 4])
    dcstring = DCString("oing", "dog")
    self.assertEqual(dcstring._find(), [])
    dcstring = DCString("doin", "dog")
    self.assertEqual(dcstring._find(), [0, 1])

  def testCount(self):
    self.assertEqual(self.dcstring._count(positions = [0, 1, 4]), 1)
    self.assertEqual(self.dcstring._count(positions = [0, 2, 4]), 2)
    self.assertEqual(self.dcstring._count(positions = [0, 1, 2]), 0)

  def testDiff(self):
    self.assertEqual(self.dcstring.diff(), "in")
    dcstring = DCString("cats and dogs", "asd")
    self.assertEqual(dcstring.diff(num_discontinuities=2), 
        "ct an dogs")
   

if __name__ == '__main__':
  unittest.main()
