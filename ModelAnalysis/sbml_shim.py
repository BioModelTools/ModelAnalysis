"""
Provides simplified, read-only access to an SBML model.
Notes:
  Because of an apparent bug in libsbml, we cannot
  pass a libsbml object across subroutine calls. SBMLShim
  provides the interface to libsbml.
"""
import urllib2
import sys
import os.path
import tellurium as te  # Must import tellurium before libsbml
import libsbml


class SBMLShim(object):
  """
  Provides access to reactions, species, and parameters.
  """

  def __init__(self, filepath=None, sbmlstr=None, 
       is_ignore_errors=False):
    """
    :param str filepath: File containing the SBML document
    :param str sbmlstr: String containing the SBML document
    :param bool isIgnoreErrors: Do not return raise an exception
        if there are errors in the document
    :raises IOError: Error encountered reading the SBML document
    :raises ValueError: if filepath and sbmlstr are both None
    Notes: If an error is occurred reading the SBML, a minimalist shim
    is still created if is_ignore_errors == True.
    """
    self._is_ignore_errors = is_ignore_errors
    reader = libsbml.SBMLReader()
    # Acquire the model if there is one
    if filepath is not None:
      self._filepath = filepath
      self._document = reader.readSBML(self._filepath)
    elif sbmlstr is not None:
      self._document = reader.readSBMLFromString(sbmlstr)
    else:
      # No model is present
      if self._is_ignore_errors:
        self._document = None
      else:
        raise ValueError("Must have an SBML source!")
    self._biomodel_id = None
    self._exception = None  # Exception when reading the model
    self._reactions = []
    self._parameters = []
    self._species = []
    if self._document is not None:
      self._checkErrors()
      self._model = self._document.getModel()
      if self._model is not None:
        self._reactions = self._getReactions()
        self._parameters = self._getParameters()  # dict with key=name
        self._species = self._getSpecies()  # dict with key=name
 
  def _checkErrors(self):
    if (self._document.getNumErrors() > 0) and not self._is_ignore_errors:
      for e in (self._document.getError(n) for n in range(self._document.getNumErrors())):
        if e.getSeverity() == libsbml.LIBSBML_SEV_ERROR or e.getSeverity() == libsbml.LIBSBML_SEV_FATAL:
            raise IOError("Errors in SBML document\n%s" % e.getMessage())
 
  @staticmethod 
  def _buildStatement(base, *args):
    """
    Constructs a statement with variable arguments.
    :param str base: base of statement
    :param tuple *args: arguments
    """
    statement = "%s(" % base
    for arg in args:
      statement = "%s, %s" % (statement, arg)
    statement = "%s)" % statement
    return statement

  def execFunction(self, func, attribute="document", *args):
    """
    Executes a function in libsbml.document or libsbml.model.
    :param str func: function to execute
    :param tuple args:
    :param str attribute: either "document" or "model"
    """
    base = "self._%s.%s" % (attribute, func)
    statement = self.__class__._buildStatement(base, *args)
    return eval(statement)

  @classmethod
  def getShimForBiomodel(cls, biomodel_id):
    """
    Obtains SBML for the the Biomodel.
    :param str biomodel_id:
    :return SBMLShim:
    """
    url = "http://www.ebi.ac.uk/biomodels-main/download?mid=%s" % biomodel_id
    try:
      response = urllib2.urlopen(url)
      sbmlstr = response.read()
      shim = SBMLShim(sbmlstr=sbmlstr)
    except Exception as err:
      shim = SBMLShim(sbmlstr="", is_ignore_errors=True)  # Minimal shim
      shim._exception = err
    shim._biomodel_id = biomodel_id
    return shim

  def getException(self):
    return self._exception

  def _getSpecies(self):
    speciess = {}
    for idx in range(self._model.getNumSpecies()):
      species = self._model.getSpecies(idx)
      speciess[species.getId()] = species
    return speciess

  def getSpecies(self):
    return self._species.keys()

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

  def getReactionIndicies(self):
    return range(self._model.getNumReactions())

  def getParameterNames(self):
    return self._parameters.keys()

  def getParameters(self):
    return self._parameters.values()

  def _coerceToReaction(self, reaction_or_int):
    """
    :param libsbml.Reaction or int reaction_or_int:
    :return libsbml.Reaction:
    """
    if isinstance(reaction_or_int, int):
      reaction = self._model.getReaction(reaction_or_int)
    else:
      reaction = reaction_or_int
    return reaction

  def getReactants(self, reaction):
    """
    :param libsbml.Reaction or int:
    :return list-of-libsbml.SpeciesReference:
    To get the species name: SpeciesReference.species
    To get stoichiometry: SpeciesReference.getStoichiometry
    """
    reaction = self._coerceToReaction(reaction)
    return [reaction.getReactant(n) for n in range(reaction.getNumReactants())]

  def getProducts(self, reaction):
    """
    :param libsbml.Reaction:
    :return list-of-libsbml.SpeciesReference:
    """
    reaction = self._coerceToReaction(reaction)
    return [reaction.getProduct(n) for n in range(reaction.getNumProducts())]

  def getReactionString(self, reaction):
    """
    Provides a string representation of the reaction
    :param libsbml.Reaction reaction:
    """
    reaction = self._coerceToReaction(reaction)
    cls = SBMLShim
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
    reaction = self._coerceToReaction(reaction)
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

  @staticmethod
  # Create an SBML file from an antimony string
  def createSBML(antimony_str):
    """
    :param str antimony_str: antimony model
    :return str SBML:
    """
    rr = te.loada(antimony_str)
    sbmlstr = rr.getSBML()
    return sbmlstr
  
  @staticmethod
  # Creates a reaction
  def createSBMLReaction(reactants, products):
    """
    :param list-of-str reactants:
    :param list-of-str products:
    :return str SBML:
    """
    antimony_str = " + ".join(reactants)
    antimony_str += " -> "
    antimony_str += " + ".join(products) + "; 1" 
    species = list(reactants)
    species.extend(products)
    for spc in species:
      new_str = "\n%s = 1;" % spc
      antimony_str += new_str
    sbmlstr = SBMLShim.createSBML(antimony_str)
    return sbmlstr

  def getBiomodelId(self):
    return self._biomodel_id


if __name__ == '__main__':
  main(sys.argv)  
