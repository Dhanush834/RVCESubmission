from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import rdMolDescriptors  # Import the rdMolDescriptors module

# Define the compound
smiles = "CCO"
compound = Chem.MolFromSmiles(smiles)

# Check if the compound is valid
if compound is not None:
    # Generate the compound image
    image = Draw.MolToImage(compound)

    # Get the compound details
    # Check if "_Name" property is available before accessing it
    name = compound.GetProp("_Name") if "_Name" in compound.GetPropNames() else "N/A"
    
    # Use rdMolDescriptors module to access CalcMolFormula and CalcExactMolWt
    formula = rdMolDescriptors.CalcMolFormula(compound)
    weight = rdMolDescriptors.CalcExactMolWt(compound)

    # Display the compound image and details
    image.show()
    print("Compound Name:", name)
    print("Compound Formula:", formula)
    print("Compound Weight:", weight)
else:
    print("Invalid compound generated from SMILES.")
