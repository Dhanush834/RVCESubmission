import pandas as pd
import pubchempy as pcp

def get_compound_name_from_smiles(smiles):
    try:
        # Search PubChem with the provided SMILES
        compound = pcp.get_compounds(smiles, 'smiles', record_type='3d')[0]

        # Get the compound name
        compound_name = compound.iupac_name

        return compound_name

    except Exception as e:
        print(f"Error: {e}")
        return None

# Read CSV file containing canonical SMILES structures
csv_file_path = input("Enter the path to the CSV file: ")
df = pd.read_csv(csv_file_path)

# Create a new column for compound names
df['Compound Name'] = df['Canonical SMILES'].apply(get_compound_name_from_smiles)

# Display the results
print(df[['Canonical SMILES', 'Compound Name']])
