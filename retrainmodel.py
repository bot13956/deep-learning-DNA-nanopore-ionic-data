from itertools import product
from collections import defaultdict
import pickle

# Step 1: Define a named function for defaultdict initialization
def default_dict_int():
    return defaultdict(int)

# Step 2: Load the DNA sequence from the file and clean it
def load_dna_sequence(file_path):
    with open(file_path, 'r') as file:
        sequence = file.read().replace('\n', '')
    
    # Ensure the sequence only contains valid nucleotides
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    cleaned_sequence = ''.join([char for char in sequence if char in valid_nucleotides])
    
    return cleaned_sequence

# Step 3: Generate k-mers and map them to indices
def generate_kmers(k):
    nucleotides = ['A', 'T', 'C', 'G']  # Only valid nucleotides
    kmers = [''.join(p) for p in product(nucleotides, repeat=k)]
    kmer_to_index = {kmer: i for i, kmer in enumerate(kmers)}
    index_to_kmer = {i: kmer for kmer, i in kmer_to_index.items()}
    return kmers, kmer_to_index, index_to_kmer

# Step 4: Convert the DNA sequence to k-mer indices
def sequence_to_kmers(sequence, k, kmer_to_index):
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    return [kmer_to_index[kmer] for kmer in kmers if kmer in kmer_to_index]

# Step 5: Build a transition matrix to predict the next k-mer
def build_transition_matrix(kmer_indices, num_kmers):
    transition_matrix = defaultdict(default_dict_int)

    # Count transitions between k-mers
    for i in range(len(kmer_indices) - 1):
        current_kmer = kmer_indices[i]
        next_kmer = kmer_indices[i + 1]
        transition_matrix[current_kmer][next_kmer] += 1

    # Convert counts to probabilities
    for current_kmer in transition_matrix:
        total = sum(transition_matrix[current_kmer].values())
        for next_kmer in transition_matrix[current_kmer]:
            transition_matrix[current_kmer][next_kmer] /= total

    return transition_matrix

# Step 6: Save the transition matrix to a file
def save_model(transition_matrix, file_path):
    with open(file_path, 'wb') as file:
        pickle.dump(transition_matrix, file)
    print(f"Model saved to {file_path}")

# Main function to retrain the model
def main():
    # Path to the training file and model file
    train_file_path = 'Clusters.txt'  # Replace with your training file path
    model_file_path = 'transition_matrix.pkl'  # File to save the updated model

    # Step 1: Load the training DNA sequence
    train_sequence = load_dna_sequence(train_file_path)
    print("Loaded training DNA sequence:", train_sequence)

    # Step 2: Generate k-mers and their mappings
    k = 2  # Set k (e.g., k=2 for dinucleotides)
    kmers, kmer_to_index, index_to_kmer = generate_kmers(k)
    print("All possible k-mers:", kmers)
    print("k-mer to index mapping:", kmer_to_index)

    # Step 3: Convert the training sequence to k-mer indices
    train_kmer_indices = sequence_to_kmers(train_sequence, k, kmer_to_index)
    print("Training k-mer indices:", train_kmer_indices)

    # Step 4: Build the transition matrix using the training data
    num_kmers = len(kmers)
    transition_matrix = build_transition_matrix(train_kmer_indices, num_kmers)

    # Step 5: Save the updated transition matrix to a file
    save_model(transition_matrix, model_file_path)

# Run the main function
if __name__ == "__main__":
    main()