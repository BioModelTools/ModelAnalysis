# ModelAnalysis
Analysis of kinetics models that provides various statistics for
the BioModels repository (http://www.ebi.ac.uk/biomodels-main).
Existing BioModel statistic focus on what is modelled, with only
minimal information about what is modelled (e.g., http://www.ebi.ac.uk/biomodels-main/static-pages.do?page=release_20140411). Having more
details about the constructs and patterns used in models is helpful
to establishing basic practices for kinetics modelling and tools
to improve the quality of models. This has strong parallels
with software engineering practices for documentation and
programming style.

This project provides the following statistics for each model:

- BIOMODEL ID
- Numer of reactions
- Mean, Std of # reactions per reaction
- Mean, Std of # products per reaction
- Fraction of kinetics that are classified as:
  - Mass action
  - Michaelis Menten
  - Functions
  - Other
- Number of parameters
- Fraction of reactions that contain the following patterns:
  - Add moiety: Reactant is a substring of a product.
  - Remove moiety: Product is a substring of a reactant.
  - Transfer moiety: One product is a substring of a reactant and
    another reactant appears as a product with the difference
    between the first reactant and product.
  - Add, remove, transfer Pi moiety: Looks for "p" at the beginning or end of a name.
  - Complex formation: At least two reactants appear as a substring ofone product.
  - Complex disassociation: Two products, when concatenated, form one reactant.
  - Catalyzed reaction: One or more species appears as both a reactant and a product.
