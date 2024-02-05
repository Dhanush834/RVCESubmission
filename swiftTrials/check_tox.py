import csv

def load_toxicity_data(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]
    return rows

def get_toxicity_properties(smiles, data):
    start_index = -1
    end_index = -1

    for i, row in enumerate(data):
        if row and row[0] == "SMILES:" + smiles:
            start_index = i
            break

    if start_index != -1:
        for i in range(start_index + 1, len(data)):
            if not data[i] or not data[i][0]:
                end_index = i
                break

        return data[start_index+1:end_index]
    else:
        return None

def print_toxicity_properties(smiles, properties):
    print(f"SMILES: {smiles}")
    for row in properties:
        print(f"{row[0]}\t{row[1]}\t{row[2]}")

if __name__ == "__main__":
    csv_file = "tox-master.csv"  # Replace with your actual CSV file

    # Load the toxicity data from the CSV file
    toxicity_data = load_toxicity_data(csv_file)

    # Example SMILES structure
    input_smiles = "CC1COC(=O)O"  # Replace with the SMILES structure you want to check

    # Get toxicity properties for the input SMILES
    properties = get_toxicity_properties(input_smiles, toxicity_data)

    if properties:
        print_toxicity_properties(input_smiles, properties)
    else:
        print(f"No data found for SMILES: {input_smiles}")
