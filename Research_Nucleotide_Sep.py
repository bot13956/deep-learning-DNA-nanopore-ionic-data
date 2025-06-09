import pandas as pd
import matplotlib.pyplot as plt

# Load the updated dataset with blockade height
file_path = r"C:\Users\ASUS\Desktop\DNA\clustered-nanopore-reads-dataset-main\ResearchData_with_BlockadeHeight.csv"
df = pd.read_csv(file_path)

# Define nucleotide color and label mapping
colors = {
    "A": "blue",
    "T": "green",
    "C": "orange",
    "G": "purple"
}

labels = {
    "A": "dAMP",
    "T": "dTMP",
    "C": "dCMP",
    "G": "dGMP"
}

# ===============================
# Part 1: Combined Scatter Plot
# ===============================
plt.figure(figsize=(10, 7))
for base, color in colors.items():
    subset = df[df["Type"] == base]
    plt.scatter(subset["t"], subset["Blockade_Height"], c=color, alpha=0.5, label=labels[base])

plt.xlabel("Dwell Time (s)")
plt.ylabel("Blockade Height (pA)")
plt.title("Combined Scatter Plot: Blockade Height vs Dwell Time (All Nucleotides)")
plt.legend()
plt.grid(True)
plt.show()

# ===============================
# Part 2: Individual Scatter Plots
# ===============================
nucleotide_counts = df["Type"].value_counts()

for base, color in colors.items():
    subset = df[df["Type"] == base]
    count = nucleotide_counts[base]
    plt.figure(figsize=(8, 6))
    plt.scatter(subset["t"], subset["Blockade_Height"], c=color, alpha=0.5, label=labels[base])
    plt.xlabel("Dwell Time (s)")
    plt.ylabel("Blockade Height (pA)")
    plt.title(f"{labels[base]} - Blockade Height vs Dwell Time (Total: {count})")
    plt.legend()
    plt.grid(True)
    plt.show()

# ===============================
# Summary of Counts
# ===============================
print("Total number of nucleotides in each category:")
print(nucleotide_counts)


I0 = df["I"].quantile(0.95)
print(f"95th percentile of current (I0): {I0} pA")


df["Blockade_Height"] = I0 - df["I"]
# Save the updated DataFrame with Blockade Height
df.to_csv(file_path, index=False)