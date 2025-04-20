import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# usage: python3 complete_wine_analysis_from_MagMetW.py

# Define the compound class mapping
compound_classes = {
    "Alcohols": [
        "1_3-Propanediol", "2-Methylbutanol", "2_3-Butanediol", "Acetoin", "Ethanolamine", "Ethyl lactate", "Glycerol",
        "Isoamylalcohol", "Isobutanol", "Methanol", "Phenylethanol", "Propanol"
    ],
    "Organic Acids": [
        "2-Hydroxyglutaric acid", "Citric acid", "Acetoacetate", "Formate", "Galacturonate", "Indole-3-lactate", "Lactic acid", "Malate",
        "Oxoglutarate", "Fumarate", "Pyruvate", "Shikimate", "Sorbate", "Succinate", "Tartarate"
    ],
    "Amino Acids": [
        "4-Aminobutyrate", "Alanine", "Asparagine", "Aspartate", "beta-Alanine", "Betaine", "Carnitine", "L-Proline",
        "Leucine", "Methionine", "Ornithine", "Phenylalanine", "Pyroglutamate", "Tyrosine"
    ],
    "Wine 'fault'": [
        "5-Hydroxymethyl-2-furancarboxaldehyde", "Acetaldehyde", "Acetaldehyde (bisulfite)", "Acetate", "Acetone",
        "Cadaverine", "Ethyl acetate"
    ],
    "Polyphenols": [
        "Caffeate", "Caftarate", "Catechin", "Epicatechin", "Ferulate", "Gallate", "Syringate", "Trigonelline", "Tyrosol"
    ],
    "Vitamins": [
        "Choline"
    ],
    "Sugars": [
        "Arabinose", "Fructose", "Galactose", "Glucose", "myo-Inositol", "Sucrose", "Trehalose", "Xylose"
    ],
    "Ethanol": [
        "Ethanol"
    ],
    "Nucleobases": [
        "Adenine", "Uridine", "Uracil"
    ],
    "Chemical shift standard": [
        "DSS", "Phasing compound"
    ]
}

# Define headers
headers = ['Compound ID', 'Compound Name', 'Concentration (µM)', 'Column 4', 'Column 5']

# Specify the folder containing the .csv files
folder_path = './'

# List all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Dictionary to hold compound comparison data across all files
compound_comparison_data = {}

# Process each CSV file
for input_csv_file in csv_files:
    file_prefix = os.path.splitext(os.path.basename(input_csv_file))[0]
    df = pd.read_csv(os.path.join(folder_path, input_csv_file), skiprows=10, header=None, names=headers)

    print(f"Processing file: {input_csv_file}")
    print(df.head())

    ethanol_concentration = 0
    other_concentrations = {class_name: 0 for class_name in compound_classes if class_name not in ["Ethanol", "Chemical shift standard"]}

    # Process rows in the CSV
    for _, row in df.iterrows():
        compound_name = row['Compound Name']
        concentration = row['Concentration (µM)']

        # Store per-compound concentration
        if compound_name not in compound_comparison_data:
            compound_comparison_data[compound_name] = {}
        compound_comparison_data[compound_name][file_prefix] = concentration

        if compound_name == "Ethanol":
            ethanol_concentration += concentration
        else:
            for class_name, compounds in compound_classes.items():
                if compound_name in compounds and class_name not in ["Ethanol", "Chemical shift standard"]:
                    other_concentrations[class_name] += concentration
                    break

    # ===== Pie Chart 1: Ethanol vs Others =====
    labels_1 = ['Ethanol', 'Others']
    values_1 = [ethanol_concentration, sum(other_concentrations.values())]
    colors_1 = sns.color_palette("pastel", 2)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges_1, texts_1 = ax.pie(values_1, labels=labels_1, startangle=140, colors=colors_1, labeldistance=1.2)
    for i, text in enumerate(texts_1):
        text.set_color(colors_1[i])

    percentages_1 = [f'{value / sum(values_1) * 100:.2f}%' for value in values_1]
    legend_labels_1 = [f"{labels_1[i]}: {percentages_1[i]}" for i in range(len(labels_1))]
    ax.legend(legend_labels_1, loc="center left", bbox_to_anchor=(1, 0.5), title="Compounds")

    ax.set_title(f'{file_prefix} - Ethanol vs Other Compounds')
    ax.axis('equal')
    plt.tight_layout()
    plt.savefig(f"{folder_path}/{file_prefix}_ethanol_vs_others_pie_chart.pdf", format="pdf")
    plt.show()

    # ===== Pie Chart 2: Compound Class Distribution (Excl. Ethanol) =====
    labels_2 = list(other_concentrations.keys())
    values_2 = list(other_concentrations.values())
    pastel_colors = sns.color_palette("pastel", len(labels_2))

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges_2, texts_2 = ax.pie(values_2, labels=labels_2, startangle=140, colors=pastel_colors, labeldistance=1.2)
    for i, text in enumerate(texts_2):
        text.set_color(pastel_colors[i])

    percentages_2 = [f'{value / sum(values_2) * 100:.2f}%' for value in values_2]
    legend_labels_2 = [f"{labels_2[i]}: {percentages_2[i]}" for i in range(len(labels_2))]
    ax.legend(legend_labels_2, loc="center left", bbox_to_anchor=(1, 0.5), title="Compound %")

    ax.set_title(f'{file_prefix} - Distribution of Compounds')
    ax.axis('equal')
    plt.tight_layout()
    plt.savefig(f"{folder_path}/{file_prefix}_distribution_of_compounds_pie_chart.pdf", format="pdf")
    plt.show()

# ===== After Processing All Files: Create Comparison Table =====

# Create a compound-to-class mapping
compound_to_class = {}
for class_name, compounds in compound_classes.items():
    for compound in compounds:
        compound_to_class[compound] = class_name

# Convert comparison dictionary to DataFrame
comparison_df = pd.DataFrame.from_dict(compound_comparison_data, orient='index').fillna(0)
comparison_df = comparison_df.sort_index()

# Add compound class as a new column
comparison_df.insert(0, 'Compound Class', comparison_df.index.map(lambda name: compound_to_class.get(name, 'Unknown')))

# Save the comparison table with class to Excel
comparison_excel_path = os.path.join(folder_path, 'compound_comparison_table.xlsx')
comparison_df.to_excel(comparison_excel_path, engine='openpyxl')

print(f"\n Compound comparison table saved to: {comparison_excel_path}")
