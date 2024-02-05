import pubchempy as pcp
import csv

# List of substance names
substance_names = [
    "Heptanoic Acid", "Ethyl Acetate", "Propionic Acid", "Isopropylamine",
    "Diethylene Triamine", "Cyclohexanone", "Diethyl Carbonate", "Propylene Carbonate",
    "Methyl Methacrylate", "Butyl Acrylate", "Triethylene Glycol", "1,4-Dioxane",
    "Isopropyl Ether", "Ethyl Benzoate", "Hexylamine", "Isophorone", "Dimethyl Carbonate",
    "N-Butyl Acetate", "Methyl Methanesulfonate", "N-Ethylpyrrolidone", "1,2-Dichloroethane",
    "tert-Butyl Alcohol", "1,3-Dioxolane", "Trichloroethylene", "Propyl Acetate",
    "2-Methyl-2-butene", "Methyl Acrylate", "N-Butyl Propionate", "Dibutyl Ether",
    "Diethylene Glycol Diethyl Ether", "Methyl tert-Butyl Ether (MTBE)", "Diethyl Malonate",
    "2-Methylpentane", "Tetraethyl Lead", "1,2-Dibromoethane", "Methyl Chloride",
    "Isobutyl Propionate", "Ethyl Thiocyanate", "Propylamine", "Diethylamine"
]

# Dictionary to store Canonical SMILES
canonical_smiles_dict = {}

# Iterate through the list of names
for name in substance_names:
    # Search for the compound by name
    results = pcp.get_compounds(name, 'name')
    # Check if results are found
    if results:
        # Get the first result
        compound = results[0]
        # Get the Canonical SMILES
        canonical_smiles = compound.canonical_smiles
        # Store the Canonical SMILES in the dictionary
        canonical_smiles_dict[name] = canonical_smiles
    else:
        # If no results are found, store a message in the dictionary
        canonical_smiles_dict[name] = 'No result found'

# Save the Canonical SMILES dictionary to a CSV file
with open('master_db.csv', 'w', newline='') as csvfile:
    fieldnames = ['Chemical Name', 'Canonical SMILES']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for name, smiles in canonical_smiles_dict.items():
        writer.writerow({'Chemical Name': name, 'Canonical SMILES': smiles})

print("Data has been saved to master_db.csv.")
