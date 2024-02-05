import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import DataStructs

# Load the CSV file into a DataFrame
df = pd.read_csv('SIMILES.csv',encoding='latin-1')

# Function to compute the Morgan fingerprint for a given SMILES string
def compute_fingerprint(smiles):
    if pd.notna(smiles):
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
            return fp
    return None

# Function to calculate similarity between two fingerprints
def calculate_similarity(fp1, fp2):
    if fp1 is not None and fp2 is not None:
        return DataStructs.TanimotoSimilarity(fp1, fp2)
    else:
        return None

# Input SMILES structure to find similarities
input_smiles = 'O=C(C)Oc1ccccc1C(=O)O'

# Compute fingerprint for the input SMILES
input_fp = compute_fingerprint(input_smiles)

# Check if the input SMILES is valid
if input_fp is None:
    print("Invalid input SMILES structure.")
else:
    # Calculate similarity for each drug in the DataFrame
    df['Similarity'] = df['SMILES'].apply(lambda x: calculate_similarity(input_fp, compute_fingerprint(x)))

    # Sort the DataFrame based on similarity in descending order
    df_sorted = df.sort_values(by='Similarity', ascending=False)

    # Display the results
    print("Top 5 similar drugs:")
    print(df_sorted[['DrugName', 'Similarity']].head(5))