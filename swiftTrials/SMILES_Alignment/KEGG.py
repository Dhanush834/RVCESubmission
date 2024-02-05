from Bio.KEGG import REST
import pubchempy as pcp
from rdkit import Chem
from rdkit.Chem import AllChem

# Function to retrieve the name of the compounds given a compound id
def get_compound_name(cpd_id):
    entry = REST.kegg_get(cpd_id).read()
    for line in entry.rstrip().split("\n"):
        if line.startswith("NAME"):
            name = line.split(" ", 1)[1]
            return name.strip().rstrip(';')

# Retrieves all the canonical SMILES in a given pathway id and returns them as a list
def pathway(kegg_map):
    result = REST.kegg_link('compound', kegg_map).read()
    
    lines = result.strip().split('\n')
    cpd_codes = [line.split('\t')[1] for line in lines]
    
    names = []
    for codes in cpd_codes:
        names.append(get_compound_name(codes))
        
    smiles = []

    # Fetch the SMILES strings
    for compound in names:
        results = pcp.get_compounds(compound, 'name')
        if results:
            smiles.append(results[0].canonical_smiles)
            
    return smiles

# Canonicalize using RDKit
def canonicalize(smiles_list):
    canonical_smiles = []
    for smile in smiles_list:
        mol = Chem.MolFromSmiles(smile)
        if mol:
            mol = Chem.AddHs(mol)
            AllChem.Compute2DCoords(mol)
            canonical_smiles.append(Chem.MolToSmiles(mol, isomericSmiles=True))
    return canonical_smiles

# Example usage:
citrate_cycle_smiles = pathway('M00009')
citrate_cycle_canonical = canonicalize(citrate_cycle_smiles)
print(citrate_cycle_canonical)

glycolysis_smiles = pathway('M00001')
glycolysis_canonical = canonicalize(glycolysis_smiles)
print(glycolysis_canonical)
