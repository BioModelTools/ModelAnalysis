'''A discontiguous string is a substring that may have one or more embedded substrings. '''

class DCString(object):
  """
  A discontinuous substring is a substring that may not occur in successive positions.
  For example, "dog" is a continguous substring in "Cats and dogs". However it is
  a discontiguous substring in "doing" (do__g). The difference between "dog" and
  "doing" is "in". 
  """

  def __init__(self, string, substring):
    """
    :param str string: Main string
    :param str substring: Embedded within string, possibly with discontinuities
    """
    self._string = string
    self._substring = substring
    self._positions = self._find()

  def _find(self):
    """
    Determines if the substring is present in the string.
    :return list-of-int: positions in the string or empty if none
    """
    subpos = 0
    len_substring = len(self._substring)
    found = False
    positions = []
    for pos in range(len(self._string)):
      if self._string[pos] == self._substring[subpos]:
        positions.append(pos)
        subpos += 1
        if subpos >= len_substring:
          break
    return positions

  def _count(self, positions=None):
    """
    :param list-of-int positions: if None, use self._positions
    :return int: number of discontinuities in the main string for substring
    """
    if positions is None:
      positions = self._positions
    pairs = zip(positions[0:-1], positions[1:])
    num = sum([1 if y - x > 1 else 0 for x,y in pairs])
    return num

  def diff(self, **kwgs):
    """
    :return list-of-str: Returns the difference between substring and the string
    :raises ValueError: isSubstring is False
    """
    if not self.isPresent(**kwgs):
      raise ValueError("Not a substring")
    return ''.join([self._string[p] for p in range(len(self._string))
                    if p not in self._positions])
    

  def isPresent(self, num_discontinuities=1):
    """
    :param int num_discontinuities: Number of discontinuities permitted in the string
    :return bool: True if substring lies within string, possibly discontiguously
    """
    if len(self._positions) == len(self._substring):
      if self._count() <= num_discontinuities:
        return True
      else:
        return False
    else:
      return False
   
    
    
