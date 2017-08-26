"""
Provides simplified, read-only access to an SBML model.
"""
import sys
import os.path
import tellurium as te  # Must import tellurium before libsbml
import libsbml


class SimpleSBML(object):
  """
  Provides access to reactions, species, and parameters.
  """

  def __init__(self, filepath=None, sbmlstr=None):
    """
    :param str filepath: File containing the SBML document
    :param str sbmlstr: String containing the SBML document
    :raises IOError: Error encountered reading the SBML document
    :raises ValueError: if filepath and sbmlstr are both None
    """
    self._reader = libsbml.SBMLReader()
    if filepath is not None:
      self._filepath = filepath
      self._document = self._reader.readSBML(self._filepath)
    elif sbmlstr is not None:
      self._document = self._reader.readSBMLFromString(sbmlstr)
    else:
      raise ValueError("Must have an SBML source!")
    if (self._document.getNumErrors() > 0):
      raise IOError("Errors in SBML document\n%s" 
          % self._document.printErrors())
    self._model = self._document.getModel()
    self._reactions = self._getReactions()
    self._parameters = self._getParameters()  # dict with key=name
    self._species = self._getSpecies()  # dict with key=name

  @classmethod
  def getSBMLForBiomodel(cls, biomodel_id):
    """
    Obtains SBML for the the Biomodel.
    :param str biomodel_id:
    """
    url = "http://www.ebi.ac.uk/biomodels-main/download?mid=%s" % biomodel_id
    return te.loadSBMLModel(url).getSBML()

  def _getSpecies(self):
    speciess = {}
    for idx in range(self._model.getNumSpecies()):
      species = self._model.getSpecies(idx)
      speciess[species.getId()] = species
    return speciess

  def _getReactions(self):
    """
    :param libsbml.Model:
    :return list-of-reactions
    """
    num = self._model.getNumReactions()
    return [self._model.getReaction(n) for n in range(num)]

  def _getParameters(self):
    """
    :param libsbml.Model:
    :return list-of-reactions
    """
    parameters = {}
    for idx in range(self._model.getNumParameters()):
      parameter = self._model.getParameter(idx)
      parameters[parameter.getId()] = parameter
    return parameters

  def getReactions(self):
    return self._reactions

  def getParameters(self):
    return self._parameters.values()

  def getReactants(self, reaction):
    """
    :param libsbml.Reaction:
    :return list-of-libsbml.SpeciesReference:
    To get the species name: SpeciesReference.species
    To get stoichiometry: SpeciesReference.getStoichiometry
    """
    return [reaction.getReactant(n) for n in range(reaction.getNumReactants())]

  def getProducts(self, reaction):
    """
    :param libsbml.Reaction:
    :return list-of-libsbml.SpeciesReference:
    """
    return [reaction.getProduct(n) for n in range(reaction.getNumProducts())]

  def getReactionString(self, reaction):
    """
    Provides a string representation of the reaction
    :param libsbml.Reaction reaction:
    """
    cls = SimpleSBML
    reaction_str = ''
    base_length = len(reaction_str)
    for reference in self.getReactants(reaction):
      if len(reaction_str) > base_length:
        reaction_str += " + " + reference.species
      else:
        reaction_str += reference.species
    reaction_str += "-> "
    base_length = len(reaction_str)
    for reference in self.getProducts(reaction):
      if len(reaction_str) > base_length:
        reaction_str += " + " + reference.species
      else:
        reaction_str += reference.species
    kinetics_terms = cls.getReactionKineticsTerms(reaction)
    reaction_str += "; " + ", ".join(kinetics_terms)
    return reaction_str

  @classmethod
  def getReactionKineticsTerms(cls, reaction):
    """
    Gets the terms used in the kinetics law for the reaction
    :param libsbml.Reaction
    :return list-of-str: names of the terms
    """
    terms = []
    law = reaction.getKineticLaw()
    if law is not None:
      math = law.getMath()
      asts = [math]
      while len(asts) > 0:
        this_ast = asts.pop()
        if this_ast.isName():
          terms.append(this_ast.getName())
        else:
          pass
        num = this_ast.getNumChildren()
        for idx in range(num):
          asts.append(this_ast.getChild(idx))
    return terms

  def isSpecies(self, name):
    """
    Determines if the name is a chemical species
    """
    return self._species.has_key(name)

  def isParameter(self, name):
    """
    Determines if the name is a parameter
    """
    return self._parameters.has_key(name)


if __name__ == '__main__':
  main(sys.argv)  
