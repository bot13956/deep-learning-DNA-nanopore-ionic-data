from itertools import product
from collections import defaultdict
import random
import pickle  # For saving and loading the model

def default_dict_int():
    return defaultdict(int)

def load_dna_sequence(file_path):
    with open(file_path, 'r') as file:
        sequence = file.read().replace('\n', '')
    valid_nucleotides = {'A', 'T', 'C', 'G'}
    cleaned_sequence = ''.join([char for char in sequence if char in valid_nucleotides])
    return cleaned_sequence

def generate_kmers(k):
    nucleotides = ['A', 'T', 'C', 'G']
    kmers = [''.join(p) for p in product(nucleotides, repeat=k)]
    kmer_to_index = {kmer: i for i, kmer in enumerate(kmers)}
    index_to_kmer = {i: kmer for kmer, i in kmer_to_index.items()}
    return kmers, kmer_to_index, index_to_kmer

def sequence_to_kmers(sequence, k, kmer_to_index):
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    return [kmer_to_index[kmer] for kmer in kmers if kmer in kmer_to_index]

def load_model(file_path):
    with open(file_path, 'rb') as file:
        transition_matrix = pickle.load(file)
    print(f"Model loaded from {file_path}")
    return transition_matrix

def predict_next_kmer_sampling(current_kmer, transition_matrix):
    if current_kmer in transition_matrix:
        next_kmers = list(transition_matrix[current_kmer].keys())
        probabilities = list(transition_matrix[current_kmer].values())
        return random.choices(next_kmers, weights=probabilities)[0]
    else:
        return random.choice(list(transition_matrix.keys()))

def predict_sequence(test_sequence, transition_matrix, k, kmer_to_index, index_to_kmer, prediction_length):
    test_kmer_indices = sequence_to_kmers(test_sequence, k, kmer_to_index)

    if not test_kmer_indices:
        raise ValueError("No valid k-mers found in the test sequence. Check if the sequence is too short or invalid.")

    current_kmer = test_kmer_indices[-1]
    predicted_indices = []

    for _ in range(prediction_length):
        next_kmer = predict_next_kmer_sampling(current_kmer, transition_matrix)
        predicted_indices.append(next_kmer)
        current_kmer = next_kmer

    predicted_kmers = [index_to_kmer[idx] for idx in predicted_indices if idx in index_to_kmer]
    predicted_chars = ''.join([kmer[-1] for kmer in predicted_kmers])
    return predicted_chars  # return only prediction

def save_predicted_sequence(predicted_sequence, file_path):
    with open(file_path, 'w') as file:
        file.write(predicted_sequence)
    print(f"Predicted sequence saved to {file_path}")

def main():
    test_file_path = 'Sample.txt'
    model_file_path = 'transition_matrix.pkl'
    predicted_sequence_file = 'predicted_sequence.txt'

    k = 2
    _, kmer_to_index, index_to_kmer = generate_kmers(k)
    transition_matrix = load_model(model_file_path)
    test_sequence = load_dna_sequence(test_file_path)

    print(f"Test sequence: {test_sequence}")
    print(f"Length of test sequence: {len(test_sequence)}")

    test_kmer_indices = sequence_to_kmers(test_sequence, k, kmer_to_index)
    print(f"Generated test k-mer indices: {test_kmer_indices}")

    if not test_kmer_indices:
        print("Error: Test sequence is too short or does not contain valid k-mers.")
        return

    prediction_length = 100
    predicted_part = predict_sequence(test_sequence, transition_matrix, k, kmer_to_index, index_to_kmer, prediction_length)

    save_predicted_sequence(predicted_part, predicted_sequence_file)

if __name__ == "__main__":
    main()
