import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = r"C:\Users\ASUS\Desktop\DNA\clustered-nanopore-reads-dataset-main\adjusted_nucleotide_data.csv"
df = pd.read_csv(file_path)

# Count the occurrences of each nucleotide
nucleotide_counts = df["Nucleotide"].value_counts()

# Define colors for each nucleotide
colors = {
    "dAMP": "blue",
    "dTMP": "green",
    "dCMP": "orange",
    "dGMP": "purple"
}

# Plot each nucleotide separately with count
for nucleotide, color in colors.items():
    subset = df[df["Nucleotide"] == nucleotide]
    count = nucleotide_counts[nucleotide]  # Get the count from the value_counts
    plt.figure(figsize=(8, 6))
    plt.scatter(subset["Dwell Time (ms)"], subset["Current Drop (nA)"], c=color, alpha=0.5, label=nucleotide)
    plt.xlabel("Dwell Time (ms)")
    plt.ylabel("Current Drop (nA)")
    plt.title(f"Scatter Plot for {nucleotide} (Total: {count})")  # Add count in the title
    plt.legend()
    plt.grid(True)
    plt.show()

