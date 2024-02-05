import pickle

# Load the contents of the .pkl file
with open('score_all_v_all.pkl', 'rb') as f:
    loaded_score = pickle.load(f)

# Print the loaded content
print(loaded_score)
