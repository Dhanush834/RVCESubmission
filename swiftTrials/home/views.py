# myapp/views.py
from django.http import JsonResponse
import pandas as pd
import requests
import json

def run_python_program(request):

    def get_classyfire_info(smiles):
        base_url = "https://structure.gnps2.org/classyfire"
        params = {"smiles": smiles}

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad requests
            data = response.json()

            # Extract relevant information from the response
            inchl_key = data.get("inchikey", "")
            superclass = data.get("superclass", {}).get("name", "")
            class_ = data.get("class", {}).get("name", "")

            # Check for the presence of 'subclass' key before accessing it
            subclass_data = data.get("subclass", {})
            subclass = subclass_data.get("name", "") if subclass_data else ""

            molecular_framework = data.get("molecular_framework", "")
            pathway = data.get("pathway", "")

            return inchl_key, superclass, class_, subclass, molecular_framework, pathway

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return "", "", "", "", "", ""

    # Your SMILES array
    your_smiles = ["CCCCCCC(=O)O"]

    # Create a DataFrame with the SMILES
    df = pd.DataFrame({"Canonical SMILES": your_smiles})

    # Apply the ClassyFire API to each row in the DataFrame 
    result = df["Canonical SMILES"].map(get_classyfire_info)

    # Create new columns with the extracted information
    df[["InChIKey", "Superclass", "Class", "Subclass", "Molecular Framework", "Pathway"]] = pd.DataFrame(result.tolist(), index=df.index)

    # Display the DataFrame in the terminal
    output = df.to_dict(orient="records") # Convert DataFrame to dictionary for JsonResponse
    print(output)
    return JsonResponse(output[0])

    

