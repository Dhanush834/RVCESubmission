from rdkit import Chem
from rdkit.Chem import AllChem
import math
import pickle 

# empty list to read list from a file
smiles = []

# open file and read the content in a list
with open(r'smiles.txt', 'r') as fp:
    for line in fp:
        # remove linebreak from a current name
        # linebreak is the last character of each line
        x = line[:-1]

        # add current item to the list
        smiles.append(x)

# Returns all Gast_charges in the database into a list
gast_charges = []
for i in smiles:
    mol = Chem.MolFromSmiles(i)
    AllChem.ComputeGasteigerCharges(mol)
    charges = [atom.GetDoubleProp('_GasteigerCharge') for atom in mol.GetAtoms()]
    gast_charges.append(charges)

gast_charges = [item for sublist in gast_charges for item in sublist]
gast_charges = [x for x in gast_charges if not math.isnan(x)]
gast_charges = [x for x in gast_charges if not math.isinf(x)]

# function that yields a database of differences
def gast_diff(gast):
    gast_charge = []
    for i in range(0, len(gast)):
        for j in range(i + 1, len(gast)):
            gast_charge.append(abs(gast[i] - gast[j]))

    return gast_charge

# creates the scoring matrix of all vs all
score = {}
total_count = len(gast_charges)
for i in range(0, 30):
    test = round(i * 10**-1, 1)  # where 10^d, d is the number of zeros after max of range
    count = len([x for x in gast_charges if x >= test])
    prob = count / total_count
    score[test] = math.log2(prob)

with open('score_all_v_all.pkl', 'wb') as f:
    pickle.dump(score, f)
