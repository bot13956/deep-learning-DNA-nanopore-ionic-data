def calculate_accuracy(predicted_sequence, actual_sequence, test_sequence_length):
    predicted_part = predicted_sequence
    actual_part = actual_sequence[test_sequence_length:test_sequence_length + len(predicted_part)]

    correct = sum(p == a for p, a in zip(predicted_part, actual_part))
    total = len(actual_part)
    accuracy = (correct / total) * 100 if total > 0 else 0

    print(f"Predicted Part     : {predicted_part}")
    print(f"Actual Comparison  : {actual_part}")
    return accuracy

def main():
    predicted_sequence_file = 'predicted_sequence.txt'
    actual_sequence_file = 'Sample.txt'

    with open(predicted_sequence_file, 'r') as file:
        predicted_sequence = file.read().replace('\n', '')

    with open(actual_sequence_file, 'r') as file:
        actual_sequence = file.read().replace('\n', '')

    # Length of input sequence used for prediction (assumed from same file)
    # You may hardcode it or pass as variable if known explicitly
    test_sequence_length = len(actual_sequence) - len(predicted_sequence)

    accuracy = calculate_accuracy(predicted_sequence, actual_sequence, test_sequence_length)
    print(f"Prediction accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    main()
