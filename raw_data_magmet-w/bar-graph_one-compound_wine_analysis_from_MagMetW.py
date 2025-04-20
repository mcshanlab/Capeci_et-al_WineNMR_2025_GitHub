import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

# ==================== USER INPUT ====================
compound_of_interest = "Methanol"  # <-- Change this to any compound name you want
# ====================================================

# Expected headers
headers = ['Compound ID', 'Compound Name', 'Concentration (µM)', 'Column 4', 'Column 5']

# Folder with CSVs
folder_path = './'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Wine category function
def categorize_wine_type(wine_name):
    wine_name_lower = wine_name.lower()
    if 'red' in wine_name_lower:
        return 'red'
    elif 'white' in wine_name_lower:
        return 'white'
    elif 'rose' in wine_name_lower or 'rosé' in wine_name_lower:
        return 'rose'
    elif 'orange' in wine_name_lower:
        return 'orange'
    else:
        return 'unknown'

# Clean label function
def clean_label(file_prefix):
    # Remove common suffixes like '_magmet_results'
    label = re.sub(r'_magmet_results$', '', file_prefix, flags=re.IGNORECASE)
    # Replace underscores with spaces
    label = label.replace('_', ' ')
    return label.strip().title()

# Define custom color map
wine_color_map = {
    'red': '#E72727',
    'white': '#C6C6C5',
    'rose': '#E093BF',
    'orange': '#F9AC3E',
    'unknown': '#888888'
}

# Collect data
compound_data = []

for input_csv_file in csv_files:
    file_path = os.path.join(folder_path, input_csv_file)
    file_prefix = os.path.splitext(os.path.basename(input_csv_file))[0]
    cleaned_label = clean_label(file_prefix)

    try:
        df = pd.read_csv(file_path, skiprows=10, header=None, names=headers)
        compound_row = df[df['Compound Name'] == compound_of_interest]

        if not compound_row.empty:
            concentration = compound_row['Concentration (µM)'].values[0]
            wine_category = categorize_wine_type(file_prefix)
            compound_data.append({
                'Wine Label': cleaned_label,
                'Concentration (µM)': concentration,
                'Wine Category': wine_category
            })
        else:
            print(f"[!] Compound '{compound_of_interest}' not found in {input_csv_file}")

    except Exception as e:
        print(f"[!] Error processing {input_csv_file}: {e}")

# Create and sort DataFrame
compound_df = pd.DataFrame(compound_data)
compound_df = compound_df.sort_values(by='Concentration (µM)', ascending=False)
compound_df['Color'] = compound_df['Wine Category'].map(wine_color_map)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(
    data=compound_df,
    x='Wine Label',
    y='Concentration (µM)',
    palette=compound_df.set_index('Wine Label')['Color'].to_dict()
)
plt.xticks(rotation=45, ha='right')
plt.title(f'Concentration of {compound_of_interest} in Different Wine Types')
plt.tight_layout()
plt.savefig(f"bar_plot_{compound_of_interest}_sorted.pdf", format='pdf')
plt.show()
